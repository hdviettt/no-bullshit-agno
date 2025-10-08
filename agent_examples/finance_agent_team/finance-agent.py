from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.db.sqlite import SqliteDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.team import Team
from agno.os import AgentOS
from agno.models.anthropic import Claude

import os
import dotenv
dotenv.load_dotenv()

db = SqliteDb(
    db_file="agno.db",
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

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
    model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
    tools=[DuckDuckGoTools()],
    # storage=SqliteAgentStorage(table_name="web_agent", db_file="agents.db"),
    db=db,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model = Claude(id="claude-sonnet-4-5", api_key=os.getenv("ANTHROPIC_API_KEY")),
    
    # tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    tools = [YFinanceTools()],
    instructions=["Always use tables to display data"],
    # storage=SqliteAgentStorage(table_name="finance_agent", db_file="agents.db"),
    db=db,
    add_history_to_context=True,
    add_datetime_to_context=True,
    markdown=True,
)

agent_team = Team(
    name="Finacne and Web Team", members=[finance_agent, web_agent], db=db
)

# # Stream with intermediate steps
# agent_team.print_response(
#     "What is the current stock price of Microsoft? Also, find the latest news about Microsoft from the web and provide a summary.",
#     stream=True,
#     stream_intermediate_steps=True
# )


agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    # agents=[assistant],
    teams=[agent_team]
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="finance-agent:app", reload=True)
    ##app="my_os:app", 