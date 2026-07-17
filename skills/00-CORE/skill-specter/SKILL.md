---
id: skill-specter
name: Skill Specter
description: Security scanner for AI agent skills using NVIDIA garak. Use before installing any new skill to detect vulnerabilities, prompt injection, data exfiltration, and other risks. Invoke with 'use_skill("skill-specter")' or 'scan skill: <path>' or 'scan repo: <url>' or 'scan url: <url>'.
triggers:
  - "specter"
  - "skill scanner"
  - "scan skill"
  - "garak"
  - "security scan"
  - "scan for vulnerabilities"
---

# Skill Specter (NVIDIA garak-based scanner)

You now have a local scanner that audits AI agent skills/materials for security risks before you install or trust them.

## Tool path (Python CLI)
- Scanner root: `/home/hatem/.hermes/profiles/hafsa/tools/skill-scanner`
- Install: `python3 -m pip install -r requirements.txt`
- Run: `python3 -m garak --model_type probe --probes all <target>` or use the wrapper in `skill_scanner/`
- Result file: latest report under `runs/` (garak default) or as printed output

## Quick routes
- **Directory/repo:** run from project dir or pass abs path
- **Remote repo tar/zip:** download then scan
- **URL/single file:** fetch → save under a temp scan dir → scan that dir
- **Frontend file (.tsx/.jsx/.js/.ts):** prefer static AST via `semgrep` — much fewer false positives

## Why this matters
Skills are executed code on your machine. Scan before you install.
