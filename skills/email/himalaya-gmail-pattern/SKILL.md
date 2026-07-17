---
name: himalaya-gmail-pattern
description: "Validated himalaya 1.2.0 Gmail config shape and verified probing steps."
version: 0.1.0
author: Hafsa
license: MIT
metadata:
  hermes:
    tags: [email, himalaya, gmail]
---

# Himalaya Gmail Pattern

Use this when wiring himalaya to a Gmail account. It distills the exact config shape that parsed correctly for `backend.auth.type` in this environment, plus the probe sequence to move from parser success to operational verification.

## Verified config shape

```toml
[accounts.hafsa]
email = "hshindys@gmail.com"
display-name = "Hafsa"
default = true

backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "hshindys@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "echo APP_PASSWORD_OR_PASS_CMD"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "hshindys@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "echo APP_PASSWORD_OR_PASS_CMD"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

## Known format fact from this session

With himalaya `v1.2.0`, `backend.auth.type = "password"` interpreted `backend.auth.cmd` correctly when the auth block was present on both IMAP and SMTP. Other forms like `backend.auth.password = "..."`, `backend.auth.raw = "..."`, `backend.auth.type = "cmd"`, or `backend.auth.type = "command"` all failed parser validation with the same TOML error surface in this build.

## Verification sequence

1. `himalaya account list`
2. `himalaya envelope list --account hafsa -o plain`
3. If auth fails, it is almost always credentials, not config shape.

## Security

- Keep the config file mode `600`.
- Do not paste live app passwords in logs or chat. Use `pass show ...` or local secret files in production.
