import logging
import os
from io import BytesIO
from typing import Dict, Any, Optional
from PIL import Image
from core.client import WPClient

logger = logging.getLogger(__name__)

class MediaService:
    """
    Service for processing and uploading media to WordPress.
    Automatically converts images to WebP before upload.
    """
    def __init__(self, client: WPClient):
        self.client = client

    def _convert_to_webp(self, local_path: str, quality: int = 80) -> BytesIO:
        """
        Loads an image from local_path and returns a BytesIO object 
        containing the converted WebP data.
        """
        logger.info(f"Converting {local_path} to WebP...")
        img = Image.open(local_path)
        
        # Ensure we are in RGB mode (handles PNG transparency)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")
            
        webp_io = BytesIO()
        img.save(webp_io, format="WEBP", quality=quality, method=6)
        webp_io.seek(0)
        return webp_io

    async def upload_image(self, local_path: str, alt_text: str = "", title: str = "") -> Dict[str, Any]:
        """
        Converts the image to WebP and uploads it to the WordPress media library.
        Returns the attachment metadata.
        """
        # Convert locally
        filename = os.path.basename(local_path)
        webp_filename = os.path.splitext(filename)[0] + ".webp"
        webp_data = self._convert_to_webp(local_path)

        # Upload using the WPClient specialized method
        result = await self.client.upload_media(
            filename=webp_filename,
            file_data=webp_data.getvalue(),
            mime_type='image/webp'
        )
        
        # If we have extra metadata like alt_text, we perform an update
        if alt_text or title:
            await self.client.post(f"media/{result['id']}", data={
                'alt_text': alt_text,
                'title': title
            })
            
        return result
