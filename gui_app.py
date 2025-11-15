# gui_app.py
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import os
import webbrowser
import tempfile
from datetime import datetime
import time

# Import your logic
from AClib import (
    genSummary,
    generate_toc,
    extract_keywords,
    send_markdown_email
)
from openai import OpenAI

# --- Configuration ---
SENDER_EMAIL = "youemail@gmail.com"
SENDER_PASSWORD = "abcd efgh ijkl mnop" # Your 16-digit app password
RECEIVER_EMAIL = "someoneelse@email.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Point to your LOCAL server
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

class ArticleAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        root.title("📝 Article Analyzer (Local LLM)")
        root.geometry("850x600")

        # Input label
        tk.Label(root, text="Paste your article text below:", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        # Input text area — reduced height
        self.input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, font=("Consolas", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        # Button frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        # Larger buttons
        self.analyze_btn = tk.Button(
            btn_frame,
            text="🔍 Analyze & Email Report",
            command=self.start_analysis,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8
        )
        self.analyze_btn.pack(side=tk.LEFT, padx=10)

        self.quit_btn = tk.Button(
            btn_frame,
            text="❌ Quit",
            command=root.quit,
            bg="#f44336",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=8
        )
        self.quit_btn.pack(side=tk.LEFT, padx=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, mode='determinate', length=600)
        self.progress.pack(pady=10)

        # Elapsed time label
        self.time_var = tk.StringVar()
        self.time_var.set("Elapsed: 0.0s")
        self.time_label = tk.Label(root, textvariable=self.time_var, font=("Arial", 10), fg="gray")
        self.time_label.pack()

        # Status label — big and bold
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to analyze")
        self.status_label = tk.Label(
            root,
            textvariable=self.status_var,
            fg="#1976D2",
            font=("Arial", 14, "bold"),
            wraplength=800,
            justify="center"
        )
        self.status_label.pack(pady=10)

        # Analysis state
        self.analysis_start_time = None
        self.analysis_active = False

    def start_analysis(self):
        article = self.input_text.get("1.0", tk.END).strip()
        if not article:
            messagebox.showwarning("Empty Input", "Please paste an article first.")
            return

        # Reset UI
        self.progress['value'] = 0
        self.time_var.set("Elapsed: 0.0s")
        self.analyze_btn.config(state=tk.DISABLED, text="⏳ Processing...")
        self.status_var.set("Starting analysis...")
        self.analysis_start_time = time.time()
        self.analysis_active = True

        # Start timer update loop
        self.update_timer()

        # Run analysis in background
        thread = threading.Thread(target=self.run_analysis, args=(article,), daemon=True)
        thread.start()

    def update_timer(self):
        if self.analysis_active:
            elapsed = time.time() - self.analysis_start_time
            self.time_var.set(f"Elapsed: {elapsed:.1f}s")
            self.root.after(100, self.update_timer)  # Update every 100ms

    def update_status_and_progress(self, step, total_steps, message):
        # Update progress bar (0–100%)
        self.progress['value'] = (step / total_steps) * 100
        self.status_var.set(message)
        self.root.update_idletasks()

    def run_analysis(self, article):
        total_steps = 4
        try:
            final_markdown = "# 📊 Article Analysis Report\n\n"

            # ➤ STEP 1: Summary
            self.update_status_and_progress(1, total_steps, "Step 1/4: Generating summary...")
            summary = genSummary(client, article)
            final_markdown += f"## 📝 Summary\n\n{summary}\n\n"

            # ➤ STEP 2: Table of Contents
            self.update_status_and_progress(2, total_steps, "Step 2/4: Generating Table of Contents...")
            toc = generate_toc(client, article)
            final_markdown += "## 🗂️ Table of Contents\n\n"
            if toc:
                for item in toc.items:
                    final_markdown += f"- **{item.title}**\n  → {item.key_idea}\n\n"
            else:
                final_markdown += "_Could not generate TOC._\n\n"

            # ➤ STEP 3: Keywords
            self.update_status_and_progress(3, total_steps, "Step 3/4: Extracting keywords...")
            keywords = extract_keywords(client, article)
            final_markdown += "## 🔑 Keywords\n\n"
            if keywords:
                for i, kw in enumerate(keywords.keywords, 1):
                    final_markdown += f"{i}. **{kw.word}** ({kw.relevance:.2f})\n   → {kw.reason}\n\n"
            else:
                final_markdown += "_Could not extract keywords._\n\n"

            # ➤ STEP 4: Email & Finalize
            self.update_status_and_progress(4, total_steps, "Step 4/4: Sending email and preparing report...")
            email_subject = "📄 AI Article Analysis Report"
            send_markdown_email(
                sender_email=SENDER_EMAIL,
                sender_password=SENDER_PASSWORD,
                receiver_email=RECEIVER_EMAIL,
                subject=email_subject,
                markdown_content=final_markdown,
                smtp_server=SMTP_SERVER,
                smtp_port=SMTP_PORT
            )

            # Save report
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
                f.write(final_markdown)
                self.temp_md_path = f.name

            self.root.after(0, self.show_completion, self.temp_md_path)

        except Exception as e:
            error_msg = f"Error during analysis or email:\n{str(e)}"
            print(error_msg)
            self.root.after(0, messagebox.showerror, "❌ Failure", error_msg)
            self.root.after(0, self.reset_ui)

    def show_completion(self, md_path):
        self.reset_ui()
        elapsed = time.time() - self.analysis_start_time
        self.status_var.set("✅ Report sent by email & opened locally!")
        self.time_var.set(f"Total time: {elapsed:.1f}s")
        self.progress['value'] = 100

        try:
            if os.name == 'nt':
                os.startfile(md_path)
            else:
                webbrowser.open(f"file://{md_path}")
        except Exception as e:
            messagebox.showwarning(
                "Viewer Issue",
                f"Report saved and emailed, but couldn't open viewer:\n{e}\n\nFile: {md_path}"
            )

    def reset_ui(self):
        self.analyze_btn.config(state=tk.NORMAL, text="🔍 Analyze & Email Report")
        self.status_var.set("Ready to analyze")
        self.analysis_active = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ArticleAnalyzerGUI(root)
    root.mainloop()
