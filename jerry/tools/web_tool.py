"""Web scraping and content extraction tool."""

import logging
import requests
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)


class WebTool:
    """Web scraping and content extraction tool."""
    
    def __init__(self):
        """Initialize web tool."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def get_langchain_tools(self) -> List[BaseTool]:
        """Get LangChain tools for web operations."""
        return [
            self.scrape_website,
            self.get_website_summary,
            self.extract_links,
            self.get_page_title,
        ]
    
    @tool
    def scrape_website(url: str, max_length: int = 2000) -> str:
        """Scrape content from a website."""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return "Invalid URL provided."
            
            # Add https if no scheme provided
            if not parsed.scheme:
                url = f"https://{url}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return f"Content from {url}:\n\n{text}"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping website {url}: {e}")
            return f"Error accessing website {url}: {str(e)}"
        except Exception as e:
            logger.error(f"Error scraping website {url}: {e}")
            return f"Error scraping website {url}: {str(e)}"
    
    @tool
    def get_website_summary(url: str) -> str:
        """Get a summary of a website including title, description, and key content."""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return "Invalid URL provided."
            
            # Add https if no scheme provided
            if not parsed.scheme:
                url = f"https://{url}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "No title found"
            
            # Extract meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '').strip() if meta_desc else "No description found"
            
            # Extract main content (try to find main content area)
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
            if main_content:
                # Remove script and style elements
                for script in main_content(["script", "style"]):
                    script.decompose()
                
                content_text = main_content.get_text()
                # Clean up whitespace
                lines = (line.strip() for line in content_text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                content = ' '.join(chunk for chunk in chunks if chunk)
                
                # Truncate content
                if len(content) > 1000:
                    content = content[:1000] + "..."
            else:
                content = "No main content found"
            
            summary = f"**{title_text}**\n\n"
            summary += f"URL: {url}\n\n"
            summary += f"Description: {description}\n\n"
            summary += f"Content Preview:\n{content}"
            
            return summary
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting website summary {url}: {e}")
            return f"Error accessing website {url}: {str(e)}"
        except Exception as e:
            logger.error(f"Error getting website summary {url}: {e}")
            return f"Error getting website summary {url}: {str(e)}"
    
    @tool
    def extract_links(url: str, max_links: int = 10) -> str:
        """Extract all links from a webpage."""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return "Invalid URL provided."
            
            # Add https if no scheme provided
            if not parsed.scheme:
                url = f"https://{url}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all links
            links = soup.find_all('a', href=True)
            
            if not links:
                return f"No links found on {url}"
            
            # Extract and format links
            link_list = []
            for link in links[:max_links]:
                href = link.get('href')
                text = link.get_text().strip()
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = urljoin(url, href)
                elif not href.startswith(('http://', 'https://')):
                    href = urljoin(url, href)
                
                link_list.append({
                    'text': text or href,
                    'url': href
                })
            
            response = f"Links found on {url}:\n\n"
            for i, link in enumerate(link_list, 1):
                response += f"{i}. **{link['text']}**\n   {link['url']}\n\n"
            
            return response
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error extracting links from {url}: {e}")
            return f"Error accessing website {url}: {str(e)}"
        except Exception as e:
            logger.error(f"Error extracting links from {url}: {e}")
            return f"Error extracting links from {url}: {str(e)}"
    
    @tool
    def get_page_title(url: str) -> str:
        """Get the title of a webpage."""
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return "Invalid URL provided."
            
            # Add https if no scheme provided
            if not parsed.scheme:
                url = f"https://{url}"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = soup.find('title')
            if title:
                title_text = title.get_text().strip()
                return f"Title of {url}: {title_text}"
            else:
                return f"No title found for {url}"
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error getting page title {url}: {e}")
            return f"Error accessing website {url}: {str(e)}"
        except Exception as e:
            logger.error(f"Error getting page title {url}: {e}")
            return f"Error getting page title {url}: {str(e)}"
