from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI
from datetime import datetime

# for GMAIL function
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown


MODEL_NAME = "localai"

def readContext():
    """
    Accept multi-line input (perfect for pasting full article text).
    Press Ctrl+D (Unix) or Ctrl+Z (Windows) + Enter to finish.
    """
    print("📝 Paste the article text below. Press Ctrl+D (or Ctrl+Z) when done:\n")
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass
    return '\n'.join(lines)


# FUNCTIONS FOR STRUCTURED OUTPUT LLM CALLS
###############################################################################
def extract_keywords(client, article_text):
    # DEFINE PYDANTIC SCHEME
    class KeywordItem(BaseModel):
        word: str = Field(..., description="The actual keyword or phrase")
        relevance: float = Field(..., ge=0.0, le=1.0, description="How central this concept is to the article (0.0 to 1.0)")
        reason: str = Field(..., description="One-sentence explanation of why this keyword matters")
    class KeywordExtraction(BaseModel):
        keywords: List[KeywordItem] = Field(..., description="Top 5 most meaningful keywords")
    
    # RUN THE STRUCTURED LLM CALL
    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a semantic analyst. Identify the 5 most important conceptual keywords in the article. Focus on novelty, centrality, and technical significance."},
                {"role": "user", "content": f"""
Analyze the following article and extract exactly 5 keywords that capture its core ideas.

Rules:
- Prioritize technical terms, novel concepts, and recurring themes.
- Avoid generic words like 'AI', 'system', 'approach'.
- Each keyword must be justified by its role in the article.
- The 'relevance' score must be a decimal number (float) between 0.0 and 1.0.
- Return only valid JSON matching the schema.

[Start of Article]
{article_text}
[End of Article]
"""}
            ],
            response_format=KeywordExtraction,
            temperature=0.3
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print("Failed to extract keywords:", e)
        return None

    
def generate_toc(client,article_text: str):
    # DEFINE PYDANTIC SCHEME
    class TocItem(BaseModel):
        title: str = Field(..., description="The exact heading text")
        key_idea: str = Field(..., description="One-sentence summary of what this section is really about")
    class TableOfContents(BaseModel):
        items: List[TocItem] = Field(..., description="List of all sections in order")
    
    # RUN THE STRUCTURED LLM CALL
    try:
        completion = client.beta.chat.completions.parse(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a precision editor. Extract the logical structure of the article and return ONLY a well-formed TableOfContents."},
                {"role": "user", "content": f"""
Analyze the following article and generate a clear, hierarchical Table of Contents.

Rules:
- Report only the main sections.
- Titles must reflect actual content, not generic labels.
- Each key idea must capture the essence in plain English.
- Return nothing but valid JSON matching the schema.

[Start of Article]
{article_text}
[End of Article]
"""}
            ],
            response_format=TableOfContents
        )
        return completion.choices[0].message.parsed
    except Exception as e:
        print("Failed to generate TOC:", e)
        return None

# FUNCTIONS FOR STANDARD LLAMA.CPP LLM CALLS
###############################################################################
def genOS_chat(client, user_prompt, history):
    """
    Sends a prompt to OpenRouter and appends the response to chat history.
    Prints the AI's reply and returns updated history.
    """
    STOPS = ['<|im_end|>']
    history.append({"role": "user", "content": user_prompt})
    
    completion = client.chat.completions.create(
        model="localai", # this field is currently unused
        messages=history,
        temperature=0.3,
        frequency_penalty  = 1.45,
        max_tokens = 1200,
        stop=STOPS
    )
    response = completion.choices[0].message.content
    print(response)
    history.append({"role": "assistant", "content": response})
    return history

# Function for Generatring meaningful summary
def genSummary(client,context):
    # 🚀 MAIN PIPELINE
    history = []  # Start fresh

    # Step 1: Tell the AI to read and confirm
    p1 = f"""
    Read the following article carefully. When you're done, say "I am ready".

    [Start of article]
    {context}
    [End of article]
    """
    print("\n🤖 AI is reading the article...\n")
    history = genOS_chat(client, p1, history)

    # Step 3: Ask for the summary
    p2 = """
    Now, write a short, clear summary in plain English — no jargon.

    Then, list exactly 3 key points.

    Finally, tell me: does the author have a critique or unique angle? What’s their stance?
    """
    print("\n🤖 AI is generating the summary...\n")
    history = genOS_chat(client, p2, history)
    return history[-1]["content"]


# FUNCTIONS TO SEND EMAILS
###############################################################################
def convert_markdown_to_html(markdown_text):
    """Converts Markdown to HTML with syntax highlighting and tables."""
    return markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])

def send_markdown_email(
    sender_email, 
    sender_password, 
    receiver_email, 
    subject, 
    markdown_content, 
    smtp_server="smtp.gmail.com", 
    smtp_port=465
):
    """
    Sends a beautifully formatted email using Markdown + HTML.
    Works with Yahoo, Gmail, Outlook — just change the SMTP settings.
    """
    # Convert Markdown to HTML
    html_content = convert_markdown_to_html(markdown_content)
    
    # Create message container
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Attach plain text and HTML versions
    part1 = MIMEText(markdown_content, "plain")  # Fallback
    part2 = MIMEText(html_content, "html")      # Pretty version
    msg.attach(part1)
    msg.attach(part2)

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            #server.starttls()  # Secure connection
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")