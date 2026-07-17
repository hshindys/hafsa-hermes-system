# Talent Acquisition / Career

LinkedIn talent/company/job scraping reference.

## LinkedIn

```bash
# Profile
mcporter call 'linkedin-scraper.get_person_profile(linkedin_url: "https://linkedin.com/in/username")'

# People search
mcporter call 'linkedin-scraper.search_people(keyword: "AI engineer", limit: 10)'

# Company profile
mcporter call 'linkedin-scraper.get_company_profile(linkedin_url: "https://linkedin.com/company/xxx")'

# Jobs
mcporter call 'linkedin-scraper.search_jobs(keyword: "software engineer", limit: 10)'
```

> **Login required**: LinkedIn scraper needs an active session.

### Fallback

If MCP is unavailable, use Jina Reader:

```bash
curl -s "https://r.jina.ai/https://linkedin.com/in/username"
```
