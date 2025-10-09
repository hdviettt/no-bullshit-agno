# AI Content Creation System with Agno

> An intelligent multi-agent system for automated short story generation powered by Agno and Claude AI, with comprehensive observability and cost tracking.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno](https://img.shields.io/badge/agno-2.1.3-purple.svg)](https://github.com/agno-agi/agno)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

## Overview

This project implements an AI-powered agentic workflow system designed for creative content generation. Built with [Agno](https://agno.com), it orchestrates multiple specialized AI agents to collaboratively produce high-quality short stories from simple topic inputs.

### Key Features

- **Multi-Agent Collaboration**: Coordinated team of specialized agents (Outline Agent, Content Writer)
- **Persistent Memory**: SQLite-backed session and conversation history
- **Observability**: Full tracing and evaluation using Arize Phoenix
- **Cost Tracking**: Granular token usage and cost analytics per agent and session
- **Web API**: FastAPI-powered REST interface with AgentOS
- **Search Integration**: DuckDuckGo and MCP tools for research capabilities
- **Enterprise Ready**: Production-grade error handling, logging, and metrics

## Architecture

```

         +---------------------------+
         |   AgentOS (FastAPI App)   |
         +-------------+-------------+
                       |
                       v
              +--------+--------+
              |  Content Team   |
              |   (Manager)     |
              +--------+--------+
                       |
           +-----------+-----------+
           |                       |
           v                       v
      +----+----+            +-----+-----+
      | Outline |            | Content   |
      |  Agent  |  --------> |  Writer   |
      +---------+            +-----------+
           |                       |
           +-----------+-----------+
                       |
                       v
            +----------+------------+
            |  SQLite Database      |
            |  - Sessions           |
            |  - Memory             |
            |  - Metrics            |
            |  - Token Usage        |
            +-----------------------+
```

### Agent Responsibilities

1. **Outline Agent**: Researches topics and generates structured story outlines
2. **Content Writer**: Transforms outlines into compelling short stories
3. **Team Coordinator**: Orchestrates agent collaboration and output aggregation

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (Claude Sonnet 4.5)
- Node.js and npm (for MCP tools)
- Optional: Mapbox API key (for location-based content)

## Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/no-bullshit-agno.git
cd no-bullshit-agno
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional - for enhanced features
MAPBOX_ACCESS_TOKEN=your_mapbox_token
COHERE_API_KEY=your_cohere_key  # For RAG embeddings

# Phoenix Observability (defaults shown)
PHOENIX_COLLECTOR_ENDPOINT=http://localhost:6006
PHOENIX_PROJECT_NAME=writer
```

## Quick Start

### 1. Start Arize Phoenix (Optional - for observability)

```bash
python -m phoenix.server.main serve
```

Phoenix will be available at `http://localhost:6006`

### 2. Run the Agent System

```bash
python agents.py
```

The FastAPI server will start at `http://localhost:8000`

### 3. Access the API

**Interactive Documentation**: `http://localhost:8000/docs`

**Example Request**:
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{"topic": "A detective solving a mystery in a futuristic city"}'
```

## Usage

### Python API

```python
from agents import content_team

# Initialize the agent system
os_instance = content_team()

# Generate content programmatically
result = os_instance.run(
    message="Write a story about artificial intelligence gaining consciousness",
    session_id="story-session-001"
)

print(result)
```

### Command Line

```bash
# Start the server
python agents.py

# In another terminal, use the CLI
python -c "
from agents import content_team
os = content_team()
print(os.run('Write a story about time travel'))
"
```

## Observability & Analytics
### Arize Phoenix Dashboard

Access comprehensive tracing at `http://localhost:6006`:
- Agent execution traces
- Latency analysis
- Token consumption per request
- Error tracking
- Performance metrics

### Database Schema

The SQLite database (`database.db`) contains:

```sql
-- Session management
sessions         -- Agent/team conversation sessions
memory           -- Long-term agent memory
metrics          -- Performance metrics
evals            -- Evaluation data

-- Custom tracking
token_usage      -- Detailed token consumption and costs
knowledge        -- RAG knowledge base (future)
```

## Project Structure

```
no-bullshit-agno/
├── agents.py              # Main agent definitions and orchestration
├── database.db            # SQLite database
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration (create from .env.example)
├── .env.example           # Example environment variables
├── documents/             # Knowledge base files (for RAG)
├── rag.ipynb             # RAG experimentation notebook
├── agent_guide.ipynb     # Development guide
└── LICENSE               # Apache 2.0 license
```

## Configuration

### Agent Customization

Edit `agents.py` to customize agent behavior:

```python
outline_agent = Agent(
    name="Outline Agent",
    role="Create story outlines",
    model=Claude(id="claude-sonnet-4-5-20250929"),
    instructions=[
        "Generate creative and structured outlines",
        "Research the topic thoroughly using search tools"
    ],
    tools=[DuckDuckGoTools()],
    # Memory settings
    add_history_to_context=True,
    num_history_runs=2,
    search_session_history=True,
)
```

### Database Configuration

Modify database settings in `agents.py`:

```python
db = SqliteDb(
    db_file="database.db",
    session_table="sessions",
    memory_table="memory",
    metrics_table="metrics",
)
```

## Advanced Features

### Session Management

```python
# Continue a previous conversation
result = os_instance.run(
    message="Make the story darker",
    session_id="story-session-001"  # Same session ID
)
```

### Search History

Agents can search through previous sessions:

```python
outline_agent = Agent(
    search_session_history=True,  # Enable session search
    num_history_runs=2,            # Retrieve last 2 runs
    enable_session_summaries=True  # Summarize long conversations
)
```

### RAG Integration (Coming Soon)

ChromaDB integration for knowledge-augmented generation:

```python
# Uncomment RAG configuration in agents.py
knowledge = Knowledge(
    name="Story writing knowledge",
    vector_db=ChromaDb(collection="stories"),
    embedder=CohereEmbedder()
)
```

## Performance & Costs

Based on testing with Claude Sonnet 4.5:

| Metric | Average | Notes |
|--------|---------|-------|
| Story Generation Time | 15-30s | Depends on complexity |
| Input Tokens | ~1,500 | Including context |
| Output Tokens | ~3,000 | 500-800 word stories |
| Cost Per Story | $0.06-$0.12 | At current pricing |

*Monitor costs in real-time using `analyze_costs.py`*

## Troubleshooting

### Common Issues

**Database locked error**:
```bash
# Close all connections or delete the database
rm database.db
# Restart the application
```

**Phoenix not connecting**:
```bash
# Verify Phoenix is running
curl http://localhost:6006/healthz

# Check environment variables
echo $PHOENIX_COLLECTOR_ENDPOINT
```

**MCP tools not working**:
```bash
# Ensure Node.js is installed
node --version

# Test MCP server manually
npx -y @mapbox/mcp-server
```

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Agents

1. Define agent in `agents.py`
2. Add to team members list
3. Update team instructions
4. Test with sample queries

### Extending Tools

```python
from agno.tools import Tool

custom_tool = Tool(
    name="my_tool",
    function=my_function,
    description="Tool description"
)

agent = Agent(tools=[custom_tool])
```

## Roadmap

- [ ] RAG integration with ChromaDB
- [ ] Multi-format export (PDF, DOCX, Markdown)
- [ ] Custom evaluation metrics
- [ ] Batch processing API
- [ ] Agent reasoning mode optimization
- [ ] Image generation integration
- [ ] Multi-language support
- [ ] Web UI dashboard

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Agno](https://agno.com) - AI agent framework
- [Anthropic](https://anthropic.com) - Claude AI models
- [Arize Phoenix](https://phoenix.arize.com) - Observability platform
- [DuckDuckGo](https://duckduckgo.com) - Search API

## Author

**Hoang Duc Viet**

## Support

For issues and questions:
- Open an issue on GitHub
- Check the [Agno documentation](https://docs.agno.com)
- Review Phoenix [troubleshooting guide](https://docs.arize.com/phoenix)

---

**Version**: 0.1.0
**Last Updated**: October 2025
**Status**: Active Development
