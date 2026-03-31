# 🤖 myPeppy

A personal AI companion with persistent memory, per-user accounts, and emotional insights.

## Stack
- **Frontend** — Streamlit
- **AI** — Claude (Anthropic) for chat, Voyage AI for embeddings
- **Database** — Supabase (PostgreSQL + pgvector + Auth)
- **Hosting** — Streamlit Cloud

---

## One-time Supabase setup

### 1 — Create a Supabase project
Go to [supabase.com](https://supabase.com) → New project → choose a region close to your users.

### 2 — Run the SQL setup
In your Supabase project: **SQL Editor → New query** → paste the contents of `supabase_setup.sql` → **Run**.

This creates the `journal_entries` and `memories` tables, the pgvector index, and the `match_memories` RPC function.

### 3 — Enable OAuth providers
In Supabase: **Authentication → Providers** → enable **Google**, **GitHub**, **Facebook**.

For each provider you need to create an OAuth app and paste in the credentials:

**Google** — [console.cloud.google.com](https://console.cloud.google.com) → APIs & Services → Credentials → Create OAuth client → Web app. Set redirect URI to: `https://your-project.supabase.co/auth/v1/callback`

**GitHub** — [github.com/settings/developers](https://github.com/settings/developers) → New OAuth App. Set callback URL to: `https://your-project.supabase.co/auth/v1/callback`

**Facebook** — [developers.facebook.com](https://developers.facebook.com) → Create App → Facebook Login. Set redirect URI to: `https://your-project.supabase.co/auth/v1/callback`

### 4 — Get your Voyage AI key (free embeddings)
Sign up at [voyageai.com](https://www.voyageai.com) → API Keys → copy your key.

---

## Deploy to Streamlit Cloud

### Secrets to add in Streamlit Cloud → Settings → Secrets:
```toml
ANTHROPIC_API_KEY  = "sk-ant-..."
VOYAGE_API_KEY     = "pa-..."
SUPABASE_URL       = "https://your-project.supabase.co"
SUPABASE_ANON_KEY  = "your-anon-key"
APP_URL            = "https://bypeppy.streamlit.app"
```

Find `SUPABASE_URL` and `SUPABASE_ANON_KEY` in your Supabase project under **Settings → API**.

---

## Project structure

```
├── main.py                       # Entry point + auth gate
├── auth.py                       # Login/signup (Google, GitHub, Facebook, email)
├── supabase_client.py            # Shared Supabase connection
├── supabase_setup.sql            # Run once in Supabase SQL editor
├── requirements.txt
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml              # Local only — never commit
├── agents/
│   ├── conversation_agent.py
│   ├── emotion_agent.py
│   ├── reasoning_agent.py        # Claude API
│   ├── planning_agent.py
│   ├── insight_agent.py
│   └── voice_agent.py            # Local use only
├── memory/
│   ├── journal_db.py             # Supabase journal_entries table
│   └── memory_db.py              # Supabase memories table + pgvector
└── dashboard/
    └── views.py
```
