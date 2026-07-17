---
name: ophthalmology-ai-retinal-analysis
description: >
  MUST USE when analyzing retinal images (fundus photos, OCT scans) or when
  user mentions eye diseases, retinal screening, or ophthalmology AI.
  
  Covers: Reti-Pioneer framework for multidisease detection via retinal imaging,
  EyeFM clinical copilot, OVFM surgical video analysis.
  
  Key capabilities:
  - Retinal image analysis for systemic disease detection
  - Diabetic retinopathy screening
  - Glaucoma detection
  - Age-related macular degeneration (AMD) classification
  - Surgical step recognition in ophthalmic procedures
  
  NOT for: general eye complaints without imaging, prescription writing.
metadata:
  hermes:
    tags: [ophthalmology, retinal-imaging, ai-diagnosis, eye-diseases]
    priority: high
---

# Ophthalmology AI — Retinal Image Analysis

## Core Framework: Reti-Pioneer (Nature Medicine, 2026)

### What it does
Uses retinal fundus photos (CFPs) to screen for endocrine and metabolic diseases — not just eye diseases.

### Key Results
- 107,730 CFPs from UK Biobank + Chinese tertiary hospitals
- Multi-task framework integrating vision foundation models (Swin Transformer, Vision Mamba, RETFound)
- Links retinal features to proteomic and genetic markers
- Validated in prospective silent trial + clinical pilot

### Clinical Applications
1. **Diabetic Retinopathy Screening** — automated grading from fundus photos
2. **Systemic Disease Detection** — diabetes, hypertension, kidney disease markers in retinal images
3. **Surgical Navigation** — OVFM for real-time ophthalmic surgery assistance

### EyeFM Clinical Copilot (Nature Medicine, 2025)
- Pretrained on 14.5 million ocular images
- RCT on 668 patients: 92.2% vs 75.4% diagnostic accuracy
- Improves ophthalmologist performance across all metrics

### OVFM — Surgical Video Analysis (Nature Biomedical Engineering, 2026)
- 1.1 million video clips, 144 surgical types
- Real-time surgical step recognition and navigation
- Deployable on surgical microscope units

## Quick Reference

| Task | Model | Accuracy | Source |
|------|-------|----------|--------|
| Retinal disease screening | Reti-Pioneer | Multi-disease | Nature Medicine 2026 |
| Clinical diagnosis assistance | EyeFM | 92.2% | Nature Medicine 2025 |
| Surgical video analysis | OVFM | State-of-art | Nat Biomed Eng 2026 |

## Usage Guidelines
1. Always confirm image quality before analysis
2. Flag urgent findings (retinal detachment, acute glaucoma) immediately
3. Recommend specialist referral for complex cases
4. Document all AI-assisted findings in patient record
