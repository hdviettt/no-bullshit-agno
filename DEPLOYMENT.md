# Railway Deployment Guide - Agno Content Creation Team

This guide will help you deploy your AI Content Creation Team to Railway.

## Files Created

✅ **Dockerfile** - Container configuration for your agent
✅ **docker-compose.yaml** - Local testing configuration
✅ **.dockerignore** - Exclude unnecessary files from Docker build
✅ **railway.json** - Railway-specific configuration
✅ **agents.py** - Updated to use environment variables for port/host
✅ **requirements.txt** - All Python dependencies (already existed)

## Prerequisites

1. **Railway Account** - Sign up at https://railway.app
2. **Git Repository** - Your code should be in a GitHub repo
3. **API Keys** - All your environment variables ready

## Step-by-Step Deployment to Railway

### 1. Push Your Code to GitHub

```bash
# If not already a git repo
git init
git add .
git commit -m "Prepare for Railway deployment"

# Create a new GitHub repo and push
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy to Railway

#### Option A: Via Railway Dashboard (Recommended)

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize GitHub and select your repository
5. Railway will automatically detect the `Dockerfile` and start building

#### Option B: Via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

### 3. Configure Environment Variables

In the Railway dashboard, go to your project → **Variables** tab and add:

**Required API Keys:**
```
ANTHROPIC_API_KEY=sk-ant-api03-...
XAI_API_KEY=xai-...
FREEPIK_API_KEY=FPSXc909...
COHERE_API_KEY=wiZKEho6...
```

**Optional API Keys:**
```
OPENAI_API_KEY=sk-proj-...
TAVILY_API_KEY=tvly-dev-...
CHROMA_API_KEY=ck-5h8C...
MAPBOX_ACCESS_TOKEN=pk.eyJ1...
SUPABASE_DB_URL=postgresql://...
```

**Note:** Railway automatically provides the `PORT` environment variable.

### 4. Enable Public URL

1. In Railway dashboard, go to your service
2. Click on **Settings** tab
3. Under **Networking**, click **Generate Domain**
4. Your agent will be available at: `https://your-app.railway.app`

### 5. Monitor Deployment

- **Build Logs**: Watch the build process in real-time
- **Deploy Logs**: Check if the application started correctly
- **Metrics**: Monitor CPU, memory usage
- **Health Check**: Visit `https://your-app.railway.app/docs` to see the API documentation

## Local Testing with Docker

Before deploying to Railway, test locally:

```bash
# Build and run with Docker Compose
docker-compose up --build

# Your agent will be available at:
# http://localhost:7778
```

To stop:
```bash
docker-compose down
```

## Accessing Your Deployed Agent

Once deployed, your agent will be accessible at:

- **API Endpoint**: `https://your-app.railway.app`
- **API Docs**: `https://your-app.railway.app/docs`
- **AgentOS UI**: `https://your-app.railway.app` (if configured)
- **Workflows**: `https://your-app.railway.app/workflows`

## Team Configuration

Your deployed agent includes:

**🎯 Team: AI SEO Content Team**

**Agents:**
1. **Outline Agent** - Creates story outlines (uses Grok-4)
2. **Content Writer Agent** - Writes story text (uses Grok-4)
3. **Image Integration Agent** - Adds real images from Freepik (uses Grok-4)

**Tools:**
- DuckDuckGo Search
- 13 Freepik MCP Tools (images, video generation, AI detection)

**Features:**
- SQLite database for sessions and memories
- Arize Phoenix integration for tracing
- Markdown output support
- Caching enabled for performance

## Troubleshooting

### Build Fails
- Check if all API keys are set in Railway variables
- Review build logs in Railway dashboard
- Ensure `requirements.txt` has all dependencies

### App Crashes on Start
- Check deploy logs for errors
- Verify all required API keys are present
- Ensure database file permissions are correct

### MCP Tools Timeout
- Freepik API might be slow - increase timeout (already set to 30s)
- Check if `FREEPIK_API_KEY` is valid

### Port Issues
- Railway automatically sets `PORT` - don't hardcode it
- The app already reads from `os.getenv("PORT", "7778")`

## Cost Estimation

Railway offers:
- **Free Tier**: $5 credit/month, perfect for testing
- **Pro Plan**: $20/month + usage-based pricing

Typical usage for this agent:
- ~512MB RAM usage
- Minimal CPU when idle
- Moderate CPU during story generation

**Estimated cost**: $5-15/month depending on traffic

## Updating Your Deployment

To update your deployed agent:

```bash
# Make changes to your code
git add .
git commit -m "Update agent configuration"
git push

# Railway will automatically rebuild and redeploy
```

## Database Persistence

Your `database.db` file stores:
- Agent sessions
- Conversation history
- User memories
- Evaluation data

**Important**: Railway provides ephemeral storage. For production:
1. Use Railway's PostgreSQL addon (recommended)
2. Or, mount a persistent volume
3. Or, use external database (Supabase, AWS RDS)

To add Railway PostgreSQL:
1. In project dashboard, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Update `agents.py` to use PostgreSQL instead of SQLite

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Configure all environment variables
3. ✅ Generate public domain
4. Test the API at `/docs` endpoint
5. Share with users!

## Support

- Railway Docs: https://docs.railway.app
- Agno Docs: https://docs.agno.com
- GitHub Issues: Create an issue in your repository

---

**Your agent is ready for production! 🚀**
