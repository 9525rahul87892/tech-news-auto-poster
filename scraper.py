"""
Tech News Scraper — pulls articles from RSS feeds.
No AI involved. Pure RSS parsing and filtering.
"""

import json
import os
import time
from datetime import datetime, timezone

import feedparser

from config import RSS_FEEDS, LOOKBACK_HOURS, MAX_ARTICLES_PER_RUN, HISTORY_FILE


def load_posted_history(history_file=HISTORY_FILE):
    """Load the set of already-posted article URLs."""
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("posted_urls", []))
    return set()


def save_posted_history(posted_urls, history_file=HISTORY_FILE):
    """Save the updated set of posted article URLs."""
    # Keep only the last 500 URLs to prevent unbounded growth
    urls_list = list(posted_urls)
    if len(urls_list) > 500:
        urls_list = urls_list[-500:]
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump({"posted_urls": urls_list, "last_updated": datetime.now(timezone.utc).isoformat()}, f, indent=2)


def parse_published_date(entry):
    """Extract published date from a feed entry, return as datetime or None."""
    published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if published_parsed:
        try:
            return datetime(*published_parsed[:6], tzinfo=timezone.utc)
        except (ValueError, TypeError):
            return None
    return None


def clean_summary(raw_summary):
    """Strip HTML tags from summary for a clean text version."""
    if not raw_summary:
        return ""
    # Simple HTML tag removal (no external deps needed)
    import re
    clean = re.sub(r"<[^>]+>", "", raw_summary)
    clean = clean.strip()
    # Truncate to ~200 chars for LinkedIn readability
    if len(clean) > 200:
        clean = clean[:197] + "..."
    return clean


def scrape_feeds():
    """
    Scrape all configured RSS feeds and return recent articles.
    
    Returns:
        list[dict]: Articles with keys: title, link, source, summary, published
    """
    now = datetime.now(timezone.utc)
    cutoff_timestamp = now.timestamp() - (LOOKBACK_HOURS * 3600)
    posted_urls = load_posted_history()
    
    articles = []
    
    for feed_config in RSS_FEEDS:
        feed_name = feed_config["name"]
        feed_url = feed_config["url"]
        
        print(f"  📡 Fetching: {feed_name}...")
        
        try:
            feed = feedparser.parse(feed_url)
            
            if feed.bozo and not feed.entries:
                print(f"  ⚠️  Failed to parse {feed_name}: {feed.bozo_exception}")
                continue
            
            for entry in feed.entries:
                link = entry.get("link", "")
                title = entry.get("title", "").strip()
                
                if not link or not title:
                    continue
                
                # Skip already-posted articles
                if link in posted_urls:
                    continue
                
                # Check publication date
                pub_date = parse_published_date(entry)
                if pub_date and pub_date.timestamp() < cutoff_timestamp:
                    continue
                
                # Extract and clean summary
                raw_summary = entry.get("summary", "") or entry.get("description", "")
                summary = clean_summary(raw_summary)
                
                articles.append({
                    "title": title,
                    "link": link,
                    "source": feed_name,
                    "summary": summary if summary else f"Latest from {feed_name}",
                    "published": pub_date.isoformat() if pub_date else now.isoformat(),
                })
                
        except Exception as e:
            print(f"  ❌ Error fetching {feed_name}: {e}")
            continue
    
    # Sort by most recent first
    articles.sort(key=lambda a: a["published"], reverse=True)
    
    # Cap the results
    articles = articles[:MAX_ARTICLES_PER_RUN]
    
    print(f"\n  ✅ Found {len(articles)} new articles across all feeds")
    return articles


if __name__ == "__main__":
    print("🔍 Running scraper standalone test...\n")
    results = scrape_feeds()
    for i, article in enumerate(results[:5], 1):
        print(f"\n--- Article {i} ---")
        print(f"  Title:   {article['title']}")
        print(f"  Source:  {article['source']}")
        print(f"  Link:    {article['link']}")
        print(f"  Summary: {article['summary'][:100]}...")
