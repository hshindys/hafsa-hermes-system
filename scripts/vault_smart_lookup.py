#!/usr/bin/env python3
"""
Lightweight Vault Smart Lookup — vault-aware
- Pure stdlib
- BM25-ish scoring over markdown corpus
- Relationship traversal for entity markdown files
- Supports multiple vaults via --vault
"""

import argparse
import json
import os
import re
import math
from collections import defaultdict
from pathlib import Path

DEFAULT_VAULT = Path("/home/hatem/Documents/Hafsa")


def iter_md_files(path: Path):
    for p in path.rglob("*.md"):
        if any(skip in str(p).lower() for skip in [".trash", ".obsidian", ".git"]):
            continue
        yield p


STOP = {
    "في", "من", "إلى", "على", "هذا", "تلك", "التي", "الذي", "كان", "كانت",
    "له", "لها", "ما", "عن", "التى", "الذى", "حتى", "أو", "ثم", "أن", "لا"
}


def tokenize(text: str):
    text = text.lower()
    tokens = re.findall(r"[A-Za-z\u0600-\u06FF]{2,}", text)
    return [t for t in tokens if t not in STOP and len(t.strip()) > 1]


def load_index(vault: Path):
    safe = vault.name.strip()
    index_name = f".smart_lookup_index.{safe}.json"
    index_file = vault / index_name
    if index_file.exists():
        try:
            return json.loads(index_file.read_text(encoding="utf-8"))
        except Exception:
            pass
    return None


def build_index(vault: Path, force: bool = False):
    safe = vault.name.strip()
    index_name = f".smart_lookup_index.{safe}.json"
    index_file = vault / index_name
    if index_file.exists() and not force:
        cached = load_index(vault)
        if cached:
            return cached
    docs = {}
    inverted = defaultdict(list)
    counts = defaultdict(int)
    for path in iter_md_files(vault):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = path.relative_to(vault)
        doc_id = str(rel)
        tokens = tokenize(text + " " + path.stem)
        for t in set(tokens):
            inverted[t].append(doc_id)
        docs[doc_id] = {"title": path.stem, "path": doc_id, "tokens": tokens}
        for t in tokens:
            counts[t] += 1
    payload = {"docs": docs, "inverted": dict(inverted), "counts": dict(counts)}
    index_file.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    return payload


def smart_search(query: str, vault: Path, top_k: int = 10):
    payload = build_index(vault)
    docs = payload["docs"]
    inverted = payload["inverted"]
    counts = payload["counts"]
    q_tokens = tokenize(query)
    if not q_tokens:
        return []
    scores = defaultdict(float)
    avgdl = sum(len(d["tokens"]) for d in docs.values()) / max(len(docs), 1)
    k1, b = 1.5, 0.75
    for t in q_tokens:
        postings = inverted.get(t, [])
        df = len(postings)
        if df == 0:
            continue
        idf = math.log(1 + (len(docs) - df + 0.5) / (df + 0.5))
        for doc_id in postings:
            dl = len(docs[doc_id]["tokens"])
            tf = docs[doc_id]["tokens"].count(t)
            denom = tf + k1 * (1 - b + b * dl / max(avgdl, 1))
            scores[doc_id] += idf * tf / denom
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [{"title": docs[d]["title"], "path": docs[d]["path"], "score": round(s, 3)} for d, s in ranked]


def extra_entity_roots() -> list[Path]:
    raw = os.environ.get("VAULT_EXTRA_ROOTS", "")
    roots = []
    for item in raw.split(":"):
        item = item.strip()
        if item:
            roots.append(Path(item).expanduser().resolve())
    return roots

def traverse_entity(name: str, vault: Path):
    roots = [vault, *extra_entity_roots()]
    name_l = name.strip().lower()
    hits = []
    rels = []
    for root in roots:
        if not root.exists():
            continue
        for p in root.rglob("*.md"):
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore").lower()
            except Exception:
                continue
            if name_l in txt:
                try:
                    hits.append(str(p.relative_to(root)))
                except ValueError:
                    hits.append(str(p))
        rel_dir = root / "Relations"
        rel_file = rel_dir / f"{name}.md"
        if rel_file.exists():
            rels.extend([l for l in rel_file.read_text(encoding="utf-8").splitlines() if l.strip()])
    if not hits and not rels:
        return None
    return {"entities": hits, "relations": rels}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", "-q")
    ap.add_argument("--entity", "-e")
    ap.add_argument("--vault", "-v", default=str(DEFAULT_VAULT))
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    vault = Path(args.vault).expanduser().resolve()
    if args.entity:
        out = traverse_entity(args.entity, vault)
        if not out:
            print(json.dumps({"error": "Not found"}, ensure_ascii=False))
            return
        print(json.dumps(out, ensure_ascii=False))
        return
    if not args.query:
        ap.print_help()
        return
    results = smart_search(args.query, vault, top_k=10)
    print(json.dumps({"query": args.query, "vault": str(vault), "results": results}, ensure_ascii=False))


if __name__ == "__main__":
    main()
