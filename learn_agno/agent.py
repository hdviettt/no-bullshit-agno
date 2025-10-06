# agent & model
from agno.agent import Agent
from agno.models.anthropic import Claude
import asyncio

# tools
from agno.tools import tool
from agno.tools.github import GithubTools

# mcp
from agno.tools.mcp import MCPTools
from agno.tools.mcp import MultiMCPTools

# memory
from agno.db.sqlite import SqliteDb

# env
import os
import dotenv
dotenv.load_dotenv()

# setup database
db = SqliteDb(db_file="agno.db")

# Setup tools
@tool
def factorial(int: int) -> int:
    """Returns the factorial of a given integer."""
    if int < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if int == 0 or int == 1:
        return 1
    result = 1
    for i in range(2, int + 1):
        result *= i
    return result

async def run_agent(message: str) -> None:
    """Run the agent with given message."""

    env = {
        **os.environ,
        'FREEPIK_API_KEY': os.getenv('FREEPIK_API_KEY'),
        'DATAFORSEO_USERNAME': os.getenv('DATAFORSEO_USERNAME'),
        'DATAFORSEO_PASSWORD': os.getenv('DATAFORSEO_PASSWORD'),
        'BRAVE_API_KEY': os.getenv('BRAVE_API_KEY'),
    }

    ## CONNECT MCP
    mcp_tools = MultiMCPTools(
        commands=[
            "node D:/MCP/mcp-servers/freepik-mcp/build/index.js",
            "node D:/MCP/mcp-server-typescript/build/main/main/index.js",
            "npx -y @brave/brave-search-mcp-server"
        ],
        env=env
    )

    await mcp_tools.connect()

    try:
        agent = Agent(
            tools=[mcp_tools],
            markdown=True,
        )

        await agent.aprint_response(message, stream=True)
    
    finally:
        await mcp_tools.close()

if __name__ == "__main__":
    asyncio.run(
        run_agent(
            "What will be the next Portugal match?"
        )
    )

# agent =  Agent(
#     db=db,
#     enable_user_memories=True,
#     add_history_to_context=True,
#     num_history_runs=5,
#     model = Claude(id="claude-sonnet-4-5"),
#     tools=[
#         factorial,
#         GithubTools(),
#         # BraveSearchTools(),
#     ],
#     instructions="You are a helpful assistant.",
#     markdown=True
# )


# chat_input = input()
# while chat_input != "exit":
#     agent.print_response(
#         chat_input,
#         user_id="user1",
#         stream=True
#     )
#     chat_input = input()