---
name: radiology-clinical-skills
description: >
  MUST USE when working with radiology reports, medical imaging, PACS workflows,
  or when user mentions DICOM, CT, MRI, X-ray, ultrasound, or nuclear medicine.
  
  26 skills covering:
  - Modality detection and radiology context
  - Report analysis and structured reporting
  - Patient communication (results letters, education)
  - Workflow coordination (referrals, followup, care gaps)
  - Platform integration (PACS, DICOM, PubMed)
  - AI assistance (report assist, detection pipeline, quality review)
  - Analytics (metrics, image quality, report quality)
  - Research (guidelines, cross-referencing)
  - Dataset management and model validation
  
  NOT for: non-radiology medical imaging, direct diagnosis.
metadata:
  hermes:
    tags: [radiology, imaging, DICOM, PACS, CT, MRI, X-ray, clinical]
    priority: high
---

# Radiology Clinical Skills

## Overview
26 skills for radiological analytics, reporting, and workflow management.

## Skill Categories

### Core (2 skills)
- **modality-detection:** Identify imaging modality (CT, MRI, X-ray, US, NM)
- **radiology-context:** Foundation skill for all radiology operations

### Clinical Documentation (3 skills)
- **radiology-report-analysis:** Parse and analyze radiology reports
- **structured-reporting:** Generate structured radiology reports
- **imaging-study-review:** Review imaging studies for quality and completeness

### Patient Communication (2 skills)
- **patient-results-letter:** Generate patient-friendly results letters
- **patient-education-material:** Create educational materials for patients

### Workflow Coordination (3 skills)
- **imaging-referral:** Manage imaging referrals
- **followup-tracking:** Track follow-up recommendations
- **care-gap-closure:** Identify and close care gaps

### Platform Integration (3 skills)
- **pacs-workflow:** PACS (Picture Archiving and Communication System) workflow
- **pubmed-search:** Literature search for radiology research
- **dicom-web-query:** DICOM web queries for image retrieval

### AI Assistants (4 skills)
- **ai-report-assist:** AI-assisted radiology reporting
- **ai-detection-pipeline:** AI detection pipeline for abnormalities
- **llm-radiology-use:** LLM use cases in radiology
- **ai-quality-review:** AI quality review of radiology reports

### Analytics Quality (3 skills)
- **radiology-metrics:** Radiology department metrics
- **image-quality-audit:** Image quality auditing
- **report-quality-review:** Report quality review

### Research Evidence (3 skills)
- **guideline-integration:** Clinical guideline integration
- **cross-reference-linking:** Cross-reference linking for research
- **radiology-research:** Radiology research support

### Dataset (3 skills)
- **radiology-dataset-guide:** Guide to radiology datasets
- **dataset-preprocessing:** Dataset preprocessing for ML
- **model-validation:** Model validation for radiology AI

## Integration Targets

### PACS Systems
- Orthanc, Dcm4chee, OHIF Viewer

### AI Detection
- Aidoc, NVIDIA Clara, Zebra Medical, MaxQ AI, Qure.ai

### AI Reporting
- RadAI

### LLM Platforms
- MedPaLM API, Google Health, Amazon Healthlake

### EHR Systems
- Epic Radiant, Cerner Powerchart

### Datasets
- RSNA Data, NIH ChestX-ray14, PhysioNet MIMIC, CheXpert, LUNA16, BRATS

## CLI Tools (12)
- dicom_qido.py — DICOM query
- pubmed_search.py — Literature search
- + 10 more specialized tools

## Usage Guidelines
1. Always correlate imaging findings with clinical presentation
2. Flag urgent findings (critical results) immediately
3. Use structured reporting for consistency
4. Maintain patient privacy (HIPAA compliance)
5. Document all AI-assisted findings
