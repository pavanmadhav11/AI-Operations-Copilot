export async function sendMessage(message) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: Date.now(),
        role: "assistant",
        content: `# AI Response

You asked:

> ${message}

---

### Analysis

This is a **mock response**.

Later this response will come from:

- FastAPI
- LangGraph
- OpenAI
- Company Database

\`\`\`python
print("Hello AI")
\`\`\`

The markdown above is rendered by ReactMarkdown.
`,
      });
    }, 1500);
  });
}