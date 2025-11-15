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


## Install required Python packages
   ```bash
   pip install tkinter openai pydantic markdown
   ```

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

## 📦 Setup for CLI only app

1. **Start your local LLM server**  
   Example with `llama.cpp`:
   ```bash
   ./llama-server.exe -m your-model.gguf --port 8080
   ```
   Ensure it’s accessible at `http://localhost:8080/v1`.

2. **Download AClib.py**  
   ```bash
   from this repo
   ```

3. **Install dependencies**  
   ```bash
   pip install openai pydantic markdown
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



---


# 📘 Tutorial: Building a Desktop Article Analyzer App with Python & Local AI
#### The entire tkinter GUI app

---

## 🎯 What This App Does

This tutorial explains a **desktop application** built with Python that helps you:

- **Paste a long article or text**
- **Automatically analyze it using a local AI model** (no internet needed!)
- Get back:
  - A clear **summary**
  - A structured **Table of Contents**
  - The **top 5 keywords** with explanations
- **Email the full report** to yourself (or anyone)
- **Open a nicely formatted report** on your computer

All processing happens on **your own machine**, using a local AI server (like `llama.cpp`). Your data never leaves your computer!

---

## 🧩 How It’s Built: Two Main Files

Your project has two Python files:

1. **`AClib.py`** → Contains all the "smart" functions (AI analysis, email sending, etc.)
2. **`gui_app.py`** → The visual app window you interact with (built with **Tkinter**)

> ✅ **You already understand `AClib.py`** – so this tutorial focuses on **how the GUI (`gui_app.py`) works** and **how to use it**.

---

## 🖥️ Part 1: Understanding the GUI App (`gui_app.py`)

### 🔧 Setup & Configuration

At the top of `gui_app.py`, you’ll see some settings:

```python
SENDER_EMAIL = "youemail@gmail.com"
SENDER_PASSWORD = "abcd efgh ijkl mnop"  # Gmail App Password!
RECEIVER_EMAIL = "someoneelse@email.com"
```

> ❗ **Important**:  
> - Use a **Gmail App Password** (not your regular password).  
> - Enable 2FA in Gmail, then generate a 16-digit app password [here](https://myaccount.google.com/apppasswords).

It also connects to your **local AI server**:

```python
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)
```

> 💡 This assumes you’re running a local LLM server (like `llama.cpp` with OpenAI-compatible API) on port `8080`.  
> If you use a different port, change `8080` accordingly.

---

### 🪟 The Window Layout

The app window has:

1. **Input box** – Where you paste your article text  
   (big scrollable area)
2. **Two buttons**:
   - **"Analyze & Email Report"** → Starts the magic!
   - **"Quit"** → Closes the app
3. **Progress bar** – Shows how far along the analysis is
4. **Timer** – Counts how long the analysis takes
5. **Status message** – Tells you what’s happening (e.g., “Generating summary…”)

All this is built using **Tkinter**, Python’s built-in GUI toolkit.

---

### ▶️ What Happens When You Click “Analyze”?

1. **Checks if text is pasted**  
   → If empty, shows a warning.

2. **Locks the button**  
   → Prevents double-clicking.

3. **Starts a background process** (using `threading`)  
   → Keeps the app responsive while AI works (which can take time!).

4. **Runs 4 steps in order**:
   - **Step 1**: Ask AI to read & summarize the article
   - **Step 2**: Extract a clean Table of Contents
   - **Step 3**: Pull out 5 key keywords with relevance scores
   - **Step 4**: Format everything into a report → **email it** → **save & open locally**

5. **Updates progress** in real-time  
   → You see exactly what the AI is doing.

6. **When done**:  
   - Opens the report in your default browser/text editor  
   - Shows “✅ Report sent by email & opened locally!”

---

### 📤 How the Report Looks

The final report is a **Markdown (.md) file** – clean and readable:

```markdown
# 📊 Article Analysis Report

## 📝 Summary
[Short plain-English summary here]

## 🗂️ Table of Contents
- **Introduction**
  → Explains the problem being addressed...
- **Methodology**
  → Describes the experimental setup...

## 🔑 Keywords
1. **Quantum decoherence** (0.92)
   → Central to the paper's argument about stability...
2. **Topological qubits** (0.87)
   → Proposed as a solution to error rates...
...
```

This gets **emailed to you** and **saved temporarily** on your computer.

---

## 🛠️ How to Use This App (Step-by-Step)

### ✅ Prerequisites

1. **Run a local LLM server**  
   Example using `llama.cpp` with OpenAI API support:
   ```bash
   ./server -m models/your-model.gguf --port 8080
   ```
   (Make sure it’s running before starting the app!)

2. **Set up Gmail App Password**  
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Create one for “Mail” → copy the 16-digit code

3. **Install required Python packages**:
   ```bash
   pip install tkinter openai pydantic markdown
   ```

### ▶️ Running the App

1. Open terminal
2. Navigate to your project folder
3. Run:
   ```bash
   python gui_app.py
   ```
4. A window pops up → **paste your article**
5. Click **“Analyze & Email Report”**
6. Wait 10–60 seconds (depends on article length & your PC)
7. Check your email + a report opens on your screen!

---

## 🔒 Privacy & Safety

- ✅ **No data leaves your computer** – AI runs locally
- ✅ **Email only sends the final report** (not your raw input)
- ❌ Never put sensitive/personal info in the article if you’re unsure

---

## 🛠️ Customization Tips

### Change who receives the email:
```python
RECEIVER_EMAIL = "your-email@example.com"
```

### Use a different email provider (e.g., Outlook):
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587  # Note: may need STARTTLS
```
> ⚠️ You’ll need to adjust the `send_markdown_email` function for non-Gmail servers.

### Disable email & just save locally:
Comment out the email line in `run_analysis()`:
```python
# send_markdown_email(...)  # ← comment this
```

---

## ❓ Common Issues & Fixes

| Problem | Solution |
|-------|--------|
| **“Connection refused”** | Make sure your LLM server is running on `localhost:8080` |
| **Email fails** | Double-check app password & Gmail settings |
| **App freezes** | Wait! Large articles take time. Progress bar shows it’s working. |
| **No report opens** | Check the error message – file is still saved (path shown) |

---

## 🌟 Final Thoughts

This app turns your **local AI model** into a **personal research assistant**!  
You can analyze news articles, research papers, meeting notes – all **offline and private**.

And because it’s open-source and built with standard Python tools, you can **modify it** to:
- Add PDF/text file upload
- Save reports to a folder
- Add more AI analysis types (sentiment, entities, etc.)

---

## 📎 Bonus: Want to Try Without Coding?

You can share this app with friends! Just:
1. Package it with `pyinstaller`
2. Give them the executable + instructions to run their own local LLM

> 🌐 Local AI is the future of private, fast, and free text analysis!

---

**Happy analyzing!** 🚀  
*Built with ❤️ using Python, Tkinter, and your own AI brain.*


# 📘 Understanding the Tkinter App: Python Explained Simply

**A gentle walkthrough of `gui_app.py` – no coding expertise needed!**

Think of this app like a friendly robot assistant that lives on your desktop. You talk to it through buttons and text boxes, and it uses AI to analyze your articles. Below, we’ll peek “under the hood” to see how each part works—using plain language and helpful analogies.

---

## 🏗️ 1. Setting Things Up: Imports & Configuration

```python
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import os
import webbrowser
import tempfile
from datetime import datetime
import time

from AClib import (
    genSummary,
    generate_toc,
    extract_keywords,
    send_markdown_email
)
from openai import OpenAI
```

### What’s happening?
- **`tkinter`**: This is Python’s built-in toolbox for making windows, buttons, and text boxes.  
  → `tk` is the main module.  
  → `scrolledtext` gives you a text box with a scroll bar (perfect for long articles!).  
  → `messagebox` shows pop-up alerts (like “Oops! You forgot to paste text.”).  
  → `ttk` adds modern-looking widgets (like the sleek progress bar).

- **`threading`**: Lets the app do two things at once!  
  → While the AI is thinking (which takes time), your app *doesn’t freeze*.  
  → Like ordering coffee while still browsing the menu.

- **`tempfile` & `webbrowser`**: Used to **save your report temporarily** and **open it in your browser**—like auto-opening a PDF after download.

- **`from AClib import ...`**: This is where your app borrows the “smart” functions you already built!  
  → It’s like hiring a team of experts (summary writer, keyword finder, email sender) just by saying their names.

---

## 🌐 2. Connecting to Your Local AI

```python
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)
```

### What’s happening?
This tells your app:  
> “Hey! The AI brain is running right here on my computer, at `localhost:8080`.”

- **`localhost`** = your own computer.  
- **`8080`** = the “door number” (port) where your AI server is listening.  
- **`api_key="not-needed"`** = since it’s local, no password is required (unlike cloud APIs).

💡 If you change the port in your `llama.cpp` server, update this number too!

---

## 🎨 3. Building the Window: `__init__` Method

```python
class ArticleAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        root.title("📝 Article Analyzer (Local LLM)")
        root.geometry("850x600")
        ...
```

### What’s happening?
This is the **blueprint for your app window**.

- **`class ArticleAnalyzerGUI`**: A “recipe” for creating the app. Every time you run it, it follows this recipe.
- **`self.root = root`**: `root` is the main window. We save it so we can change it later (like updating buttons).
- **`root.title(...)`**: Sets the window name (what you see at the top).
- **`root.geometry(...)`**: Sets the window size—850 pixels wide, 600 tall.

Then, it adds:
- A **label** (“Paste your article text below”)
- A **big text box** (`scrolledtext.ScrolledText`) where you paste your article
- **Buttons** (“Analyze” and “Quit”) in a row (`btn_frame`)
- A **progress bar** (shows how much is done)
- A **timer** (“Elapsed: 5.2s”)
- A **status message** (“Generating summary…”)

All these pieces are **“packed”** into the window—like placing furniture in a room.

---

## ▶️ 4. Starting the Analysis: `start_analysis()` Method

```python
def start_analysis(self):
    article = self.input_text.get("1.0", tk.END).strip()
    if not article:
        messagebox.showwarning("Empty Input", "Please paste an article first.")
        return
    ...
```

### What’s happening?
This runs **when you click “Analyze”**.

- **`self.input_text.get("1.0", tk.END)`**: Grabs all text from the input box.  
  → `"1.0"` means “start at line 1, character 0”.  
  → `tk.END` means “go to the very end”.
- **`.strip()`**: Removes extra blank spaces at the start/end.
- If the article is empty → show a warning and **stop**.

Then:
- It **resets the progress bar and timer**
- **Disables the button** (so you can’t click it twice)
- **Starts a timer** (`update_timer()`)
- **Launches the analysis in the background** using `threading.Thread(...)`

> 🧵 **Why threading?**  
> Without it, the whole app would freeze while waiting for AI. With threading, the window stays responsive—you can even move it around!

---

## ⏱️ 5. Keeping Time: `update_timer()` Method

```python
def update_timer(self):
    if self.analysis_active:
        elapsed = time.time() - self.analysis_start_time
        self.time_var.set(f"Elapsed: {elapsed:.1f}s")
        self.root.after(100, self.update_timer)
```

### What’s happening?
This is a **mini clock** that ticks every 0.1 seconds.

- **`self.root.after(100, ...)`**: “In 100 milliseconds, run this function again.”  
  → This creates a smooth, updating timer—like a stopwatch!
- **`self.time_var.set(...)`**: Updates the text you see (“Elapsed: 3.4s”)

It only runs while analysis is active (`self.analysis_active = True`).

---

## 🔄 6. Showing Progress: `update_status_and_progress()`

```python
def update_status_and_progress(self, step, total_steps, message):
    self.progress['value'] = (step / total_steps) * 100
    self.status_var.set(message)
    self.root.update_idletasks()
```

### What’s happening?
This **refreshes the progress bar and status message** during analysis.

- **`self.progress['value'] = ...`**: Fills the bar (e.g., 2/4 steps → 50% full)
- **`self.status_var.set(...)`**: Changes the big bold message (“Step 2/4: Generating Table of Contents…”)
- **`self.root.update_idletasks()`**: Forces the window to **redraw immediately**  
  → Without this, you’d only see updates *after* the whole analysis finishes!

---

## 🤖 7. The Brain: `run_analysis()` Method

```python
def run_analysis(self, article):
    total_steps = 4
    try:
        final_markdown = "# 📊 Article Analysis Report\n\n"

        # ➤ STEP 1: Summary
        self.update_status_and_progress(1, total_steps, "Step 1/4: Generating summary...")
        summary = genSummary(client, article)
        final_markdown += f"## 📝 Summary\n\n{summary}\n\n"
        ...
```

### What’s happening?
This is the **core workflow**—the app’s “to-do list”:

1. **Start with a report title** (`# 📊 Article Analysis Report`)
2. **Step 1**: Call `genSummary()` → add result to report
3. **Step 2**: Call `generate_toc()` → format as bullet points
4. **Step 3**: Call `extract_keywords()` → list with relevance scores
5. **Step 4**:  
   - **Email the report** using `send_markdown_email()`  
   - **Save it locally** using `tempfile.NamedTemporaryFile()`  
     → Creates a real `.md` file on your computer (e.g., `/tmp/tmp12345.md`)

> 📝 **Why `tempfile`?**  
> It automatically picks a safe, unique filename so you don’t overwrite old reports.

All of this runs in the **background thread**, so your window stays smooth.

---

## 🎉 8. Wrapping Up: `show_completion()` & `reset_ui()`

```python
def show_completion(self, md_path):
    self.reset_ui()
    ...
    webbrowser.open(f"file://{md_path}")
```

### What’s happening?
When analysis finishes:

- **`reset_ui()`**: Re-enables the button, resets status → app is ready again!
- **`webbrowser.open(...)`**: Opens the report in your default browser  
  → On Windows, `os.startfile()` does the same (opens in default app)

If opening fails (rare), it shows a warning with the file path—so you can find it manually.

---

## 🧠 Key Concept Recap

| Concept | Why It Matters |
|-------|---------------|
| **`threading`** | Keeps the app responsive during slow AI work |
| **`self.root.after()`** | Updates timer/status without freezing |
| **`update_idletasks()`** | Forces instant screen refresh |
| **`tempfile`** | Safely saves reports without cluttering your folders |
| **`class` and `self`** | Lets different parts of the app “talk” to each other (e.g., button tells progress bar to update) |

---

## 💡 Tkinter tweaks!

Even if you don’t write GUI code every day, you now understand:
- How the window is built
- How buttons trigger smart actions
- How the app stays smooth while doing heavy work
- How your local AI powers everything—privately and offline

And best of all: **you can tweak it!**  
Want a bigger text box? Change `height=10` → `height=15`.  
Want to skip email? Comment out the `send_markdown_email` line.

Your desktop AI assistant—fully under your control. 🛠️✨
