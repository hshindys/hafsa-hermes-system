---
id: hyperframes
name: Hyperframes / HyperFrames-Studio
description: Turn HTML/CSS/media into deterministic MP4 videos. Use for demos, animations, slides, and motion graphics. Invoke with 'use_skill("hyperframes")'.
triggers:
  - "hyperframes"
  - "html to video"
  - "mp4"
  - "video gen"
  - "motion graphics"
  - "animation"
---

# Hyperframes / HyperFrames-Studio

## Repo
`/home/hatem/.hermes/profiles/hafsa/tools/HyperFrames-Studio`

## What
Open-source framework for deterministic MP4 generation from HTML/CSS, media, and seekable animations.

## Use cases
- Product demos, slides, motion graphics, cinematic trailers
- Reusable templates + data-driven renders
- Plug into AI coding agents / Hermes for video output

## Setup (best path)
1. Read `README.md` for install instructions for your OS.
2. Run local renderer: Chrome + FFmpeg are required.
3. For agent mode, use skills: put repo on PATH and call with prompt → output MP4.

## Output
Render result as absolute path MP4 in repo output folder.

## Usage in this session
Call `use_skill("hyperframes")` to enter Hyperframes mode and describe the video scene/template to build.
