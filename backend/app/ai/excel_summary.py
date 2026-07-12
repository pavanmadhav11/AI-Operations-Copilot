from app.ai.llm import ask_llm


def generate_excel_summary(text: str):

    messages = [
        {
            "role": "system",
            "content": """
You are an expert Excel analyst.

Summarize the uploaded workbook.

Include:

• Overall purpose
• Sheets available
• Important columns
• Main observations

Keep the summary under 300 words.
""",
        },
        {
            "role": "user",
            "content": text[:12000],
        },
    ]

    return ask_llm(messages)