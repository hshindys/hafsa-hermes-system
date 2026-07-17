# 2026-06-22 OpenDesign session notes

## Verified
- GLM-5.2 OpenRouter model ID: `z-ai/glm-5.2`
- GLM-5.1 OpenRouter model ID: `z-ai/glm-5.1`
- `open-design-mcp` installs via npm globally; missing `OD_DAEMON_URL` blocks startup.
- Yaxin9Luo/OpenDesign git clone returned `Repository not found`; use npm bridge or direct HTML builds instead.
- Filesystem paths with Arabic folders + emoji break in shell heredocs; `write_file` works on `/home/hatem/Documents/Hafsa/🎯 المشاریع/...`.

## Built artifacts
- Landing page: `~/Documents/Hafsa/🎯 المشاریع/حفصة-landing-page/index.html`
- Dashboard: `~/Documents/Hafsa/🎯 المشاریع/حفصة-dashboard/index.html`

## Local integration observations
- Hermes config modification via YAML script succeeded.
- Safe prose feedback on draft design output.
- Browser snapshot returned OpenRouter model page content, not tool output.
