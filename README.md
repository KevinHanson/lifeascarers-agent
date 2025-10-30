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

