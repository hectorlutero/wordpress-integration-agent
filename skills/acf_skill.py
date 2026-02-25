import logging
from typing import Dict, Any, Optional
from core.client import WPClient

logger = logging.getLogger(__name__)

class ACFSkill:
    """
    Skill for interacting with Advanced Custom Fields (ACF).
    Requires the ACF REST API toggle to be enabled in WordPress.
    """
    def __init__(self, client: WPClient):
        self.client = client

    async def get_fields(self, post_id: int) -> Dict[str, Any]:
        """
        Retrieves all ACF fields for a specific post.
        """
        # If ACF REST API is enabled, fields are available under the 'acf' key.
        # We fetch the post and extract the 'acf' object.
        post = await self.client.get(f"posts/{post_id}")
        return post.get("acf", {})

    async def update_field(self, post_id: int, field_name: str, value: Any) -> Dict[str, Any]:
        """
        Updates a specific ACF field for a post.
        """
        data = {
            "acf": {
                field_name: value
            }
        }
        logger.info(f"Updating ACF field '{field_name}' for post {post_id}")
        return await self.client.post(f"posts/{post_id}", data=data)

    async def update_fields(self, post_id: int, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Updates multiple ACF fields for a post.
        """
        data = {
            "acf": fields
        }
        logger.info(f"Updating multiple ACF fields for post {post_id}")
        return await self.client.post(f"posts/{post_id}", data=data)
