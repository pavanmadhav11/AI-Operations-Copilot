from app.ai.llm import ask_llm


def generate_pdf_summary(text: str) -> str:
    messages = [
        {
            "role": "system",
            "content": """
You are an expert document analyst.

Generate a concise summary of the uploaded PDF.

Return:
- Overall purpose
- Key points
- Important findings
- Conclusion

Keep it under 300 words.
""",
        },
        {
            "role": "user",
            "content": text[:12000],
        },
    ]

    return ask_llm(messages)