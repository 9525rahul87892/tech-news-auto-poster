"""
Configuration for the Tech News Scraper & LinkedIn Poster.
No AI involved — just RSS feeds and formatting.
"""

# ─── RSS Feeds ───────────────────────────────────────────────
# Curated list of top tech news RSS feeds
RSS_FEEDS = [
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com/feed/",
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com/rss/index.xml",
    },
    {
        "name": "Ars Technica",
        "url": "https://feeds.arstechnica.com/arstechnica/index",
    },
    {
        "name": "Wired",
        "url": "https://www.wired.com/feed/rss",
    },
    {
        "name": "Hacker News (Best)",
        "url": "https://hnrss.org/best",
    },
    {
        "name": "MIT Technology Review",
        "url": "https://www.technologyreview.com/feed/",
    },
    {
        "name": "Engadget",
        "url": "https://www.engadget.com/rss.xml",
    },
]

# ─── Scraper Settings ────────────────────────────────────────
# How far back (in hours) to look for articles
LOOKBACK_HOURS = 3

# Maximum number of articles to consider per scrape run
MAX_ARTICLES_PER_RUN = 20

# ─── Posting Settings ───────────────────────────────────────
# Number of articles to post per run (1 keeps it non-spammy)
POSTS_PER_RUN = 1

# ─── Post Formatting ────────────────────────────────────────
# Template for the LinkedIn post body
# Available placeholders: {title}, {summary}, {source}, {link}
POST_TEMPLATE = """🔥 {title}

{summary}

📰 Source: {source}
🔗 Read more: {link}

#TechNews #Technology #Innovation #Software #StartUps"""

# ─── LinkedIn API ────────────────────────────────────────────
LINKEDIN_API_BASE = "https://api.linkedin.com"
LINKEDIN_POSTS_ENDPOINT = f"{LINKEDIN_API_BASE}/rest/posts"
LINKEDIN_USERINFO_ENDPOINT = f"{LINKEDIN_API_BASE}/v2/userinfo"
LINKEDIN_API_VERSION = "202504"

# ─── File Paths ──────────────────────────────────────────────
HISTORY_FILE = "posted_history.json"
