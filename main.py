"""
Main Orchestrator — ties scraper and poster together.
Run this script to scrape news and post to LinkedIn.
"""

import argparse
import sys
from datetime import datetime, timezone

from scraper import scrape_feeds, load_posted_history, save_posted_history
from poster import post_to_linkedin
from config import POSTS_PER_RUN


def run(dry_run=False):
    """Main orchestration: scrape → pick top articles → post."""
    
    print("=" * 60)
    print(f"🚀 Tech News Auto-Poster")
    print(f"   Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"   Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    print("=" * 60)
    
    # Step 1: Scrape feeds
    print("\n📡 Step 1: Scraping RSS feeds...")
    articles = scrape_feeds()
    
    if not articles:
        print("\n⚠️  No new articles found. Nothing to post.")
        print("   This can happen if all recent articles were already posted.")
        return 0
    
    # Step 2: Pick top article(s) and post
    print(f"\n📝 Step 2: Posting top {POSTS_PER_RUN} article(s) to LinkedIn...")
    
    posted_urls = load_posted_history()
    success_count = 0
    
    for article in articles[:POSTS_PER_RUN]:
        print(f"\n  📰 Posting: {article['title']}")
        print(f"     Source:  {article['source']}")
        
        success = post_to_linkedin(article, dry_run=dry_run)
        
        if success:
            posted_urls.add(article["link"])
            success_count += 1
    
    # Step 3: Save history (even in dry-run to test the mechanism)
    if success_count > 0:
        save_posted_history(posted_urls)
        print(f"\n💾 Step 3: Updated posted history ({len(posted_urls)} total URLs tracked)")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Done! Posted {success_count}/{POSTS_PER_RUN} article(s)")
    print("=" * 60)
    
    return 0 if success_count > 0 else 1


def main():
    parser = argparse.ArgumentParser(
        description="Auto Tech News Scraper & LinkedIn Poster"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape and format posts without actually posting to LinkedIn",
    )
    args = parser.parse_args()
    
    try:
        exit_code = run(dry_run=args.dry_run)
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
