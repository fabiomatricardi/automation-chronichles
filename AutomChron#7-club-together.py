from openai import OpenAI
from datetime import datetime
import AClib as ml

# CONSTANTS AND CONFIGURATION
# --- Configuration ---
SENDER_EMAIL = "youremail@gmail.com"  # your gmail email
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx" #"abcd efgh ijkl mnop"  # Your 16-digit app password
RECEIVER_EMAIL = "someone@whatever.com" # it can be the same of the sender...
# GMAIL SMTP settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

# Point to your LOCAL server
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)
MODEL_NAME = "localai"

header = """
############################################################
#         AUTOMATION CHRONICLES - MISSION 7                #
#    Extracting summaries, topics and keywords             #
#     and send an email with google mail                   #
############################################################

"""
print(header)


if __name__ == "__main__":
    # Accept a multi-line string in the terminal
    article = ml.readContext()
    start = datetime.now()

    # EMAIL SUBJECT
    email_subject = f"IDEA: 💡 New automatic report!"
    final_markdown = """"""

    # GENERATION OF THE SUMMARY
    print("\n🧑‍🏫 AI is Generating the summary...\n")
    summary = ml.genSummary(client,article)
    from rich import print
    print("\n✅ Generated SUMMARY:\n")
    print(summary)
    final_markdown += f"# SUMMARY\n\n{summary}\n\n"

    # GENERATION OF THE TABLE OF CONTENTS
    print("\n🧠 AI is building the Table of Contents...\n")
    toc = ml.generate_toc(client,article)
    final_markdown += f"## TABLE OF CONTENTS\n\n"

    if toc:
        print("\n✅ Generated TOC:\n")
        for item in toc.items:
            # prefix = "# " if item.level == 1 else "  ##"
            print(f"{item.title}")
            final_markdown += f"{item.title}\n"
            print(f"     → {item.key_idea}\n")
            final_markdown += f"     → {item.key_idea}\n"
        print('*'*60)
        from rich import print
        final_markdown += "\n\n"
        print(toc)
    
    # GENERATION OF THE KEYWORDS
    print("\n🧠 AI is sniffing out keywords...\n")
    result = ml.extract_keywords(client,article)
    final_markdown += f"## KEYWORDS\n\n"

    if result:
        print("\n✅ Extracted Keywords:\n")
        for i, kw in enumerate(result.keywords, 1):
            print(f"{i}. **{kw.word}** ({kw.relevance:.2f})")
            final_markdown += f"{i}. **{kw.word}** ({kw.relevance:.2f})"
            print(f"   → {kw.reason}\n")
            final_markdown += f"   → {kw.reason}\n"
        print('*' * 50)  
        final_markdown += "\n\n"      
    
    end = datetime.now() -start
    print('*' * 50)
    final_markdown += f'Completed in {end}'
    print(f'Completed in {end}')

    # SENDING FINAL EMAIL
    email_markdown_content = final_markdown
    ml.send_markdown_email(
        SENDER_EMAIL,
        SENDER_PASSWORD,
        RECEIVER_EMAIL,
        email_subject,
        email_markdown_content,
        SMTP_SERVER,
        SMTP_PORT
    )    
    print(final_markdown)