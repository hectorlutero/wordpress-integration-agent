import asyncio
import logging
from core.client import WPClient
from core.config import setup_logging

async def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    client = WPClient()
    logger.info("Testing connection to WordPress...")
    
    if await client.check_connection():
        logger.info("SUCCESS: Authenticated successfully.")
        
        # Optionally, list the last 2 posts to see if it works
        try:
            posts = await client.get("posts", params={"per_page": 2})
            logger.info(f"Retrieved {len(posts)} posts. Titles:")
            for post in posts:
                logger.info(f"- {post['title']['rendered']}")
        except Exception as e:
            logger.error(f"Error retrieving posts: {e}")
    else:
        logger.error("FAILURE: Connection or authentication failed.")

if __name__ == "__main__":
    asyncio.run(main())
