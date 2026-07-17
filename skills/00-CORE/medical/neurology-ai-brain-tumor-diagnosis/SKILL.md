---
name: neurology-ai-brain-tumor-diagnosis
description: >
  MUST USE when analyzing brain MRI scans, discussing brain tumors, or when
  user mentions neurology AI, neuroimaging, or CNS diseases.
  
  Covers: Dual-path deep learning for brain tumor classification, ConvNeXt-based
  MRI analysis, content-based image retrieval (CBIR) for similar case matching.
  
  Key capabilities:
  - Brain tumor classification (glioma, meningioma, pituitary, no tumor)
  - MRI-based diagnostic support
  - Similar case retrieval for clinical reference
  - Explainable AI with Grad-CAM++ and SHAP
  
  NOT for: stroke management, epilepsy, movement disorders (separate skills needed).
metadata:
  hermes:
    tags: [neurology, brain-tumor, mri, ai-diagnosis, neuroimaging]
    priority: high
---

# Neurology AI — Brain Tumor Diagnosis

## Core Framework: Dual-Path Deep Learning (BMC Medical Informatics, 2026)

### What it does
Simultaneously classifies brain tumors AND retrieves visually similar cases from a reference database.

### Key Results
- 99.71% classification accuracy (precision/recall/F1 > 0.99)
- 97.74% mean average retrieval precision
- New metric: Classification-Retrieval Agreement Score (CRAS) > 0.96
- Evaluated on 3,064 MRI images from 233 patients

### Architecture
- GhostNetV3 backbone (lightweight)
- Deformable convolutions (adapts to irregular tumor shapes)
- Decoupled Fully Connected (DFC) attention mechanism
- Joint optimization of classification + retrieval

### ConvNeXt Base Framework (MDPI Bioengineering, 2026)
- >99.6% accuracy across 3 independent datasets
- 4-class classification: glioma, meningioma, pituitary tumor, no tumor
- Explainable with Grad-CAM++ and Gradient SHAP
- Statistically validated with Friedman's test, Holm/Wilcoxon post hoc

## Quick Reference

| Task | Model | Accuracy | Source |
|------|-------|----------|--------|
| Brain tumor classification | Dual-Path DL | 99.71% | BMC Med Inform 2026 |
| Brain tumor classification | ConvNeXt Base | >99.6% | MDPI Bioeng 2026 |
| Similar case retrieval | CBIR | 97.74% | BMC Med Inform 2026 |

## Clinical Workflow
1. **MRI Acquisition** — T1-weighted contrast-enhanced images
2. **Preprocessing** — skull stripping, normalization, registration
3. **AI Analysis** — classification + similar case retrieval
4. **Report Generation** — structured report with confidence scores
5. **Specialist Review** — radiologist confirms AI findings

## Usage Guidelines
1. Always correlate AI findings with clinical presentation
2. Flag urgent findings (large tumors, midline shift, hydrocephalus)
3. Recommend biopsy for uncertain cases
4. Use similar case retrieval to support clinical decision-making
5. Document AI confidence scores in report
