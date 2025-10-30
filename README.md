# 🧠 LifeAsCarers Agentic AI  
**Automated Research Summarization & Blog Generation Pipeline**

---

## 🌍 Overview
The **LifeAsCarers Agentic AI** system is an autonomous research summarization agent designed to translate the latest dementia-related caregiving studies into accessible, empathetic blog content for the [LifeAsCarers](https://lifeascarers.com) project.

Every week, the agent:
1. Queries the **Dimensions API** for new open-access caregiving papers.  
2. Summarizes them in a warm, reflective tone using a local **Ollama LLM (Mistral)** model.  
3. Outputs Markdown blog drafts with metadata and structure ready for publication.  
4. (Optional) Posts drafts directly to a connected WordPress site via REST API.

The goal is to bridge **academic research** and **everyday caregiving insight**—automating the discovery and translation process while maintaining human warmth and editorial review.

---

## 🧩 Architecture

| Component | Role | Tech Stack |
|------------|------|------------|
| **Agent Container** | Fetches research, runs LLM summarization, and writes blog posts | Python 3.11 · LangChain · Requests · JSON · Markdown |
| **Ollama Container** | Local inference server running the Mistral model | Ollama (`mistral:latest`) |
| **OpenWebUI** | Optional local chat interface to inspect and debug the model | OpenWebUI |
| **Docker Compose** | Orchestrates all services with shared networking and data volume | Docker Engine on Windows/Linux/macOS |
| **Task Scheduler (Windows)** | Runs the agent weekly to generate new posts | Windows Task Scheduler |

---

## ⚙️ Project Structure

```
agentic-ai/
│
├── agent/                      # Core Python app
│   ├── agentic_pipeline.py     # Main agent workflow
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Builds the agent container
│
├── data/                       # Output folder for summaries and markdown posts
│   ├── posts/                  # Individual blog posts (.md)
│   └── summaries.json          # JSON log of generated content
│
├── .env                        # API keys and environment variables (not tracked)
├── .gitignore                  # Ignores sensitive files and Docker junk
├── docker-compose.yml           # Multi-service orchestration
└── README.md                   # You are here 🚀
```

---

## 🚀 Quick Start

### 1️⃣ Clone the repository
```bash
git clone git@github.com:KevinHanson/lifeascarers-agent.git
cd lifeascarers-agent
```

### 2️⃣ Create your `.env` file
```bash
DIMENSIONS_API_KEY=your_dimensions_api_key_here
OLLAMA_API_URL=http://ollama:11434
```

### 3️⃣ Start the full stack
```bash
docker compose up -d --build
```

This launches:
- **Ollama** (LLM inference server)  
- **OpenWebUI** (optional chat frontend)  
- **AI Agent** (fetch + summarize loop)

---

## 🧠 Agent Workflow

1. **Fetch Data:**  
   The agent authenticates with the Dimensions API using your key and retrieves newly published dementia-caregiving research.

2. **Summarize Findings:**  
   Each paper is summarized through the Mistral model via LangChain and formatted in the **LifeAsCarers** tone:
   - Relatable introduction  
   - Research summary  
   - Practical caregiving reflection  
   - Bold, positive takeaway  

3. **Generate Output:**  
   Markdown blog posts with YAML front matter are saved to `/data/posts`, along with a JSON index file for tracking.

4. **(Optional) Publish:**  
   The agent can use the WordPress REST API to automatically create draft posts on your blog for human review.

---

## 🗓️ Automation

For Windows, schedule weekly execution via **Task Scheduler**:

| Setting | Value |
|----------|--------|
| **Action** | `docker exec -it ai-agent python /app/agentic_pipeline.py` |
| **Trigger** | Weekly – Saturday, 2:00 PM |
| **Condition** | Run whether user is logged in or not |
| **Result** | New draft posts appear in `/data/posts` on Sunday morning |

---

## 🔑 Environment Variables

| Variable | Description |
|-----------|-------------|
| `DIMENSIONS_API_KEY` | API key for the Dimensions research API |
| `OLLAMA_API_URL` | Local Ollama service URL (default: `http://ollama:11434`) |
| `WORDPRESS_URL` | (Optional) WordPress REST endpoint |
| `WORDPRESS_USER` | (Optional) WordPress username |
| `WORDPRESS_APP_PASSWORD` | (Optional) WordPress application password |

---

## 📝 Example Output

```markdown
---
title: "Understanding Mental Health Struggles Among Caregivers of Chronic Illness Patients"
date: 2025-10-28
tags: ["dementia", "caregiving", "research", "lifeascarers"]
author: "LifeAsCarers AI Agent"
---

As a caregiver, you already know that caring for a loved one battling a chronic illness can be emotionally and physically draining.  
...

**Takeaway for Care Partners:**  
**Empower yourself: knowing the potential impact of caregiving intensity on your mental health allows you to take proactive steps.**

---
**Source:** American Journal of Preventive Medicine  
[10.1016/j.amepre.2025.108165](#)
```

---

## 🧰 Development Notes

- **Local testing:**
  ```bash
  docker exec -it ai-agent python /app/agentic_pipeline.py
  ```
- **Check logs:**
  ```bash
  docker logs ai-agent
  ```
- **Inspect network health:**
  ```bash
  docker exec -it ai-agent curl -s http://ollama:11434/api/tags
  ```

---

## 📦 Dependencies

- Python 3.11  
- LangChain + langchain-ollama  
- Requests  
- Docker & Docker Compose  
- Ollama (Mistral)  
- Optional: WordPress REST API

---

## ❤️ Credits
Created and maintained by **[Kevin S. Hanson, Ed.D.](https://kevinhanson.org/)**  
Part of the *LifeAs* ecosystem — empowering caregivers through research, empathy, and technology.

---

## 🧭 License
MIT License © 2025 Kevin S. Hanson  
See [LICENSE](LICENSE) for details.