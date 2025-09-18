"""GitHub integration tool using github3.py."""

import os
import logging
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from github3 import GitHub

logger = logging.getLogger(__name__)


class GitHubTool:
    """GitHub integration tool for repository operations."""
    
    def __init__(self):
        """Initialize GitHub tool."""
        self.github_token = os.environ.get("GITHUB_TOKEN")
        self.github = None
        if self.github_token:
            self.github = GitHub(token=self.github_token)
    
    def get_langchain_tools(self) -> List[BaseTool]:
        """Get LangChain tools for GitHub operations."""
        return [
            self.search_repositories,
            self.get_repository_info,
            self.list_recent_prs,
            self.get_pr_details,
            self.search_issues,
        ]
    
    def get_auth_url(self, user_id: str) -> str:
        """Get GitHub OAuth URL for authentication."""
        # This would typically redirect to GitHub OAuth
        return f"https://github.com/login/oauth/authorize?client_id={os.environ.get('GITHUB_CLIENT_ID', '')}&redirect_uri={os.environ.get('GITHUB_REDIRECT_URI', '')}&state={user_id}"
    
    @tool
    def search_repositories(query: str) -> str:
        """Search for GitHub repositories."""
        try:
            github_token = os.environ.get("GITHUB_TOKEN")
            if not github_token:
                return "GitHub token not configured. Please set GITHUB_TOKEN environment variable."
            
            github = GitHub(token=github_token)
            repos = github.search_repositories(query)
            
            results = []
            for repo in repos[:5]:  # Limit to 5 results
                results.append({
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "url": repo.html_url
                })
            
            if not results:
                return f"No repositories found for query: {query}"
            
            response = f"Found {len(results)} repositories for '{query}':\n\n"
            for repo in results:
                response += f"• **{repo['full_name']}** ({repo['stars']} stars)\n"
                response += f"  {repo['description'] or 'No description'}\n"
                response += f"  {repo['url']}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching repositories: {e}")
            return f"Error searching repositories: {str(e)}"
    
    @tool
    def get_repository_info(owner: str, repo: str) -> str:
        """Get detailed information about a specific repository."""
        try:
            github_token = os.environ.get("GITHUB_TOKEN")
            if not github_token:
                return "GitHub token not configured. Please set GITHUB_TOKEN environment variable."
            
            github = GitHub(token=github_token)
            repository = github.repository(owner, repo)
            
            if not repository:
                return f"Repository {owner}/{repo} not found."
            
            info = {
                "name": repository.name,
                "full_name": repository.full_name,
                "description": repository.description,
                "stars": repository.stargazers_count,
                "forks": repository.forks_count,
                "watchers": repository.watchers_count,
                "language": repository.language,
                "created_at": repository.created_at.isoformat(),
                "updated_at": repository.updated_at.isoformat(),
                "url": repository.html_url,
                "clone_url": repository.clone_url,
            }
            
            response = f"**{info['full_name']}**\n\n"
            response += f"Description: {info['description'] or 'No description'}\n"
            response += f"Language: {info['language'] or 'Not specified'}\n"
            response += f"Stars: {info['stars']} | Forks: {info['forks']} | Watchers: {info['watchers']}\n"
            response += f"Created: {info['created_at']}\n"
            response += f"Updated: {info['updated_at']}\n"
            response += f"URL: {info['url']}\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting repository info: {e}")
            return f"Error getting repository info: {str(e)}"
    
    @tool
    def list_recent_prs(owner: str, repo: str, limit: int = 5) -> str:
        """List recent pull requests for a repository."""
        try:
            github_token = os.environ.get("GITHUB_TOKEN")
            if not github_token:
                return "GitHub token not configured. Please set GITHUB_TOKEN environment variable."
            
            github = GitHub(token=github_token)
            repository = github.repository(owner, repo)
            
            if not repository:
                return f"Repository {owner}/{repo} not found."
            
            prs = list(repository.pull_requests(state='all'))[:limit]
            
            if not prs:
                return f"No pull requests found for {owner}/{repo}."
            
            response = f"Recent pull requests for {owner}/{repo}:\n\n"
            for pr in prs:
                status = "🟢 Open" if pr.state == "open" else "🔴 Closed"
                response += f"• **#{pr.number}** {pr.title} {status}\n"
                response += f"  Author: {pr.user.login}\n"
                response += f"  Created: {pr.created_at.strftime('%Y-%m-%d %H:%M')}\n"
                response += f"  URL: {pr.html_url}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error listing PRs: {e}")
            return f"Error listing PRs: {str(e)}"
    
    @tool
    def get_pr_details(owner: str, repo: str, pr_number: int) -> str:
        """Get detailed information about a specific pull request."""
        try:
            github_token = os.environ.get("GITHUB_TOKEN")
            if not github_token:
                return "GitHub token not configured. Please set GITHUB_TOKEN environment variable."
            
            github = GitHub(token=github_token)
            repository = github.repository(owner, repo)
            
            if not repository:
                return f"Repository {owner}/{repo} not found."
            
            pr = repository.pull_request(pr_number)
            
            if not pr:
                return f"Pull request #{pr_number} not found in {owner}/{repo}."
            
            response = f"**Pull Request #{pr.number}: {pr.title}**\n\n"
            response += f"Status: {'🟢 Open' if pr.state == 'open' else '🔴 Closed'}\n"
            response += f"Author: {pr.user.login}\n"
            response += f"Created: {pr.created_at.strftime('%Y-%m-%d %H:%M')}\n"
            response += f"Updated: {pr.updated_at.strftime('%Y-%m-%d %H:%M')}\n"
            response += f"URL: {pr.html_url}\n\n"
            
            if pr.body:
                response += f"Description:\n{pr.body[:500]}{'...' if len(pr.body) > 500 else ''}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting PR details: {e}")
            return f"Error getting PR details: {str(e)}"
    
    @tool
    def search_issues(owner: str, repo: str, query: str = "", state: str = "open") -> str:
        """Search for issues in a repository."""
        try:
            github_token = os.environ.get("GITHUB_TOKEN")
            if not github_token:
                return "GitHub token not configured. Please set GITHUB_TOKEN environment variable."
            
            github = GitHub(token=github_token)
            repository = github.repository(owner, repo)
            
            if not repository:
                return f"Repository {owner}/{repo} not found."
            
            search_query = f"repo:{owner}/{repo} {query}"
            issues = github.search_issues(search_query, state=state)
            
            results = []
            for issue in issues[:5]:  # Limit to 5 results
                results.append({
                    "number": issue.number,
                    "title": issue.title,
                    "state": issue.state,
                    "user": issue.user.login,
                    "created_at": issue.created_at,
                    "url": issue.html_url
                })
            
            if not results:
                return f"No {state} issues found for query '{query}' in {owner}/{repo}."
            
            response = f"Found {len(results)} {state} issues for '{query}' in {owner}/{repo}:\n\n"
            for issue in results:
                status_icon = "🟢" if issue['state'] == "open" else "🔴"
                response += f"• **#{issue['number']}** {issue['title']} {status_icon}\n"
                response += f"  Author: {issue['user']}\n"
                response += f"  Created: {issue['created_at'].strftime('%Y-%m-%d %H:%M')}\n"
                response += f"  URL: {issue['url']}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching issues: {e}")
            return f"Error searching issues: {str(e)}"
