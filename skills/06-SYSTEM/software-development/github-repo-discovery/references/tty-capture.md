# Capturing TTY Output from Interactive CLI Processes

Interactive CLI tools (OAuth flows, password prompts, etc.) often print a URL or code
then block waiting for user input. These processes write to the TTY, not to stdout
pipes, so regular `subprocess.Popen(stdout=PIPE)` capture hangs silently.

## Problem

```python
# This HANGS — process writes URL to TTY, not pipe
proc = subprocess.Popen(
    ["hermes", "auth", "add", "xai-oauth", "--no-browser"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
output = proc.stdout.readline()  # blocks forever, reads nothing
```

Same issue with `terminal(command="...")` in foreground mode — the command blocks
waiting for browser callback.

## Solutions

### 1. PTY Mode (preferred)

Run with `pty: true` to allocate a pseudo-TTY. Process writes to the PTY as if it
were a real terminal, and parent can read its output.

```
(background=true, pty=true, notify_on_complete=true)
    ↓ hermes auth add xai-oauth --no-browser
    ↓ prints: "Open this URL to authorize: https://..."
    ↓ Waiting for callback on http://127.0.0.1:56121/callback
```

Then poll: `process(action='poll')` → read `output_preview`

After capturing the URL, **leave the process running** in the background. When the
user opens the URL in their browser and approves, the process completes automatically.

### 2. script command

```bash
script -q -c "hermes auth add xai-oauth --no-browser" /dev/null
```

Forces TTY allocation at the OS level. Not installed on minimal systems by default.

### 3. manual-paste mode

```
hermes auth add xai-oauth --manual-paste
```

Skips the loopback listener entirely. Process prints a code, user pastes it back.

## Callback Port Considerations

OAuth flows use a loopback callback server (e.g. `127.0.0.1:56121`). The browser
must reach **the machine where the process is running**. If the agent is on a remote
server, the user needs an SSH tunnel on their local machine:

```bash
ssh -N -L 56121:127.0.0.1:56121 user@remote-host
```

Only then open the authorization URL in their local browser.

## Key Insight

The process is NOT broken or hung — it's actively listening for the HTTP callback.
Killing it mid-flow means re-running and getting a new URL. Let it run in the
background while the user completes the browser step.
