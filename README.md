# 🧪 Local LLM Testcase Generator

A secure, local tool for generating Gherkin test cases using **Ollama** and **Python**.

## 🚀 Quick Start
Double-click the **`run.bat`** file to launch the application.

## 📋 Requirements
- **Ollama**: Must be installed and running.
- **Model**: `llama3.2` (Run `ollama pull llama3.2` if missing).
- **Python**: 3.10 - 3.13 (Verified on 3.13).

## 🛠️ Architecture
```mermaid
graph TD
    User([User]) -->|Inputs Feature| UI[Streamlit UI (app.py)]
    UI -->|Calls| Tool[Python Tool (generate_testcases.py)]
    Tool -->|Prompts| Ollama[Ollama LLM (llama3.2)]
    Ollama -->|JSON Response| Tool
    Tool -->|Structured Data| UI
    UI -->|Renders| Cards[Test Case Cards]
```
- **Layer 1 (Rules)**: `architecture/generation_sop.md`
- **Layer 3 (Tools)**: `tools/generate_testcases.py`
- **Layer 4 (UI)**: `app.py` (Streamlit)

## 🔒 Security
All generation is performed **locally** on your machine. No data is sent to the cloud.
