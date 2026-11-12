from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings

def ask_llm(messages):
    if not settings.GROQ_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="AI chat is unavailable until GROQ_API_KEY is set in the service environment.",
        )

    client = OpenAI(
        api_key=settings.GROQ_API_KEY,
        base_url="https://api.groq.com/openai/v1",
    )
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
    )

    return response.choices[0].message.content
