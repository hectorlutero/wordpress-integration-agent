# WordPress Integration Agent - Implementation Plan

## 1. Architecture Strategy
The agent will use a **Skill-Based Architecture**. Each functionality (Posts, ACF, Analytics) will be an isolated "Skill" module orchestrated by a central engine.

## 2. Project Structure
```text
wordpress-agent/
├── .env.example          # Template for credentials
├── .gitignore            # Security: Exclude .env, __pycache__, reports/
├── requirements.txt      # Dependencies: httpx, pydantic-settings, pandas
├── main.py               # CLI Interface
├── core/
│   ├── client.py         # WP REST API wrapper
│   └── config.py         # Pydantic-based settings loader
└── skills/
    ├── posts_skill.py    # WP Posts/Pages CRUD
    ├── acf_skill.py      # ACF field manipulation
    ├── analytics_skill.py# GA4 & MonsterInsights logic
    └── report_skill.py   # CSV export logic
```

## 3. Implementation Phases

### Phase 1: Security & Foundation (COMPLETED)
- [x] Create `.gitignore` to prevent credential leaks.
- [x] Implement `core/config.py` using `pydantic-settings`.
- [x] Create `core/client.py` for authenticated WP REST API calls.
- [x] Create `.env.example` template.

### Phase 2: Content & ACF Skills (COMPLETED)
- [x] Implement Post fetch/create/update logic.
- [x] Implement ACF field mapping and manipulation.

### Phase 3: Analytics & Reporting
- [ ] Integrate Google Analytics GA4 Data API.
- [ ] Implement CSV export functionality for access/health reports.

### Phase 4: CLI Interface
- [ ] Build the interactive command loop for the agent.
