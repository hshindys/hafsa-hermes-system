#!/usr/bin/env python3
"""
Vault-aware Smart Lookup wrapper
Honors per-vault config: routing + smart-lookup command
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_SCRIPT = "/home/hatem/.hermes/profiles/hafsa/scripts/vault_smart_lookup.py"


def detect_vault_root(path_str: str) -> Path:
    p = Path(path_str).expanduser().resolve()
    if (p / "📌 Index.md").exists() or (p / "🧠 Hafsa Vault.md").exists() or (p / "🧠 Hatem Vault.md").exists():
        return p
    return p


def build_routing_file(vault: Path):
    # placeholder in case we want to write routing file dynamically
    return vault / "🧠 Vault.md"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", "-v", default=str(Path("/home/hatem/Documents/Hafsa").resolve()))
    ap.add_argument("--query", "-q")
    ap.add_argument("--entity", "-e")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    script = Path(os.environ.get("VAULT_SMART_SCRIPT", DEFAULT_SCRIPT))
    if not script.exists():
        print(json.dumps({"error": f"Smart lookup script not found: {script}"}, ensure_ascii=False))
        sys.exit(1)
    cmd = [sys.executable, str(script)]
    vault = detect_vault_root(args.vault)
    cmd += ["--vault", str(vault)]
    if args.query:
        cmd += ["--query", args.query]
    if args.entity:
        cmd += ["--entity", args.entity]
    if args.rebuild:
        cmd += ["--rebuild"]
    try:
        out = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as e:
        print(json.dumps({"error": e.stderr or str(e)}, ensure_ascii=False))
        sys.exit(1)
    sys.stdout.write(out)


if __name__ == "__main__":
    main()
