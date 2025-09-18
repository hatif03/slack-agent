"""Google services integration tool."""

import os
import logging
from typing import Any, Dict, List, Optional
from langchain_core.tools import BaseTool, tool
from googleapiclient.discovery import build
from google.auth.credentials import Credentials
from google.oauth2.credentials import Credentials as OAuth2Credentials
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request

logger = logging.getLogger(__name__)


class GoogleTool:
    """Google services integration tool for Gmail, Drive, Calendar, etc."""
    
    def __init__(self):
        """Initialize Google tool."""
        self.credentials = None
        self.gmail_service = None
        self.drive_service = None
        self.calendar_service = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load Google credentials from environment or OAuth flow."""
        # Try to load from environment variables first
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
        refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
        
        if client_id and client_secret and refresh_token:
            try:
                self.credentials = OAuth2Credentials(
                    token=None,
                    refresh_token=refresh_token,
                    token_uri="https://oauth2.googleapis.com/token",
                    client_id=client_id,
                    client_secret=client_secret,
                    scopes=[
                        'https://www.googleapis.com/auth/gmail.readonly',
                        'https://www.googleapis.com/auth/drive.readonly',
                        'https://www.googleapis.com/auth/calendar.readonly'
                    ]
                )
                self.credentials.refresh(Request())
                
                # Initialize services
                self.gmail_service = build('gmail', 'v1', credentials=self.credentials)
                self.drive_service = build('drive', 'v3', credentials=self.credentials)
                self.calendar_service = build('calendar', 'v3', credentials=self.credentials)
                
            except Exception as e:
                logger.warning(f"Failed to load Google credentials: {e}")
                self.credentials = None
    
    def get_langchain_tools(self) -> List[BaseTool]:
        """Get LangChain tools for Google services."""
        return [
            self.search_gmail,
            self.list_drive_files,
            self.get_calendar_events,
            self.search_google_docs,
        ]
    
    def get_auth_url(self, user_id: str) -> str:
        """Get Google OAuth URL for authentication."""
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8080/callback")
        
        scopes = [
            'https://www.googleapis.com/auth/gmail.readonly',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/calendar.readonly'
        ]
        
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": client_id,
                    "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [redirect_uri]
                }
            },
            scopes=scopes
        )
        flow.redirect_uri = redirect_uri
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=user_id
        )
        
        return auth_url
    
    @tool
    def search_gmail(query: str, max_results: int = 5) -> str:
        """Search Gmail messages."""
        try:
            if not self.gmail_service:
                return "Google Gmail service not configured. Please set up Google OAuth credentials."
            
            # Search for messages
            results = self.gmail_service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()
            
            messages = results.get('messages', [])
            
            if not messages:
                return f"No emails found for query: {query}"
            
            response = f"Found {len(messages)} emails for '{query}':\n\n"
            
            for message in messages:
                msg = self.gmail_service.users().messages().get(
                    userId='me',
                    id=message['id']
                ).execute()
                
                headers = msg['payload'].get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown Sender')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown Date')
                
                response += f"• **{subject}**\n"
                response += f"  From: {sender}\n"
                response += f"  Date: {date}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching Gmail: {e}")
            return f"Error searching Gmail: {str(e)}"
    
    @tool
    def list_drive_files(query: str = "", max_results: int = 10) -> str:
        """List Google Drive files."""
        try:
            if not self.drive_service:
                return "Google Drive service not configured. Please set up Google OAuth credentials."
            
            # Search for files
            results = self.drive_service.files().list(
                q=query if query else None,
                pageSize=max_results,
                fields="files(id,name,mimeType,createdTime,modifiedTime,webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                return f"No files found for query: {query or 'all files'}"
            
            response = f"Found {len(files)} files in Google Drive:\n\n"
            
            for file in files:
                file_type = file.get('mimeType', 'Unknown')
                created = file.get('createdTime', 'Unknown')
                modified = file.get('modifiedTime', 'Unknown')
                url = file.get('webViewLink', 'No URL')
                
                response += f"• **{file['name']}**\n"
                response += f"  Type: {file_type}\n"
                response += f"  Created: {created}\n"
                response += f"  Modified: {modified}\n"
                response += f"  URL: {url}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error listing Drive files: {e}")
            return f"Error listing Drive files: {str(e)}"
    
    @tool
    def get_calendar_events(max_results: int = 10) -> str:
        """Get upcoming calendar events."""
        try:
            if not self.calendar_service:
                return "Google Calendar service not configured. Please set up Google OAuth credentials."
            
            from datetime import datetime, timedelta
            
            # Get events for the next 7 days
            now = datetime.utcnow()
            time_min = now.isoformat() + 'Z'
            time_max = (now + timedelta(days=7)).isoformat() + 'Z'
            
            events_result = self.calendar_service.events().list(
                calendarId='primary',
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_results,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            
            if not events:
                return "No upcoming events found in the next 7 days."
            
            response = f"Upcoming events (next 7 days):\n\n"
            
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'No Title')
                location = event.get('location', 'No Location')
                
                response += f"• **{summary}**\n"
                response += f"  Time: {start}\n"
                response += f"  Location: {location}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting calendar events: {e}")
            return f"Error getting calendar events: {str(e)}"
    
    @tool
    def search_google_docs(query: str, max_results: int = 5) -> str:
        """Search Google Docs."""
        try:
            if not self.drive_service:
                return "Google Drive service not configured. Please set up Google OAuth credentials."
            
            # Search for Google Docs
            results = self.drive_service.files().list(
                q=f"name contains '{query}' and mimeType='application/vnd.google-apps.document'",
                pageSize=max_results,
                fields="files(id,name,createdTime,modifiedTime,webViewLink)"
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                return f"No Google Docs found for query: {query}"
            
            response = f"Found {len(files)} Google Docs for '{query}':\n\n"
            
            for file in files:
                created = file.get('createdTime', 'Unknown')
                modified = file.get('modifiedTime', 'Unknown')
                url = file.get('webViewLink', 'No URL')
                
                response += f"• **{file['name']}**\n"
                response += f"  Created: {created}\n"
                response += f"  Modified: {modified}\n"
                response += f"  URL: {url}\n\n"
            
            return response
            
        except Exception as e:
            logger.error(f"Error searching Google Docs: {e}")
            return f"Error searching Google Docs: {str(e)}"
