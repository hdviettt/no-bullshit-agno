from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.os import AgentOS

import dotenv
dotenv.load_dotenv()
import os

assistant = Agent(
    name="Assistant",
    model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="example_agentos:app", reload=True)