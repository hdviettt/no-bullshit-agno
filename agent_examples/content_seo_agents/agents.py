'''
Name: Content SEO AI Agents
Author: Hoang Duc Viet
Description: AI Agentic System for SEO content creation with Agno.
Version: 0.1.0
Latest changes: 
TODO: 
- memory management
- RAG
- Evalutation
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
outline_agent_db = SqliteDb(
    db_file="agents/outline_agent.db",
    # Table to store your Agent, Team and Workflow sessions and runs
    session_table="sessions",
    # Table to store all user memories
    memory_table="memory",
    # Table to store all metrics aggregations
    metrics_table="metrics",
    # Table to store all your evaluation data
    eval_table="evals",
    # Table to store all your knowledge content
    knowledge_table="knowledge",
)

writer_agent_db = SqliteDb(
    db_file="agents/writer_agent.db",
    # Table to store your Agent, Team and Workflow sessions and runs
    session_table="sessions",
    # Table to store all user memories
    memory_table="memory",
    # Table to store all metrics aggregations
    metrics_table="metrics",
    # Table to store all your evaluation data
    eval_table="evals",
    # Table to store all your knowledge content
    knowledge_table="knowledge",
)

team_db = SqliteDb(
    db_file="agents/content_team.db",
    # Table to store your Agent, Team and Workflow sessions and runs
    session_table="sessions",
    # Table to store all user memories
    memory_table="memory",
    # Table to store all metrics aggregations
    metrics_table="metrics",
    # Table to store all your evaluation data
    eval_table="evals",
    # Table to store all your knowledge content
    knowledge_table="knowledge",
)

"""
SEO CONTENT CREATION TEAM

Members:
- Outline Agent
- Content Writer Agent
"""
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

    outline_agent = Agent(
        name = "Outline Agent",
        role = "Create a short story outline based on a given topic",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="You are short story idea creator. You generate an idea and suggest a clear outline base on a given topic",
        instructions = [
            "When asked to write a story, only return the story and nothing else.",
            "Don't use icons and emojis"
            ],
        tools = [DuckDuckGoTools()],
        # reasoning=True,
        # reasoning_max_steps=10,
        db = outline_agent_db,
        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_chat_history=True, ## enables agent to read the chat history that were previously stored
        enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
        num_history_runs=2,
        search_session_history=True, ## allow searching through past sessions
        # num_history_sessions=2, ## retrieve only the 2 lastest sessions of the agent
        markdown=True,
        debug_mode=True,
        cache_session=True
    )

    content_writer = Agent(
        name = "Content Writer Agent",
        role = "Write story based on a given outline",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="You are a short storywriter. Base on a given outline, you write a short compelling story.",
        instructions=[
            "When asked to write a story, only return the story itself and nothing else.",
            "Never use emojis or icons."
        ],
        tools = [],
        # reasoning=True,
        # reasoning_max_steps=10,
        db = writer_agent_db,
        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_chat_history=True, ## enables agent to read the chat history that were previously stored
        enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
        num_history_runs=2,
        search_session_history=True, ## allow searching through past sessions
        # num_history_sessions=2, ## retrieve only the 2 lastest sessions of the agent
        markdown=True,
        debug_mode=True,
        cache_session=True
    )

    content_team = Team(
        name="AI SEO Content Team",
        role="Coordinate the team members",
        model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="You are a short story writing helper with 2 team members: outline agent and content writer. Use outline agent to come up with story outline base on topic, and use that outline to pass onto the content writer agent to produce a full short story. If the user provides the outline first-hand, the outline agent isn't needed.",
        instructions=[
            "When the user asks for an outline, only return the outline from the outline agent",
            "When the user asks for a story, only return the full short story after the appropriate team members have completed their job."
        ],
        tools = [],
        db = team_db,

        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_chat_history=True, ## enables agent to read the chat history that were previously stored
        enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
        num_history_runs=2,
        search_session_history=True, ## allow searching through past sessions
        read_team_history=True,

        # num_history_sessions=2, ## retrieve only the 2 lastest sessions of the agent
        markdown=True,
        debug_mode=True,
        cache_session=True,


        members=[outline_agent, content_writer], 
        reasoning=True,
        reasoning_max_steps = 2,
        # add_datetime_to_context=True,
        # add_history_to_context=True,
    )

    agent_os = AgentOS(
        id="my os",
        description="My AgentOS",
        # agents=[assistant],
        teams=[content_team],
        agents=[outline_agent, content_writer]
    )

    return agent_os

os_instance = content_team()
app = os_instance.get_app()

if __name__ == "__main__":
    os_instance.serve(app="agents:app", reload=True)
