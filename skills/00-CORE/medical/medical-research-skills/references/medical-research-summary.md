# Medical Research Summary — AI in Healthcare (2025-2026)

## Ophthalmology (طب العيون)

### Reti-Pioneer — Nature Medicine 2026
- **URL:** https://www.nature.com/articles/s41591-026-04359-w
- **What:** Multi-disease screening via retinal fundus photos (CFPs)
- **Data:** 107,730 CFPs (53,865 individuals) from UK Biobank + Chinese hospitals
- **Models:** Swin Transformer + Vision Mamba + RETFound ensemble
- **Innovation:** Links retinal features to proteomic/genetic markers
- **Validation:** Prospective silent trial + clinical pilot
- **Impact:** Scalable, clinically translatable AI framework for resource-limited settings

### EyeFM — Nature Medicine 2025
- **URL:** https://link.springer.com/article/10.1038/s41591-025-03900-7
- **What:** Multimodal vision-language eyecare copilot
- **Data:** 14.5 million ocular images, 5 imaging modalities, multiethnic
- **RCT:** 668 participants, 92.2% vs 75.4% diagnostic accuracy (AI vs standard care)
- **Impact:** Improved standardization, compliance, and referral rates

### OVFM — Nature Biomedical Engineering 2026
- **URL:** https://link.springer.com/article/10.1038/s41551-026-01622-w
- **What:** Ophthalmic video foundation model for surgical recognition
- **Data:** 1.1 million clips, 144 surgical types
- **Innovation:** Knowledge distillation for real-time deployment on surgical microscopes
- **Validation:** Cataract surgeries on wet-lab porcine eyes, 10 surgeons

---

## Neurology (المخ والأعصاب)

### Dual-Path Deep Learning — BMC Medical Informatics 2026
- **URL:** https://link.springer.com/article/10.1186/s12911-026-03367-7
- **What:** Joint brain tumor classification + content-based image retrieval (CBIR)
- **Architecture:** GhostNetV3 + deformable convolutions + DFC attention
- **Data:** 3,064 T1-weighted MRI images, 233 patients, 4 classes
- **Results:** 99.71% accuracy, 97.74% retrieval precision, CRAS > 0.96
- **Innovation:** Classification-Retrieval Agreement Score (CRAS) — new metric

### ConvNeXt Base — MDPI Bioengineering 2026
- **URL:** https://www.mdpi.com/2306-5354/13/2/157
- **What:** Explainable brain tumor classification on MRI
- **Architecture:** ConvNeXt Base
- **Data:** 3 independent MRI datasets, 4 classes (glioma, meningioma, pituitary, no tumor)
- **Results:** >99.6% accuracy, AUC ≈ 1.0
- **Validation:** Friedman's test, Holm/Wilcoxon, Kendall's W, TOPSIS
- **Explainability:** Grad-CAM++ + Gradient SHAP

---

## Internal Medicine (الباطنة)

### DxDirector-7B — Nature Communications 2026
- **URL:** https://www.nature.com/articles/s41467-026-71928-5
- **What:** Agentic LLM for full-process clinical diagnosis
- **Innovation:** Autonomously drives diagnostic workflow, requests physician only for procedures
- **Results:** Superior to state-of-the-art medical LLMs, reduces physician involvement
- **Validation:** Rare diseases + complex real-world cases

### Multimodal AMIE — Nature Medicine 2026
- **URL:** https://www.nature.com/articles/s41591-026-04371-0
- **What:** Conversational diagnostic AI with multimodal reasoning
- **Extension of:** Articulate Medical Intelligence Explorer (AMIE)
- **Data:** Dermatology photos, ECGs, clinical documents
- **Validation:** 105 simulated telehealth consultations, rated by 18 specialists
- **Results:** Outperformed PCPs in 29/32 evaluation axes
- **Innovation:** State-aware dialogue framework using Gemini 2.0 Flash

---

## Priority Ranking

| Priority | Paper | Domain | Impact Score |
|----------|-------|--------|-------------|
| 🔴 High | Reti-Pioneer | Ophthalmology | 9/10 |
| 🔴 High | EyeFM | Ophthalmology | 9/10 |
| 🔴 High | DxDirector-7B | Internal Medicine | 9/10 |
| 🔴 High | Multimodal AMIE | Internal Medicine | 8/10 |
| 🔴 High | Dual-Path DL | Neurology | 8/10 |
| 🟠 Medium | ConvNeXt | Neurology | 7/10 |
| 🟠 Medium | OVFM | Ophthalmology | 7/10 |
