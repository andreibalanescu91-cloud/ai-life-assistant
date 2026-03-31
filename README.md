# 🤖 AI Life Coach

A personal AI companion that listens, remembers, and helps you grow — built with Streamlit and Claude.

## Features

- **Chat** — Talk to your AI advisor. It detects your emotion, recalls past context, and responds with empathy + an action plan.
- **Memory** — Semantic search across everything you've ever shared.
- **Dashboard** — Visualise your emotional patterns over time.

---

## Project structure

```
├── main.py                      # Streamlit entry point
├── agents/
│   ├── conversation_agent.py    # Orchestrates the full pipeline
│   ├── emotion_agent.py         # Keyword-based emotion detection
│   ├── reasoning_agent.py       # Claude API call (advice + plan)
│   ├── planning_agent.py        # Pass-through wrapper
│   ├── insight_agent.py         # Pattern detection for dashboard
│   └── voice_agent.py           # Whisper voice transcription (optional)
├── memory/
│   ├── journal_db.py            # ChromaDB journal (persistent)
│   └── memory_db.py             # ChromaDB memory store (persistent)
├── dashboard/
│   └── views.py                 # Streamlit dashboard tab
├── requirements.txt
└── .streamlit/
    ├── config.toml              # Theme
    └── secrets.toml             # API keys (local only, never commit)
```

---

## Deploy to Streamlit Cloud (free)

### 1 — Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
gh repo create ai-life-companion --public --push
# or: git remote add origin https://github.com/YOUR_USERNAME/ai-life-companion.git
#     git push -u origin main
```

> Make sure `.gitignore` is present before pushing — it keeps your secrets and chroma_data out of the repo.

### 2 — Create the app on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app**.
3. Select your repository, branch (`main`), and set the main file path to `main.py`.
4. Click **Advanced settings → Secrets** and paste:

```toml
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

5. Click **Deploy**. Your shareable link will appear within ~60 seconds.

---

## Run locally

```bash
pip install -r requirements.txt

# Add your key to .streamlit/secrets.toml (see template)

streamlit run main.py
```

---

## Getting an Anthropic API key

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Go to **API Keys** → **Create Key**
3. Copy the key (starts with `sk-ant-`) and paste it into Streamlit secrets

---

## Notes

- ChromaDB runs in-memory on Streamlit Cloud — data resets on each redeploy. For permanent storage, swap `PersistentClient` for a hosted vector DB (Pinecone, Weaviate, etc.).
- Voice input requires `sounddevice` and a microphone — works locally, not on Streamlit Cloud.