# 🤖 WordPress Integration Agent

A powerful, Python-based agent designed to automate and manage WordPress websites via the REST API. This agent provides a modular "Skill" architecture to handle content, custom fields (ACF), and analytics reporting.

## 🚀 Features

- **Authenticated API Client:** Secure communication using WordPress Application Passwords.
- **Posts Management:** CRUD operations for posts and pages.
- **ACF Integration:** Seamless manipulation of Advanced Custom Fields.
- **Analytics (Coming Soon):** Integration with Google Analytics (GA4) for automated reporting.
- **Secure by Design:** Environment-based configuration with template protection for public repositories.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-repo/wordpress-integration-agent.git
   cd wordpress-integration-agent
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuration

1. **Create a `.env` file:**
   Copy the provided template and fill in your credentials.
   ```bash
   cp .env.example .env
   ```

2. **WordPress Credentials:**
   - **WP_URL:** The full URL of your WordPress site (e.g., `https://example.com`).
   - **WP_USERNAME:** Your WordPress admin email or username.
   - **WP_APP_PASSWORD:** An **Application Password** generated from your WordPress user profile (Users -> Profile -> Application Passwords).

## 📖 Usage

### Testing the Connection
Run the connection test to verify your credentials:
```bash
python3 test_connection.py
```

### Basic Implementation Example
```python
import asyncio
from core.client import WPClient
from skills.posts_skill import PostsSkill

async def main():
    client = WPClient()
    posts_skill = PostsSkill(client)

    # List recent posts
    posts = await posts_skill.list_posts(count=5)
    for post in posts:
        print(f"Title: {post['title']['rendered']}")

    # Create a draft
    new_post = await posts_skill.create_post(
        title="Automated Post",
        content="Hello from the Agent!",
        status="draft"
    )
    print(f"Created post ID: {new_post['id']}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 📂 Project Structure

- `core/`: Base logic, including the API `client.py` and `config.py`.
- `skills/`: Modular components for specific tasks (Posts, ACF, Analytics).
- `reports/`: Default directory for generated CSV/Excel exports.
- `.env`: (Ignored) Your private configuration.

## 🗺️ Roadmap

- [x] Phase 1: Security & Foundation
- [x] Phase 2: Content & ACF Skills
- [ ] Phase 3: Analytics & Reporting Engine
- [ ] Phase 4: Interactive CLI Chat Interface

---
*Created by [Hector Lutero](https://github.com/hectorsiman)*
