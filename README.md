# automation-chronichles
libraries for [automation chronicles sieries on my Substack](https://thepoorgpuguy.substack.com/t/automation-chronicles)

the python file AMlib.py contains all helper functions for:
- OpenAI-compatible API (via llama.cpp server at localhost:8080)
- Pydantic for structured output (keywords with relevance scores, table of contents)
- Plain chat completions for human-readable summarization
- Markdown-to-HTML email sending via Gmail (or other SMTP)

The workflow is:
- User pastes a long article
- Local LLM extracts:
  - Structured keywords
  - Table of contents
  - Narrative summary with key points and author stance

Results are formatted and emailed


---

# 🧠 Article Analyzer + Emailer (Local LLM Edition)

A lightweight Python tool that uses your **local LLM** (via `llama.cpp` server) to read long articles and automatically generate:

- ✨ A clear, jargon-free **summary**
- 📚 A structured **Table of Contents**
- 🔑 **Key topics** with relevance scores
- 📩 All delivered neatly via **email**

Built for privacy-conscious users who want AI-powered analysis **without sending data to the cloud**.

---

## 🚀 Features

- **100% local processing**: Works with any LLM served via [llama.cpp](https://github.com/ggerganov/llama.cpp) with OpenAI-compatible API (e.g., at `http://localhost:8080/v1`)
- **Structured outputs**: Uses Pydantic + OpenAI’s `response_format` for reliable, parseable results
- **Human-readable summaries**: Focuses on plain language, key insights, and author perspective
- **Email delivery**: Sends beautifully formatted HTML emails (Markdown → HTML) via Gmail or any SMTP provider
- **Easy input**: Paste full articles directly into the terminal (Ctrl+D of Ctrl+Z to submit)

---

## 🛠️ Requirements

- Python 3.9+
- A local LLM running with an **OpenAI-compatible API** (e.g., `llama.cpp` server on `localhost:8080`)
- The following Python packages:

```bash
pip install openai pydantic markdown
```

> 💡 **Note**: Your LLM server must support `/v1/chat/completions` and (for structured output) the `response_format` parameter.

---

## 📦 Setup

1. **Start your local LLM server**  
   Example with `llama.cpp`:
   ```bash
   ./llama-server.exe -m your-model.gguf --port 8080
   ```
   Ensure it’s accessible at `http://localhost:8080/v1`.

2. **Download AIlib.py**  
   ```bash
   from this repo
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt  # (or manually: openai pydantic markdown)
   ```

4. **Follow the articles with tutorial in my Substack**  
   - [The PoorGPUguy  Automation Chronicles](https://thepoorgpuguy.substack.com/t/automation-chronicles) 
   
---

## ▶️ Usage

Run the script:

```bash
python analyze_article.py
```

1. **Paste your article** when prompted (use **Ctrl+D** on Linux/macOS or **Ctrl+Z + Enter** on Windows to finish)
2. The local LLM will:
   - Read the full text
   - Generate summary, TOC, and keywords
3. **Enter your email credentials** when asked
4. Receive a beautifully formatted email with all insights!

> 🔐 All processing happens on your machine—your article never leaves localhost.

---

## 📧 Email Example

The email includes:

- **Summary**: Plain-English overview + 3 key points + author stance  
- **Table of Contents**: Logical section breakdown  
- **Top Keywords**: 5 core concepts with relevance scores (0.0–1.0) and explanations  

Formatted in clean HTML with Markdown styling!

---

## ⚙️ Customization

- **Model name**: Set `MODEL_NAME` in the script (default: `"localai"`)
- **LLM server URL**: Hardcoded to `http://localhost:8080/v1`—adjust the `OpenAI` client base URL if needed:
  ```python
  client = OpenAI(base_url="http://localhost:8080/v1", api_key="sk-no-key-needed")
  ```
- **Email provider**: Change `smtp_server` and `smtp_port` in `send_markdown_email()` for Outlook, Yahoo, etc.

---

## 🛡️ Privacy & Security

- No data is sent to external servers
- Email credentials are only used during runtime (not stored)
- Runs entirely offline once your LLM server is up

---

## 🙌 Inspired By

- [llama.cpp](https://github.com/ggerganov/llama.cpp) – for making local LLMs accessible
- OpenAI’s structured output API – for reliable parsing
- Markdown – for clean, readable output formatting

---

## 📝 License

MIT License – feel free to use, modify, and share!

---

> 💡 **Tip**: Pair this with a fast 1.2B quantized model (e.g., `LFM2-1.2b`, `qwen3-4b-instruct`) for best speed/quality balance on consumer hardware.
