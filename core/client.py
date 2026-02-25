import httpx
import logging
import base64
from typing import Dict, Any, Optional
from core.config import settings

logger = logging.getLogger(__name__)

class WPClient:
    """
    Authenticated Client for WordPress REST API.
    Handles basic CRUD operations and authentication.
    """
    def __init__(self, base_url: str = None, username: str = None, app_password: str = None):
        """
        Initializes the WP Client with configuration.
        """
        self.base_url = (base_url or settings.WP_URL).rstrip("/")
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.username = username or settings.WP_USERNAME
        self.app_password = app_password or settings.WP_APP_PASSWORD
        
        # Prepare Auth Header
        auth_str = f"{self.username}:{self.app_password}"
        encoded_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        self.headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Content-Type": "application/json",
            "User-Agent": "WPIntegrationAgent/1.0"
        }
        
    def _get_async_client(self) -> httpx.AsyncClient:
        """Helper to create an authenticated AsyncClient."""
        return httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Performs a GET request to the WordPress API."""
        async with self._get_async_client() as client:
            url = f"{self.api_url}/{endpoint.lstrip('/')}"
            logger.debug(f"GET {url} params={params}")
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs a POST request to the WordPress API."""
        async with self._get_async_client() as client:
            url = f"{self.api_url}/{endpoint.lstrip('/')}"
            logger.debug(f"POST {url}")
            response = await client.post(url, json=data)
            response.raise_for_status()
            return response.json()

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Performs a DELETE request to the WordPress API."""
        async with self._get_async_client() as client:
            url = f"{self.api_url}/{endpoint.lstrip('/')}"
            logger.debug(f"DELETE {url} params={params}")
            response = await client.delete(url, params=params)
            response.raise_for_status()
            return response.json()

    async def check_connection(self) -> bool:
        """
        Validates the connection and authentication with the WordPress site.
        """
        try:
            # Try to fetch current user data to verify auth
            await self.get("users/me")
            logger.info("WordPress connection successful.")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to WordPress: {e}")
            return False
