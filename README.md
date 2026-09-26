# NovaAgent

A real-time voice agent that listens, plans, and executes multi-step tasks — built with LiveKit Agents, a local LLM via Ollama, and a custom web interface.

Unlike a simple voice-to-text-to-voice pipeline, NovaAgent breaks your request into steps, calls tools (calculator, web search) to complete them, and speaks back a final answer — with the plan and each step visible in the UI as it happens.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![LiveKit](https://img.shields.io/badge/livekit-agents-blueviolet)
![Ollama](https://img.shields.io/badge/ollama-local%20LLM-black)

---

## Features

- **Real-time voice conversation** — powered by LiveKit's WebRTC infrastructure
- **Agentic planning** — the LLM breaks multi-step requests into a plan, executes each step, and adapts if something fails
- **Tool use** — calculator and free web search (DuckDuckGo), callable mid-conversation
- **Local reasoning** — LLM runs via Ollama, no per-token API cost
- **Noise cancellation** — real-time audio enhancement via the `ai-coustics` LiveKit plugin
- **Custom web UI** — clean, minimal interface with live transcript and step-by-step plan visibility
- **Visual state feedback** — idle → listening → thinking/planning → speaking, always clear what's happening

---

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — Python package/project manager
- [Ollama](https://ollama.com) installed locally, with a model pulled (e.g. `ollama pull gemma3:1b`)
- A free [LiveKit Cloud](https://cloud.livekit.io) account and project

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/adiihere-ai/Nova-VoiceAgent.git
cd Nova-VoiceAgent
```

**2. Create the virtual environment and install dependencies**
```bash
uv venv
.venv\Scripts\activate       # Windows
# source .venv/bin/activate  # macOS / Linux

uv add livekit-agents livekit-plugins-ai-coustics livekit-plugins-openai livekit-plugins-silero python-dotenv fastapi uvicorn
```

**3. Create a LiveKit Cloud project**
- Sign up / log in at [cloud.livekit.io](https://cloud.livekit.io)
- Create a project and copy its `URL`, `API Key`, and `API Secret`

**4. Configure environment variables**
```bash
cp .env.example .env
```
Fill in `.env`:
```
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
OLLAMA_HOST=http://localhost:11434/v1
DEFAULT_MODEL=gemma3:1b
OPENAI_API_KEY=ollama
```
`OPENAI_API_KEY` can be any placeholder string — it's only there because the LLM client library expects a non-empty key, even though requests are routed to your local Ollama server, not OpenAI.

**5. Pull your model and start Ollama**
```bash
ollama pull gemma3:1b
ollama serve
```

---

## Running it

Start each of these in its own terminal, in order:

**Terminal 1 — Ollama** (if not already running)
```bash
ollama serve
```

**Terminal 2 — Token server**
```bash
python token_server.py
```
Wait for: `Uvicorn running on http://0.0.0.0:8000`

**Terminal 3 — Agent worker**
```bash
python agent.py dev
```

**Terminal 4 — Web page**
```bash
cd web
python -m http.server 5500
```
Then open **`http://localhost:5500/index.html`** in your browser.

> Important: open the page via `http://localhost:5500`, not by double-clicking the file. Browsers block microphone access and local requests on `file://` URLs.

Click the mic and start talking.

---

## Project structure

```
Nova-VoiceAgent/
├── agent.py              # LiveKit AgentSession entrypoint (VAD, noise cancellation, LLM, STT, TTS)
├── planner.py             # Plan → execute → observe loop
├── tools.py                # Calculator and web search tools
├── config.py                # Loads settings from .env
├── token_server.py           # FastAPI server that mints LiveKit access tokens
├── web/
│   └── index.html              # Custom web interface (LiveKit JS client)
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

---

## How it works

1. You speak — audio is captured and cleaned up by the `ai-coustics` noise cancellation plugin
2. Speech-to-text transcribes your request
3. The LLM (local, via Ollama) writes a short numbered plan for multi-step requests
4. Each step executes — calling the calculator or web search tool as needed — with results fed back to the LLM
5. The LLM composes a final answer, which is spoken back to you via text-to-speech
6. The plan and each step's outcome are shown in the UI as it happens

---

## Troubleshooting

| Problem | Fix |
|---|---|
| "Failed to connect to NovaAgent" | Confirm the token server is actually running on port 8000, and you opened the page via `http://localhost:5500`, not `file://` |
| `Errno 10048` / port already in use | Find and kill the stuck process: `netstat -ano \| findstr :8000` then `taskkill /PID <pid> /F` |
| Agent worker crashes with an asyncio/event loop error | Make sure `agent.py` doesn't wrap its entrypoint in `asyncio.run()` — the LiveKit CLI manages its own event loop |
| No models found / Ollama connection refused | Run `ollama serve`, confirm your model is pulled with `ollama list` |
| Mic doesn't activate | Check browser mic permissions, and confirm the page is served over `http://localhost`, not opened as a local file |
| LLM responses are shallow or skip planning | Small models (e.g. `gemma3:1b`) can struggle with structured multi-step planning — try a larger model like `llama3.1:8b` if your hardware allows |

---

## Deployment notes

This project is not deployable to Vercel as-is — it depends on:
- A persistent agent worker process (`python agent.py dev`)
- A locally running Ollama instance

Vercel's serverless model doesn't support either of these. For real deployment, the agent worker and token server would need to run on a platform that supports long-running processes — such as a small VPS, Render, Railway, or LiveKit Cloud's own agent hosting — with the LLM either kept local (self-hosted server) or swapped for a hosted API.

For this submission, the project is intended to be run and demoed locally.

---

## License

MIT — do whatever you'd like with it.

---

Built with Python, LiveKit Agents, and Ollama.
