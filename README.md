# CareerTamer

An exclusive AI career agent that helps you tame your career path: match yourself
against job descriptions, plan your skill roadmap, run mock interviews, log daily
progress, and kick off each day with a dashboard. Powered by the Claude API.

The full persona and module spec live in [`system_prompt.py`](system_prompt.py) —
that's the contract Claude follows for every command below.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in ANTHROPIC_API_KEY
python careertamer.py
```

On first run, CareerTamer asks for your resume summary/skill tree and short-term
goal, and saves them as your Career Profile in `data/career_profile.json`.

## Commands

| Command | Module | What it does |
|---|---|---|
| *(paste a JD or job link)* | 職缺配對 Job Matcher | Match rate %, strengths/gaps/red flags, resume tweaks |
| `/path` | 發展路線規劃 Evolution Tree | Short/mid/long-term skill roadmap |
| `/interview [role or topic]` | 面試戰鬥測驗 Boss Fight | One question at a time, graded out of 10 |
| `/log [what you did today]` | 職涯日誌紀錄 Quest Log | Formats a Markdown daily update and saves it to `data/quest_log.md` |
| `/daily` | 每日啟動與提醒 Daily Sync | Dashboard: main goal, yesterday's progress, today's action, a push |
| `/help` | — | Show available commands |
| `/exit` | — | Quit |

## How state persists

- **Career Profile** (`data/career_profile.json`) is created once during
  initialization and sent as context with every message.
- **Quest Log** (`data/quest_log.md`) accumulates one dated section per `/log`
  entry. `/daily` reads the most recent entry to recall "yesterday's progress,"
  so your dashboard stays accurate across separate CLI sessions.

Both files are gitignored — they're your personal data, not project source.
