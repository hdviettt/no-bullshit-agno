'''
Name: Content SEO AI Agents
Author: Hoang Duc Viet
Description: AI Agentic System for SEO content creation with Agno.
Version: 0.1.0
Latest changes: 
TODO: 
'''

from agno.agent import Agent
from agno.team import Team
from agno.os import AgentOS

# Model
from agno.models.anthropic import Claude

# SQLite Database
from agno.db.sqlite import SqliteDb

# Tools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.mcp import MultiMCPTools

# async run for MCP
import asyncio

# Load environment variables
import os
import dotenv
dotenv.load_dotenv()

# Declare database
# db = SqliteDb(
#     db_file="agno.db",
#     # Table to store your Agent, Team and Workflow sessions and runs
#     session_table="sessions",
#     # Table to store all user memories
#     memory_table="memory",
#     # Table to store all metrics aggregations
#     metrics_table="metrics",
#     # Table to store all your evaluation data
#     eval_table="evals",
#     # Table to store all your knowledge content
#     knowledge_table="knowledge",
# )

# web_agent = Agent(
#     name="Web Agent",
#     role="Search the web for information",
#     model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
#     tools=[DuckDuckGoTools()],
#     # storage=SqliteAgentStorage(table_name="web_agent", db_file="agents.db"),
#     db=db,
#     add_history_to_context=True,
#     add_datetime_to_context=True,
#     markdown=True,
# )
'''
1. SEO CONTENT CREATION TEAM

Members:
- Outline Agent
- Content Writer Agent
'''
def content_team():
    """Run AI Agent team."""
    ## Declare MCP tools
    content_env = {
            **os.environ,
            # 'FREEPIK_API_KEY': os.getenv('FREEPIK_API_KEY'),
            # 'DATAFORSEO_USERNAME': os.getenv('DATAFORSEO_USERNAME'),
            # 'DATAFORSEO_PASSWORD': os.getenv('DATAFORSEO_PASSWORD'),
            # 'BRAVE_API_KEY': os.getenv('BRAVE_API_KEY'),
            "MAPBOX_ACCESS_TOKEN": os.getenv("MAPBOX_ACCESS_TOKEN")
    }

    content_mcp_tools = MultiMCPTools(
        commands=[
            "npx -y @mapbox/mcp-server",
        ],
        env=content_env
    )

    # content_mcp_tools.connect()
    # content_mcp_tools.connect()

    outline_agent = Agent(
        name = "Outline Agent",
        role = "Create an SEO content outline based on a given keyword",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        tools = [DuckDuckGoTools(), content_mcp_tools],
        instructions = []
    )

    content_writer = Agent(
        name="Content Writer Agent",
        role="Write SEO content based on a given outline",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        tools = [content_mcp_tools],
        instructions=[],
        # db=db,
        # add_history_to_context=True,
        # add_datetime_to_context=True,
        markdown=True,
    )

    content_team = Team(
        name="AI SEO Content Team",
        instructions="Use outline agent to come up with content outline base on keywords, and use that outline to pass onto the content writer agent to produce a full SEO content blog. If the user provides the outline first-hand, the outline agent isn't needed.",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        members=[outline_agent, content_writer], 
        reasoning=True,
        reasoning_max_steps=10
        # db=db
    )

    agent_os = AgentOS(
        id="my-first-os",
        description="My first AgentOS",
        # agents=[assistant],
        teams=[content_team],
    )

    return agent_os

os_instance = content_team()
app = os_instance.get_app()

if __name__ == "__main__":
    os_instance.serve(app="agents:app", reload=True)
