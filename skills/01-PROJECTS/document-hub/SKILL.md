---
name: document-hub
description: >
  MUST USE when user wants to create, search, filter, preview, or delete documents
  created by the agent. Provides a unified document management system.
  
  Key capabilities:
  - Create documents (invoices, reports, notes, code)
  - Search and filter by type, date, content
  - Preview documents in multiple formats
  - Delete and organize documents
  - Real-time sync with agent workspace
  
  NOT for: file system management, backup, version control.
metadata:
  hermes:
    tags: [document-hub, documents, management, search, filter]
    priority: high
---

# Document Hub — Unified Document Management

## Overview
Document Hub provides a single location for all documents created by the agent. No more losing track of invoices, reports, or notes.

## Document Types

| Type | Format | Use Case |
|------|--------|----------|
| Invoice | HTML/PDF | Billing, payments |
| Report | Markdown/PDF | Research, analysis |
| Note | Markdown | Quick notes, ideas |
| Code | Various | Scripts, projects |
| Medical | Markdown | Research summaries, skills |
| Video Summary | Markdown | YouTube summaries |

## Document Structure

```
~/Documents/Hafsa-1/
├── 📋 Video Summaries/     # Video summaries
├── 🏥 Medical/             # Medical research and skills
├── 🔧 Skills/              # Agent skills
├── 📊 Reports/             # Generated reports
├── 📝 Notes/               # Quick notes
└── 📄 Invoices/            # Generated invoices
```

## Search & Filter

### By Type
- `type:invoice` — All invoices
- `type:report` — All reports
- `type:note` — All notes
- `type:medical` — Medical documents
- `type:skill` — Skill documents

### By Date
- `date:today` — Today's documents
- `date:week` — This week's documents
- `date:month` — This month's documents

### By Content
- Full-text search across all documents
- Regex pattern matching
- Tag-based filtering

## Document Creation Workflow

### 1. Agent creates document
- Agent generates content (invoice, report, note)
- Saves to appropriate folder in vault
- Adds frontmatter with metadata

### 2. Document sync
- Symlink to agent workspace
- Real-time updates
- Version tracking

### 3. User access
- Search and filter
- Preview in multiple formats
- Delete or archive

## Frontmatter Template

```yaml
---
title: Document Title
type: invoice|report|note|medical|skill
date: YYYY-MM-DD
author: Hafsa Agent
tags: [tag1, tag2]
status: active|archived|deleted
---
```

## Usage

### Create document
```bash
# Agent creates document automatically
# User can request specific documents
```

### Search documents
```bash
# Search by type
search --type invoice

# Search by content
search --query "medical research"

# Search by date
search --date today
```

### Delete document
```bash
# Move to archive (don't delete permanently)
archive --file "document-name"

# Delete permanently
delete --file "document-name"
```

## Integration with Obsidian
- All documents stored in Obsidian vault
- Full-text search via Obsidian
- Graph view for document relationships
- Tags and folders for organization
