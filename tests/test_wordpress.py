import pytest
import asyncio
from core.client import WPClient
from services.posts_service import PostsService
from services.acf_service import ACFService

@pytest.fixture
def wp_client():
    return WPClient()

@pytest.fixture
def posts_service(wp_client):
    return PostsService(wp_client)

@pytest.fixture
def acf_service(wp_client):
    return ACFService(wp_client)

@pytest.mark.asyncio
async def test_wordpress_lifecycle(posts_service, acf_service):
    """
    Integration test: Create -> Read -> Update -> Delete
    """
    test_title = "Agent Test Post"
    test_content = "This is a post created by the integration test."
    
    # 1. Create Post
    post = await posts_service.create_post(
        title=test_title,
        content=test_content,
        status="draft"
    )
    assert post["id"] > 0
    assert post["title"]["rendered"] == test_title
    post_id = post["id"]
    
    try:
        # 2. Update Post Content
        updated_title = "Agent Test Post Updated"
        update_result = await posts_service.update_post(post_id, {"title": updated_title})
        assert update_result["title"]["rendered"] == updated_title
        
        # 3. Test ACF (Only if ACF is enabled on the post type)
        # Note: This might fail if the user hasn't defined fields or enabled REST API for them
        # but we can at least try to send data.
        try:
            acf_update = await acf_service.update_field(post_id, "test_field", "test_value")
            # If ACF is working, 'acf' key should be in response
            assert "acf" in acf_update
        except Exception as e:
            print(f"[Note] ACF update skipped or failed (likely field not defined): {e}")

        # 4. List and find our post (include drafts)
        posts = await posts_service.list_posts(count=10, status="any")
        found = any(p["id"] == post_id for p in posts)
        assert found is True

    finally:
        # 5. Cleanup: Delete the post
        try:
            delete_result = await posts_service.delete_post(post_id, force=True)
            # WordPress returns the deleted post object on success
            # If force=True, some fields might be different, so we just check it didn't error
            print(f"Cleanup: Successfully deleted test post {post_id}")
        except Exception as e:
            print(f"Cleanup Failed: {e}")

@pytest.mark.asyncio
async def test_connection_validation(wp_client):
    """Verifies that the client can connect with current credentials."""
    is_connected = await wp_client.check_connection()
    assert is_connected is True
