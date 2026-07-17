# Skill Audit Template

Use this when evaluating any new skill from GitHub trending, videos, or other sources.

## Evaluation Card

```markdown
## [SKILL NAME] — [Date]

**Source:** [GitHub URL / Video URL / Recommended by]
**Author:** [Name + credibility indicator]
**Stars:** [count] ([gained this week])
**License:** [MIT/Apache/Other]

### Relevance
- Does it fill a gap? [Yes/No — which gap?]
- Does it duplicate an existing skill? [Yes/No — which one?]
- Is it production-ready? [Yes/No — evidence?]

### Security
- [ ] Read SKILL.md fully
- [ ] Checked for prompt injection vectors
- [ ] Checked for data exfiltration paths
- [ ] Permissions are minimal and justified
- [ ] Passed skill-specter scan (if available)

### Quality Signals
- [ ] Active development (commits in last 30 days)
- [ ] Community engagement (issues, PRs, discussions)
- [ ] Credible author (known in field, or engineer at reputable company)
- [ ] Clear documentation
- [ ] Concrete use case (not just buzzwords)

### Verdict
- [ ] **INTEGRATE** — Add to skills folder
- [ ] **ARCHIVE** — Note for future, not needed now
- [ ] **SKIP** — Red flags or irrelevant

### Placement
Target folder: `~/.hermes/skills/XX-CATEGORY/`
