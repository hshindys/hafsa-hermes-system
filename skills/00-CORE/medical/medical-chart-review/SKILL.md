---
name: medical-chart-review
description: >
  MUST USE when reviewing medical charts, auditing clinical records, or when user
  mentions HEDIS, HCC coding, risk adjustment, or clinical documentation improvement.
  
  Covers 7 skills:
  - chart-review: Comprehensive medical chart review
  - hedis-nlp: HEDIS quality measure extraction via NLP
  - hcc-nlp: Hierarchical Condition Category coding via NLP
  - hipaa-compliance: HIPAA Privacy, Security, Breach Notification
  - claims-ml-audit: Machine learning audit of insurance claims
  - healthcare-code-systems: ICD-10, CPT, SNOMED, LOINC, RxNorm
  - fhir-r4-implementation: FHIR R4 interoperability
  
  NOT for: direct patient care, prescribing, diagnosis.
metadata:
  hermes:
    tags: [medical, chart-review, HEDIS, HCC, HIPAA, coding, clinical]
    priority: high
---

# Medical Chart Review Skills

## Overview
7 skills for comprehensive medical chart review, quality reporting, and compliance.

## Skills

### 1. Chart Review
- Comprehensive medical chart review
- Clinical documentation improvement (CDI)
- Quality metrics extraction

### 2. HEDIS NLP
- HEDIS quality measure extraction via NLP
- Automated quality reporting
- Gap identification

### 3. HCC NLP
- Hierarchical Condition Category coding via NLP
- Risk adjustment factor calculation
- Documentation accuracy scoring

### 4. HIPAA Compliance
- HIPAA Privacy Rule compliance
- Security Rule implementation
- Breach notification procedures
- BAA (Business Associate Agreement) review
- De-identification methods
- OCR audit preparation

### 5. Claims ML Audit
- Machine learning audit of insurance claims
- Fraud detection patterns
- Billing accuracy verification

### 6. Healthcare Code Systems
- ICD-10-CM/PCS coding
- CPT procedure coding
- SNOMED CT clinical terminology
- LOINC laboratory codes
- RxNorm medication codes

### 7. FHIR R4 Implementation
- FHIR R4 resource modeling
- Interoperability testing
- API integration

## Usage Guidelines
1. Always use `redacta` before processing clinical text
2. Flag urgent findings immediately
3. Document all review findings
4. Recommend specialist consultation for complex cases
5. Maintain HIPAA compliance at all times
