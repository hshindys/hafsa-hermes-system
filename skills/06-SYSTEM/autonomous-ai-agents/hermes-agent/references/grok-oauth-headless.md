# Grok OAuth Headless / Remote Login

When running `hermes auth add xai-oauth` on a server or container without a browser, the `--no-browser` flag prints an authorization URL instead of opening a browser. The callback listener binds to `127.0.0.1:56121` on the machine where Hermes runs.

## The Problem

If you run the command as a background process or from a non-interactive shell, the OAuth URL may not be visible in the output because:
1. The process blocks waiting for the callback
2. Output may be buffered when piped or backgrounded
3. The URL changes on each invocation (state/nonce are unique per call)

## Solution: PTY Mode for URL Capture

Use `terminal(pty=true)` to run the auth command in a pseudo-terminal, which makes the output visible:

```
terminal(background=true, pty=true, command="hermes -p <profile> auth add xai-oauth --no-browser", notify_on_complete=true)
```

Then poll for the output:

```
process(action=poll, session_id=<sid>)
process(action=log, session_id=<sid>)
```

The output will contain:
```
Open this URL to authorize Hermes with xAI:
https://auth.x.ai/oauth2/authorize?response_type=code&client_id=...&redirect_uri=...

Waiting for callback on http://127.0.0.1:56121/callback
```

**Copy the URL** and open it in a browser on the same machine (or via SSH tunnel if remote).

## SSH Tunnel for Remote Hosts

If Hermes runs on a remote server and your browser is local:

```bash
# Terminal 1 (local machine):
ssh -N -L 56121:127.0.0.1:56121 user@remote-host

# Terminal 2 (remote):
hermes auth add xai-oauth --no-browser
```

Then open the printed URL in your local browser — the callback reaches the remote listener via the tunnel.

## Manual Paste (Browser-only Consoles)

For environments like GCP Cloud Shell, GitHub Codespaces, or AWS EC2 Instance Connect where SSH tunnels aren't available:

```bash
hermes auth add xai-oauth --manual-paste
```

This skips the loopback listener entirely. If xAI shows an authorization code directly on the page (instead of redirecting), paste just the bare code value at the prompt.

## After Successful Login

Verify with:
```bash
hermes auth list
```

Look for `xai-oauth` with status `loopback_pkce ←`.

The same OAuth token is automatically reused by all direct-to-xAI tools: TTS, image generation, video generation, transcription, and X (Twitter) search.
