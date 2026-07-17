---
name: internal-medicine-ai-diagnosis
description: >
  MUST USE when discussing clinical diagnosis, differential diagnosis, or when
  user mentions internal medicine AI, diagnostic reasoning, or multimodal diagnosis.
  
  Covers: DxDirector agentic LLM for full-process clinical diagnosis, Multimodal
  AMIE for conversational diagnostic AI with image integration.
  
  Key capabilities:
  - Full-process clinical diagnosis (history → tests → diagnosis)
  - Multimodal reasoning (text + images + documents)
  - State-aware dialogue for history-taking
  - Rare disease diagnosis support
  
  NOT for: surgical planning, emergency medicine, pediatrics (separate skills).
metadata:
  hermes:
    tags: [internal-medicine, clinical-diagnosis, ai-agent, multimodal]
    priority: high
---

# Internal Medicine AI — Clinical Diagnosis

## Core Framework: DxDirector-7B (Nature Communications, 2026)

### What it does
An agentic LLM that autonomously drives the entire clinical diagnosis process — from initial complaint to final diagnosis.

### Key Results
- Superior diagnostic accuracy vs state-of-the-art medical LLMs
- Drastically reduces physician involvement
- Maintains safety framework for high-risk conditions
- Evaluated on rare diseases and complex real-world cases

### Architecture
- Agentic LLM with advanced slow thinking capabilities
- Autonomously determines optimal diagnostic strategies
- Requests physician intervention only for necessary clinical operations
- Iterative reasoning and testing

## Multimodal AMIE (Nature Medicine, 2026)

### What it does
Conversational diagnostic AI that integrates multimodal data (images, ECGs, documents) within a diagnostic conversation.

### Key Results
- Outperformed primary care physicians in 29 of 32 evaluation axes
- Superior in diagnostic accuracy AND conversation quality
- State-aware dialogue framework guides history-taking
- Evaluated in 105 simulated telehealth consultations

### Capabilities
1. **Dermatology** — skin lesion classification from photos
2. **Cardiology** — ECG interpretation
3. **Document Analysis** — lab results, clinical notes integration
4. **Empathy** — maintains patient-centered communication

## Quick Reference

| Task | Model | Performance | Source |
|------|-------|-------------|--------|
| Full clinical diagnosis | DxDirector-7B | Superior to medical LLMs | Nat Commun 2026 |
| Multimodal diagnosis | Multimodal AMIE | Outperforms PCPs | Nature Medicine 2026 |

## Clinical Workflow
1. **Patient Intake** — chief complaint, history of present illness
2. **Iterative Reasoning** — AI asks targeted questions, orders tests
3. **Multimodal Integration** — incorporates images, labs, documents
4. **Differential Diagnosis** — ranked list with confidence scores
5. **Final Diagnosis** — with supporting evidence and recommendations

## Usage Guidelines
1. Always verify AI diagnosis with clinical judgment
2. Flag high-risk conditions requiring immediate attention
3. Use as decision support, not replacement for clinical expertise
4. Document AI reasoning in patient record
5. Maintain patient safety as top priority
