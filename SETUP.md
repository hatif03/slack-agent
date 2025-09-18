# Slack Agent Open Source Setup Guide

This guide will help you set up the open-source version of Slack Agent, which replaces vendor-locked dependencies with open-source alternatives.

## What Changed

### Removed Dependencies
- `langchain-arcade` - Replaced with direct API integrations
- `arcadepy` - Replaced with open-source libraries

### New Dependencies
- `langchain-community` - Community tools and integrations
- `langchain-google-search` - Google search integration
- `requests` - HTTP requests
- `beautifulsoup4` - Web scraping
- `github3-py` - GitHub API client
- `google-api-python-client` - Google API client
- `google-auth` - Google authentication
- `google-auth-oauthlib` - Google OAuth

## Environment Variables

### Required
```bash
SLACK_BOT_TOKEN=your_slack_bot_token
SLACK_SIGNING_SECRET=your_slack_signing_secret
OPENAI_API_KEY=your_openai_api_key
```

### Optional - GitHub Integration
```bash
GITHUB_TOKEN=your_github_token
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=your_github_redirect_uri
```

### Optional - Google Integration
```bash
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_google_refresh_token
GOOGLE_REDIRECT_URI=your_google_redirect_uri
```

## Getting API Keys

### GitHub API Token
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with appropriate scopes:
   - `repo` (for private repositories)
   - `public_repo` (for public repositories)
   - `user` (for user information)

### Google API Credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the APIs you need:
   - Gmail API
   - Google Drive API
   - Google Calendar API
4. Create OAuth 2.0 credentials
5. Download the credentials JSON file
6. Use the client ID and secret from the JSON file

## Installation

1. Install dependencies:
```bash
cd SlackAgent-OpenSource
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. Test the installation:
```bash
python test_imports.py
```

## Features

### Available Tools
- **GitHub**: Search repositories, get PRs, issues, repository info
- **Google**: Gmail search, Calendar events, Drive files, Google Docs
- **Web Search**: DuckDuckGo search (privacy-focused)
- **Web Scraping**: Extract content from websites

### Tool Configuration
Tools are configured in `slack_agent/tools/manager.py`. You can:
- Enable/disable specific tools
- Add new tools by implementing the tool interface
- Configure authentication requirements

## Adding New Tools

To add a new tool:

1. Create a new file in `slack_agent/tools/` (e.g., `my_tool.py`)
2. Implement the tool class with `get_langchain_tools()` method
3. Add the tool to `slack_agent/tools/manager.py`
4. Update the tool registry

Example:
```python
class MyTool:
    def get_langchain_tools(self) -> List[BaseTool]:
        return [self.my_tool_function]
    
    @tool
    def my_tool_function(self, input: str) -> str:
        # Tool implementation
        return "Result"
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed with `poetry install`
2. **API Key Errors**: Verify your API keys are correctly set in environment variables
3. **Authentication Errors**: Check that OAuth credentials are properly configured

### Testing Individual Tools

You can test individual tools by running:
```python
from slack_agent.tools.github_tool import GitHubTool
github = GitHubTool()
tools = github.get_langchain_tools()
# Test the tools
```

## Migration from Arcade Version

If you're migrating from the Arcade version:

1. Update your environment variables (remove `ARCADE_API_KEY`)
2. Add the new API keys for services you want to use
3. The tool interface remains the same, so existing configurations should work
4. Test thoroughly to ensure all functionality works as expected

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the tool implementations in `slack_agent/tools/`
3. Check the logs for detailed error messages
