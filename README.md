# NovaAgent - LiveKit Voice Agent with local LLM Planning

NovaAgent is a voice-interactive agent that leverages LiveKit for real-time audio, Ollama for local LLM processing, and a custom Planning Loop to handle complex, multi-step requests using tools.

## Features
- **Voice-to-Voice**: Low-latency audio pipeline using Silero VAD and ai-coustics noise cancellation.
- **Local LLM**: Powered by Ollama (defaults to llama3).
- **Planner Loop**: Generates a numbered execution plan, runs tools, and synthesizes the final response.
- **Custom Tools**: Integrated calculator and DuckDuckGo web search.
- **Polished Web UI**: Custom frontend with state-aware animations and live transcripts.

## Requirements
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)
- [Ollama](https://ollama.ai/) (installed and running)
- A [LiveKit Cloud](https://livekit.io/) project

## Setup

1. **Install Ollama & Model**:
   ```bash
   ollama serve
   ollama run llama3
   ```

2. **Clone and Install Dependencies**:
   ```bash
   git clone <repo-url>
   cd Nova-Agent
   uv sync
   ```

3. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your LiveKit Cloud credentials
   ```

## Run Order

1. **Start the Token Server**:
   ```bash
   python token_server.py
   ```
   (Runs on `http://localhost:8000`)

2. **Start the Agent Worker**:
   ```bash
   python agent.py dev
   ```

3. **Open the Frontend**:
   Open `web/index.html` in your browser.

## Project Structure
- `agent.py`: LiveKit `AgentSession` entrypoint.
- `planner.py`: The Plan-Execute-Observe loop logic.
- `tools.py`: Tool definitions (Calculator, Web Search).
- `config.py`: Environment variable loader.
- `token_server.py`: FastAPI token server for frontend access.
- `web/index.html`: Custom JS/HTML voice interface.

## Troubleshooting
| Issue | Solution |
| :--- | :--- |
| Mic permission denied | Ensure you are using HTTPS or localhost and allowed mic access. |
| Agent not responding | Check if `ollama serve` is running and `DEFAULT_MODEL` matches your downloaded model. |
| Connection error | Verify `LIVEKIT_URL` in `.env` matches your LiveKit Cloud project. |

## Deployment Note
This agent requires a persistent worker process and a local Ollama instance. It cannot be deployed to serverless platforms like Vercel. LiveKit Cloud is the recommended host for the worker process in production.
