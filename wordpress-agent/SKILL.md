---
name: wordpress-agent
description: Manage WordPress websites including posts, pages, Advanced Custom Fields (ACF), and GA4 analytics. Use when you need to automate content creation, update custom fields, or generate traffic reports for WordPress sites.
---

# WordPress Agent Skill

This skill allows you to interact with WordPress websites using a set of pre-built Python services.

## Prerequisites

- **Python 3.10+**: Ensure `requirements.txt` dependencies are installed.
- **Environment**: A valid `.env` file must be present at the root with WordPress credentials.
- **ACF**: The "Show in REST API" toggle must be enabled in WordPress for ACF fields to be accessible.

## Core Services

The skill leverages the following Python modules located in the `services/` directory:

- **PostsService (`services/posts_service.py`)**: CRUD for posts/pages.
- **ACFService (`services/acf_service.py`)**: Manipulation of Advanced Custom Fields.
- **AnalyticsService (`services/analytics_service.py`)**: Fetching GA4 data.
- **ReportService (`services/report_service.py`)**: Exporting data to CSV/Excel.

## Workflows

### 1. Managing Content
To list, create, or update posts, use the `PostsService`.
- **Example**: To list 5 recent posts:
  ```python
  from core.client import WPClient
  from services.posts_service import PostsService
  client = WPClient()
  service = PostsService(client)
  posts = await service.list_posts(count=5)
  ```

### 2. Updating Custom Fields
To update ACF fields, use the `ACFService`.
- **Example**: Update a field 'price' for post 123:
  ```python
  from services.acf_service import ACFService
  service = ACFService(client)
  await service.update_field(123, 'price', '99.99')
  ```

### 3. Generating Traffic Reports
To generate a CSV report of the last 30 days:
1. Fetch data using `AnalyticsService`.
2. Export using `ReportService`.

## Guidelines

- **Always verify connection**: Use `client.check_connection()` before performing bulk operations.
- **Draft first**: When creating content, prefer `status='draft'` unless explicitly asked for 'publish'.
- **Security**: Never log the `.env` contents or the `Authorization` headers.
- **Cleanup**: If running tests or temporary tasks, use the `delete_post(post_id, force=True)` method.
