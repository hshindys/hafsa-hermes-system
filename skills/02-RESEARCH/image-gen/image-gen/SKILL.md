---
name: image-gen
description: Generate images using FLUX (via FAL.ai) and ComfyUI workflows. MUST USE when user asks for image generation, illustrations, character design, scene visualization, concept art, or image editing. Supports text-to-image and image-to-image.
---

# Image Generation — FLUX + ComfyUI

High-quality image generation using FLUX models via FAL.ai backend. Optimized for book illustrations, character design, and concept art.

## Workflow

### 1. Determine the type
- **Text-to-image**: Generate from a descriptive prompt
- **Image-to-image**: Edit/transform an existing image
- **Style reference**: Use reference images for style guidance

### 2. Write the prompt
Use detailed, structured prompts:
- Subject description (character, scene, object)
- Style (photorealistic, oil painting, watercolor, anime, etc.)
- Lighting and atmosphere
- Composition (landscape, portrait, square)
- Quality modifiers: high detail, professional, award-winning

**For رواية كرون ( Kron novel):**
- Genre: fantasy/philosophical/adventure
- Visual style: Middle Eastern/Sindbad-inspired with magical elements
- Key elements: Jinn civilization, rainbow wings, fish-scale eyes, ancient libraries, cosmic themes

### 3. Aspect ratio
- `landscape` (16:9) — scenes, wide shots
- `portrait` (16:9 tall) — character portraits
- `square` (1:1) — icons, book covers, concept art

### 4. Generation
- Primary: FLUX 2 Klein 9B via FAL.ai
- Support up to 9 reference images
- Max resolution depends on backend
- Output: URL or local file path

### 5. Post-processing
- Save reference images to `/home/hatem/Documents/Hatem Nad/رواية-كرون/references/images/`
- Log prompt + result in project notes
- Tag images for easy retrieval

## User preferences
- Language: Arabic prompts preferred, English accepted
- Style: Literary, magical realism, philosophical
- Characters:特点 رواية كرون (fish-scale eyes, hidden rainbow wings, jinn features)
- Avoid: clichéd fantasy tropes, Western-centric art
