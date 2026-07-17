---
name: glm-open-design-system
description: >
  MUST USE when building UI/UX, landing pages, dashboards, or any design work.
  Uses GLM-5.2 + OpenDesign for high-quality, consistent design output.
  
  Key capabilities:
  - Landing page generation with consistent design system
  - Dashboard UI design with real HTML/CSS output
  - Mobile interface prototyping
  - Design system creation (colors, typography, spacing, components)
  - Multi-page consistent design
  
  Models available:
  - GLM-5.2: 1M context, 128K output, best for complex design tasks
  - GLM-5.1: 202K context, cheaper, good for simpler tasks
  
  NOT for: backend development, data analysis, non-design tasks.
metadata:
  hermes:
    tags: [design, ui, ux, glm-5.2, open-design, landing-page, dashboard]
    priority: high
---

# GLM-5.2 + OpenDesign — Design System

## Overview
Use GLM-5.2 with OpenDesign for high-quality, consistent UI/UX design. The combination provides:
- Long-context design consistency (colors, typography, spacing)
- Real HTML/CSS output (not screenshots)
- Multi-page design system coherence
- Tool calling for complex design tasks

## Available Models

| Model | Context | Output | Best For |
|-------|---------|--------|----------|
| GLM-5.2 | 1M tokens | 128K | Complex design systems, multi-page |
| GLM-5.1 | 202K tokens | 65K | Simpler designs, cheaper |

## Design Workflow

### 1. Define Design System
Before generating any page, define:
- **Colors:** Primary, secondary, accent, neutral palette
- **Typography:** Font families, sizes, weights, line heights
- **Spacing:** Base unit (8px), spacing scale
- **Components:** Buttons, cards, inputs, navigation
- **Responsive:** Breakpoints for mobile, tablet, desktop

### 2. Generate Design
Use GLM-5.2 with detailed prompts:
```
Design a landing page for [product] with:
- Color palette: [specific colors]
- Typography: [font choices]
- Sections: hero, features, testimonials, CTA
- Responsive: mobile-first
- Style: [modern/minimal/bold/etc.]
```

### 3. Export & Iterate
- Output is real HTML/CSS
- Preview in browser
- Edit directly or request changes
- Hand off to coding agent if needed

## Real-World Session Findings (2026-06-22)

### Available Now
- GLM-5.2 lives at `z-ai/glm-5.2` on OpenRouter (1M context / $0.98 input, $3.08 output per 1M tokens).
- GLM-5.1 at `z-ai/glm-5.1` (202K context) for cheaper drafts.
- The OpenDesign GitHub repo `Yaxin9Luo/OpenDesign` may be inaccessible via direct clone; prefer the npm bridge (`open-design-mcp`) or build UI directly.

### Outputs Already Built
- Hafsa landing page at `~/Documents/Hafsa-1/🎯 المشاریع/حفصة-landing-page/index.html`
- Vault analytics dashboard at `~/Documents/Hafsa-1/🎯 المشاریع/حفصة-dashboard/index.html`
- These files use RTL/dark theme consistent with our visual system.

### Known Constraints
- OpenDesign daemon requires desktop app runtime; for Hermes integration, prefer direct HTML/CSS builds.
- Arabic filenames and emoji paths break in shell pipelines — use `write_file` / `read_file` for paths with Arabic or emoji segments.

## Usage Examples

### Landing Page
```
Model: GLM-5.2
Prompt: Design a modern landing page for an AI agent platform.
Include: hero section, feature grid (6 features), testimonials, pricing table, footer.
Style: dark mode, blue accent, Inter font, 8px spacing system.
```

### Dashboard
```
Model: GLM-5.2
Prompt: Design an analytics dashboard with:
- Sidebar navigation
- Stats cards (4 metrics)
- Line chart area
- Data table
- Responsive layout
```

### Mobile Interface
```
Model: GLM-5.1
Prompt: Design a mobile app interface for [app type].
Include: bottom nav, header, content area, floating action button.
Style: iOS-like, rounded corners, subtle shadows.
```

## Integration with Hermes

## Integration with Hermes

### Switch to GLM-5.2 for design tasks:
```
/model z-ai/glm-5.2
```

### Switch back to default:
```
/model openrouter/owl-alpha
```

## Design Quality Checklist

Every design must have:
- [ ] Consistent color palette
- [ ] Consistent typography (max 2-3 fonts)
- [ ] Consistent spacing (8px base unit)
- [ ] Responsive behavior defined
- [ ] Component reusability
- [ ] Accessibility (contrast, font sizes)
- [ ] Real HTML/CSS output (not screenshots)

## Pitfalls to Avoid
1. Vague prompts → generic AI-looking output
2. No design system definition → inconsistent pages
3. Too many colors/fonts → visual chaos
4. Ignoring responsive → broken on mobile
5. Screenshot-only output → needs rebuild
