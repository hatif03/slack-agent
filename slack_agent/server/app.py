"""FastAPI application for Slack Agent."""

from fastapi import FastAPI


def create_fastapi_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Slack Agent",
        description="A LLM Agent that lives in your slack workspace",
        version="0.2.0"
    )
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {"message": "Slack Agent is running"}
    
    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app
