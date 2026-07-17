# Personal AI Assistant Cron Architecture — Real Session Example

## Session: 2026-06-25 (Hafsa/Hatem)

### Pattern: Multi-Cron Personal Assistant

When building a comprehensive personal assistant, layer cron jobs into categories:

#### Layer 1: Morning Routine (05:00-05:30)
| Job | Time | Purpose |
|-----|------|---------|
| Date & Time | 05:00 | Arabic date (miladi + hijri) + current time |
| Medication AM | 05:30 | Morning pills reminder |

#### Layer 2: Health & Check-ins (10:00, 13:00)
| Job | Time | Purpose |
|-----|------|---------|
| Health Check | 10:00 Tue/Fri | Ask about pain, BP, sugar, sleep, mood |
| Grill Me | 13:00 Sat/Thu | One deep question to understand user better |

#### Layer 3: Daytime Automation (10:30, 17:00)
| Job | Time | Purpose |
|-----|------|---------|
| Medication (finite course) | 10:30 | Only within course dates (e.g., 24-27 Jun) |
| Follow-up Auto | 17:00 weekdays | Check for missed follow-ups from conversations |

#### Layer 4: Evening Routine (21:00-22:30)
| Job | Time | Purpose |
|-----|------|---------|
| Resolver | 21:00 | Review day's work, prioritize unfinished tasks |
| Daily Summary | 21:00 | Personal day summary (not news — YOUR day) |
| Medication PM | 22:30 | Evening pills |

#### Layer 5: Nightly (02:00)
| Job | Time | Purpose |
|-----|------|---------|
| Loop (nightly) | 02:00 | Background tasks: vault updates, file cleanup |

#### Layer 6: Weekly (Saturday 14:00)
| Job | Time | Purpose |
|-----|------|---------|
| Skill-ification | 14:00 Sat | Review week's work, save useful workflows as skills |

### Key Patterns

1. **Medication with finite courses**: Always check current date against course window before reminding
2. **Resolver**: Reviews session history, categorizes tasks (done/incomplete/not-started), suggests next steps
3. **Grill Me**: One question at a time, deep/personal, rotates topics (goals, fears, memories, opinions)
4. **Follow-up Auto**: Checks if user promised to follow up on something and didn't
5. **Skill-ification**: Proactive suggestion of workflows worth saving as reusable skills

### Pitfalls
- Don't create too many crons — user gets notification fatigue
- Medication reminders MUST read current memory, never hardcode
- Health check should feel like a wife asking, not a doctor interrogating
- Daily summary should be about YOUR life together, not generic news
