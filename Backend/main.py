from fastapi import FastAPI
from pydantic import BaseModel
from slack_sdk import WebClient
from dotenv import load_dotenv
from pathlib import Path
import os

# --- Setup ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
app = FastAPI(title="Slack AI Summarizer Agent")

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from .summarize import summarize_messages  # noqa: E402  ensure env is loaded first

client = WebClient(token=SLACK_BOT_TOKEN)

class SummarizeRequest(BaseModel):
    channel_id: str | None = None
    post_to_slack: bool = False

@app.post("/summarize")
def summarize_channel(request: SummarizeRequest):
    channel_id = request.channel_id or SLACK_CHANNEL_ID

    # Fetch messages
    history = client.conversations_history(channel=channel_id, limit=30)
    messages = [msg["text"] for msg in history["messages"] if "text" in msg]

    # Summarize using LangChain
    summary = summarize_messages(messages)

    # Post back to Slack if requested
    if request.post_to_slack:
        client.chat_postMessage(channel=channel_id, text=summary)

    return {"summary": summary}
