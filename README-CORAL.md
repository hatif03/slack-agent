# Slack Agent with Coral Protocol

This is a modified version of the Slack Agent that integrates with the Coral protocol for multi-agent orchestration.

## Overview

The Slack Agent has been adapted to work with Coral protocol, allowing it to:
- Participate in multi-agent conversations
- Receive instructions from other agents
- Send responses back through the Coral network
- Maintain its existing Slack functionality

## Files Added/Modified

### New Files
- `coral-agent.toml` - Coral agent configuration
- `main.py` - Coral protocol implementation
- `Dockerfile` - Container configuration
- `run_agent.sh` - Agent execution script
- `env.coral.example` - Environment variables template

### Modified Files
- `pyproject.toml` - Added Coral protocol dependencies

## Setup

1. **Install Dependencies**
   ```bash
   poetry install
   ```

2. **Configure Environment**
   ```bash
   cp env.coral.example .env
   # Edit .env with your actual values
   ```

3. **Required Environment Variables**
   - `CORAL_CONNECTION_URL` - URL to Coral server
   - `CORAL_AGENT_ID` - Unique agent identifier
   - `MODEL_API_KEY` - OpenAI API key
   - `SLACK_BOT_TOKEN` - Slack bot token
   - `SLACK_SIGNING_SECRET` - Slack signing secret

## Running the Agent

### Using Poetry
```bash
poetry run python main.py
```

### Using the Run Script
```bash
./run_agent.sh
```

### Using Docker
```bash
docker build -t slack-agent-coral .
docker run --env-file .env slack-agent-coral
```

## Coral Protocol Integration

The agent integrates with Coral protocol through:

1. **MCP Client** - Connects to Coral server via SSE
2. **Tool Integration** - Combines Coral tools with existing Slack tools
3. **Message Handling** - Processes messages from other agents
4. **Response Generation** - Sends responses back through Coral network

## Agent Capabilities

- **Slack Integration**: Full Slack workspace interaction
- **Multi-Agent Communication**: Send/receive messages with other agents
- **Tool Usage**: Access to web search, GitHub, Google tools, etc.
- **Context Awareness**: Maintains conversation history
- **Error Handling**: Robust error recovery and retry logic

## Configuration Options

The agent supports various configuration options in `coral-agent.toml`:

- Model settings (name, provider, temperature, max tokens)
- Timeout configurations
- Runtime parameters

## Troubleshooting

1. **Connection Issues**: Check Coral server URL and network connectivity
2. **Authentication**: Verify API keys and tokens are correct
3. **Tool Errors**: Check tool configurations and permissions
4. **Logs**: Enable verbose logging for detailed debugging

## Development

To modify the agent:

1. Update `main.py` for core logic changes
2. Modify `coral-agent.toml` for configuration changes
3. Update dependencies in `pyproject.toml` as needed
4. Test with `poetry run python main.py`

## Integration with Coral Server

This agent is designed to work with a Coral server instance. Make sure:

1. Coral server is running and accessible
2. Agent ID is unique across the Coral network
3. Required tools are available on the Coral server
4. Network connectivity is stable
