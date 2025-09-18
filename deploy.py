import os

import modal
from dotenv import load_dotenv
from modal import asgi_app

load_dotenv()

# Define your Modal stub
app = modal.App("SlackAgent")
vol = modal.Volume.from_name("slack-agent", create_if_missing=True)

# Create a Modal image with necessary dependencies
image = (
    modal.Image.debian_slim(python_version="3.12")
    .add_local_dir("./dist", "/root/dist", copy=True)
    .pip_install("/root/dist/slack_agent-0.2.0-py3-none-any.whl")
    .pip_install("langgraph")
)

# Define secrets to pass environment variables
secrets = modal.Secret.from_dict({
    "SLACK_BOT_TOKEN": os.environ["SLACK_BOT_TOKEN"],
    "SLACK_SIGNING_SECRET": os.environ["SLACK_SIGNING_SECRET"],
    "OPENAI_API_KEY": os.environ["OPENAI_API_KEY"],
    "FILE_STORAGE_BASE_DIR": "/data",
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    # Optional GitHub integration
    "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN", ""),
    "GITHUB_CLIENT_ID": os.environ.get("GITHUB_CLIENT_ID", ""),
    "GITHUB_CLIENT_SECRET": os.environ.get("GITHUB_CLIENT_SECRET", ""),
    "GITHUB_REDIRECT_URI": os.environ.get("GITHUB_REDIRECT_URI", ""),
    # Optional Google integration
    "GOOGLE_CLIENT_ID": os.environ.get("GOOGLE_CLIENT_ID", ""),
    "GOOGLE_CLIENT_SECRET": os.environ.get("GOOGLE_CLIENT_SECRET", ""),
    "GOOGLE_REFRESH_TOKEN": os.environ.get("GOOGLE_REFRESH_TOKEN", ""),
    "GOOGLE_REDIRECT_URI": os.environ.get("GOOGLE_REDIRECT_URI", ""),
    # Optional LangSmith tracing
    "LANGSMITH_TRACING": os.environ.get("LANGSMITH_TRACING", "false"),
    "LANGSMITH_ENDPOINT": os.environ.get("LANGSMITH_ENDPOINT", ""),
    "LANGSMITH_API_KEY": os.environ.get("LANGSMITH_API_KEY", ""),
    "LANGSMITH_PROJECT": os.environ.get("LANGSMITH_PROJECT", "slack-agent"),
})


@app.function(
    image=image, secrets=[secrets], volumes={"/data": vol}, min_containers=1
)
@modal.concurrent(max_inputs=100)
@asgi_app()
def slack_agent():
    # Import here to ensure it happens inside the container
    from slack_agent.server import create_fastapi_app

    return create_fastapi_app()
