from fastapi import FastAPI
from pydantic import BaseModel

from providers.groq_provider import send_to_groq


app = FastAPI()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]


def load_config():
    with open("config.json", "r") as file:
        return __import__("json").load(file)


@app.get("/v1/models")
def models():
    return {
        "object": "list",
        "data": [
            {
                "id": "router-groq",
                "object": "model",
                "owned_by": "ai-router"
            }
        ]
    }


@app.post("/v1/chat/completions")
def chat_completions(request: ChatRequest):
    config = load_config()

    keys = config["groq"]["api_keys"]

    if not keys:
        return {
            "error": {
                "message": "No Groq API key configured."
            }
        }

    user_message = ""

    for message in request.messages:
        if message.role == "user":
            user_message = message.content

    response = send_to_groq(user_message, keys[0])

    return {
        "id": "router-response",
        "object": "chat.completion",
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response
                },
                "finish_reason": "stop"
            }
        ]
    }
