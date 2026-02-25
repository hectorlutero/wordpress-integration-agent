import logging
from typing import List, Dict, Any, Optional
from core.client import WPClient

logger = logging.getLogger(__name__)

class PostsService:
    """
    Skill for interacting with WordPress Posts and Pages.
    """
    def __init__(self, client: WPClient):
        self.client = client

    async def list_posts(self, count: int = 10, status: str = "publish") -> List[Dict[str, Any]]:
        """Lists recent posts."""
        params = {
            "per_page": count,
            "status": status,
            "_embed": 1 # Include extra data like featured media, terms, etc.
        }
        return await self.client.get("posts", params=params)

    async def get_post(self, post_id: int) -> Dict[str, Any]:
        """Retrieves a specific post by ID."""
        return await self.client.get(f"posts/{post_id}", params={"_embed": 1})

    async def create_post(self, title: str, content: str, status: str = "draft", **kwargs) -> Dict[str, Any]:
        """Creates a new post."""
        data = {
            "title": title,
            "content": content,
            "status": status,
            **kwargs
        }
        logger.info(f"Creating new post: {title}")
        return await self.client.post("posts", data=data)

    async def update_post(self, post_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing post."""
        logger.info(f"Updating post ID: {post_id}")
        return await self.client.post(f"posts/{post_id}", data=data)

    async def delete_post(self, post_id: int, force: bool = False) -> Dict[str, Any]:
        """Deletes a post (moves to trash by default)."""
        logger.info(f"Deleting post ID: {post_id} (force={force})")
        return await self.client.delete(f"posts/{post_id}", params={"force": force})
