# Herdr Linux binary install pattern

- Latest release tag: detected from `https://github.com/ogulcancelik/herdr/releases/latest`
- Binary names: `herdr-linux-aarch64`, `herdr-linux-x86_64`
- Direct URL: `https://github.com/ogulcancelik/herdr/releases/download/v0.7.3/herdr-linux-x86_64`
- Postinstall: `install -m 0755 /tmp/herdr-linux-x86_64 ~/.local/bin/herdr`
- Verify: `herdr --version` should print something like `herdr 0.7.3`
- Build fallback only when binaries fail: `cargo build --release` requires Zig 0.15.2 for vendored libghostty-vt; skip on Fedora unless Zig is installed.
