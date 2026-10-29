import os
import anthropic
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Claude Bridge", host="0.0.0.0", port=int(os.environ.get("PORT", "10000")), stateless_http=True, json_response=True)

@mcp.tool()
def ask_claude(question: str) -> str:
    """Ask Anthropic Claude a question and return its response."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        return "Server configuration error: ANTHROPIC_API_KEY is missing."
    client = anthropic.Anthropic(api_key=key, timeout=45.0)
    response = client.messages.create(
        model=os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-5"),
        max_tokens=1200,
        messages=[{"role": "user", "content": question}],
    )
    return "\n".join(block.text for block in response.content if block.type == "text")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
