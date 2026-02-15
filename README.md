## Agentic Advisory 

An end-to-end **Agentic AI Advisory System** built with:

- React Frontend
- FastAPI  Backend
- LangGraph Multi-Agent Workflow
- LangSmith Tracing

This project demonstrates how to orchestrate a structured multi-agent AI system capable of planning, researching, writing, critiquing, and refining answers autonomously.

---

## 🏗 Project Structure

### 🧠 Backend Overview

The backend implements a multi-agent workflow using:

- LangChain
- LangGraph
- LangSmith
### 🧠 Frontend Overview
The frontend is a **React-based user interface** that allows users to interact with the Agentic AI system.

Its main purpose is to:

- Accept a user question
- Send the question to the backend API
- Display the generated advisory response
- Show iteration count and (optionally) critique results

---

## 🔁 Agent Workflow

The system follows this execution flow:

1. **Planner Agent**
   - Creates structured plan
   - Defines steps, risks, and output sections
   - Returns structured JSON

2. **Researcher Agent**
   - Produces reasoning-based research notes
   - Covers cost, speed, privacy, reliability, compliance, vendor lock-in, iteration speed, and support

3. **Writer Agent**
   - Generates structured draft
   - Uses plan + research notes
   - Provides actionable recommendation

4. **Critic Agent**
   - Reviews draft
   - Detects missing points, weak reasoning, overconfidence, risky claims
   - Returns structured JSON with a score (0–100)

5. **Finalizer Agent**
   - Produces final polished output
   - Incorporates critique if necessary
   - Returns final answer with confidence score

---

### 🔄 Iterative Improvement Logic

The workflow includes a revision loop:

- If `score < 80` → Writer revises
- If `iteration >= max_iterations` → Finalize
- Otherwise → Finalize

This enables self-improving outputs through critique and refinement.

