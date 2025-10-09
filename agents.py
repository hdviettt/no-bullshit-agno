'''
Name: Content SEO AI Agents
Author: Hoang Duc Viet
Description: AI Agentic System for SEO content creation with Agno.
Version: 0.1.0
Latest changes: 
- connected to Arize Phoenix for tracing and evaluation.
NOTES:
- not being able to trace total token usage and costs due to agno itself.

TODO: 
- RAG

'''

from agno.agent import Agent
from agno.team import Team
from agno.os import AgentOS

# Model
from agno.models.anthropic import Claude

# SQLite Database
from agno.db.sqlite import SqliteDb

# RAG Chromadb Database
# import chromadb
# from agno.knowledge.knowledge import Knowledge
# from agno.vectordb.chroma import ChromaDb
# from agno.knowledge.embedder.cohere import CohereEmbedder
# from chromadb.config import Settings
# import chromadb.utils.embedding_functions as embedding_functions


# Tools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.mcp import MultiMCPTools

# async run for MCP
import asyncio

# tracing and evaluation
from phoenix.otel import register

# Token tracking
from token_tracker import TokenTracker

# Load environment variables
import os
import dotenv
dotenv.load_dotenv()

# Initialize token tracker
tracker = TokenTracker()

# Declare database

db = SqliteDb(
    db_file="database.db",
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

# Configure RAG database with Chroma

## embedding with Cohere
# cohere_ef = embedding_functions.CohereEmbeddingFunction(
#     api_key=os.getenv('COHERE_API_KEY'),
#     model_name="embed-v4.0"
#     )

# client = chromadb.CloudClient(
#   api_key = "ck-5h8C36CwzBp81NwGoNjvZkNyrzEmjQcg5kkfPZVoQ8Pu",
#   tenant = 'de163e20-bb6f-4dc9-a7e8-51eab137d1ca',
#   database = 'agno'
# )

# knowledge = Knowledge(
#     name = "Story writing knowledge",
#     description = "Guidance on how to write effective short stories",
#     vector_db = ChromaDb(
#         collection="sample_collection",
#         embedder=CohereEmbedder(id="embed-v4.0", api_key="wiZKEho6gTFN97xutVtDKFp7pHIo7XDte10WXZfH"),
#         settings = Settings(
#             chroma_api_impl = "chromadb.api.fastapi.FastAPI",
#             chroma_server_host = "de163e20-bb6f-4dc9-a7e8-51eab137d1ca.api.trychroma.com",
#             chroma_server_http_port = 443,
#             chroma_server_ssl_enabled = True,
#             chroma_client_auth_provider="chromadb.auth.token_authn.TokenAuthClientProvider",
#             chroma_client_auth_credentials="ck-5h8C36CwzBp81NwGoNjvZkNyrzEmjQcg5kkfPZVoQ8Pu"
#         )
#     )
# )

# TRACING & EVALUATION
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:6006"
os.environ["PHOENIX_PROJECT_NAME"] = "writer"

# Register Phoenix with enhanced configuration
tracer_provider = register(
    project_name="writer",
    auto_instrument=True,
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
        model = Claude(id="claude-sonnet-4-5-20250929", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="You are short story idea creator. You generate an idea and suggest a clear outline base on a given topic",
        instructions = [
            "When asked to write a story, only return the story and nothing else.",
            "Don't use icons and emojis"
            ],
        tools = [DuckDuckGoTools()],
        # reasoning=True,
        # reasoning_max_steps=10,
        db = db,
        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_chat_history=True, ## enables agent to read the chat history that were previously stored
        # enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
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
        model = Claude(id="claude-sonnet-4-5-20250929", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="You are a short storywriter. Base on a given outline, you write a short compelling story.",
        instructions=[
            "When asked to write a story, only return the story itself and nothing else.",
            "Never use emojis or icons."
        ],
        tools = [],
        # reasoning=True,
        # reasoning_max_steps=10,
        db = db,
        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_chat_history=True, ## enables agent to read the chat history that were previously stored
        # enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
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
        model = Claude(id="claude-sonnet-4-5-20250929", api_key=os.getenv("ANTHROPIC_API_KEY")),
        description="",
        instructions=[
            "use outline agent to generate outline",
            "use writer agent to produce story from outline",
            "return ONLY the final story of the writer agent, DO NOT add extra words or explaining.",
            "dont use any icons or emojies"
        ],
        tools = [],
        db = db,
        # knowledge = knowledge,

        add_history_to_context=True, ## retrieve conversaion history -> memory
        read_team_history=True,
        # enable_session_summaries=True, ## summarizes the content of a long conversaion to storage
        num_history_runs=2,
        search_session_history=True, ## allow searching through past sessions


        # num_history_sessions=2, ## retrieve only the 2 lastest sessions of the agent
        markdown=True,
        debug_mode=True,
        cache_session=True,


        members=[outline_agent, content_writer], 
        # reasoning=True,
        # reasoning_max_steps = 2,
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
    os_instance.serve(app="agents:app", reload=False)
