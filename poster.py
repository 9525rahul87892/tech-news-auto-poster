"""
LinkedIn Poster — posts articles to LinkedIn via the Posts API.
Uses OAuth2 access token. No AI involved.
"""

import os
import requests

from config import (
    LINKEDIN_POSTS_ENDPOINT,
    LINKEDIN_USERINFO_ENDPOINT,
    LINKEDIN_API_VERSION,
    POST_TEMPLATE,
)


def get_access_token():
    """Get LinkedIn access token from environment variable."""
    token = os.environ.get("LINKEDIN_ACCESS_TOKEN")
    if not token:
        raise EnvironmentError(
            "LINKEDIN_ACCESS_TOKEN environment variable is not set.\n"
            "See SETUP_GUIDE.md for instructions on obtaining your token."
        )
    return token


def get_user_urn(access_token):
    """Fetch the authenticated user's LinkedIn URN (person ID)."""
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    
    response = requests.get(LINKEDIN_USERINFO_ENDPOINT, headers=headers, timeout=10)
    
    if response.status_code != 200:
        raise Exception(
            f"Failed to get user info (HTTP {response.status_code}): {response.text}"
        )
    
    data = response.json()
    user_sub = data.get("sub")
    
    if not user_sub:
        raise Exception(f"Could not find user ID in response: {data}")
    
    return f"urn:li:person:{user_sub}"


def format_post(article):
    """Format an article into a LinkedIn post using the template."""
    return POST_TEMPLATE.format(
        title=article["title"],
        summary=article["summary"],
        source=article["source"],
        link=article["link"],
    )


def post_to_linkedin(article, dry_run=False):
    """
    Post an article to LinkedIn.
    
    Args:
        article (dict): Article with title, summary, source, link
        dry_run (bool): If True, format and print but don't actually post
    
    Returns:
        bool: True if posted (or dry-run), False on failure
    """
    post_text = format_post(article)
    
    if dry_run:
        print("\n" + "=" * 60)
        print("🧪 DRY RUN — Would post the following to LinkedIn:")
        print("=" * 60)
        print(post_text)
        print("=" * 60)
        return True
    
    try:
        access_token = get_access_token()
        user_urn = get_user_urn(access_token)
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "LinkedIn-Version": LINKEDIN_API_VERSION,
            "X-Restli-Protocol-Version": "2.0.0",
        }
        
        payload = {
            "author": user_urn,
            "commentary": post_text,
            "visibility": "PUBLIC",
            "distribution": {
                "feedDistribution": "MAIN_FEED",
                "targetEntities": [],
                "thirdPartyDistributionChannels": [],
            },
            "lifecycleState": "PUBLISHED",
            "isReshareDisabledByAuthor": False,
        }
        
        response = requests.post(
            LINKEDIN_POSTS_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=15,
        )
        
        if response.status_code in (200, 201):
            print(f"  ✅ Successfully posted to LinkedIn!")
            print(f"     Title: {article['title']}")
            return True
        else:
            print(f"  ❌ LinkedIn API error (HTTP {response.status_code})")
            print(f"     Response: {response.text}")
            return False
            
    except EnvironmentError as e:
        print(f"  ❌ Configuration error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error posting to LinkedIn: {e}")
        return False


if __name__ == "__main__":
    # Quick test with a dummy article
    test_article = {
        "title": "Test Article — Python Automation",
        "summary": "This is a test post from the auto-poster.",
        "source": "Test Source",
        "link": "https://example.com/test",
    }
    post_to_linkedin(test_article, dry_run=True)
