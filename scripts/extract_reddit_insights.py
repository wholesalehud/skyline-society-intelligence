#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "praw>=7.7.1",
#     "pytz>=2024.1",
#     "python-dotenv>=1.0.0",
# ]
# ///

"""
Reddit Insights Extractor for Skyline Society
Extracts real comments and discussions about proposals, anniversaries, events in Raleigh
Uses PRAW (Python Reddit API Wrapper) with proven patterns from trading_intel_v2
"""

import praw
import json
import sys
import os
from datetime import datetime
from collections import Counter
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

def extract_reddit_insights(keywords, subreddits, min_score=5, limit=100):
    """
    Extract Reddit discussions and sentiment for luxury event keywords

    Args:
        keywords: List of search terms (e.g., ["proposal venue", "anniversary dinner", "luxury event"])
        subreddits: List of subreddits to search (e.g., ["raleigh", "WeddingPlanning"])
        min_score: Minimum upvotes to consider quality content
        limit: Max posts to analyze per keyword

    Returns:
        Structured insights about wants, problems, and opportunities
    """

    # Initialize Reddit using credentials from .env
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'SkylineSocietyResearch:v1.0')

    if not client_id or not client_secret:
        print("\n❌ ERROR: Reddit API credentials not found!")
        print("\n📝 TO FIX:")
        print("   1. Go to https://www.reddit.com/prefs/apps")
        print("   2. Create a new 'script' app")
        print("   3. Copy client_id and client_secret")
        print("   4. Update .env file with your credentials")
        print("\n   Or use the existing credentials already in .env\n")
        sys.exit(1)

    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    print(f"✅ Connected to Reddit as: {user_agent}\n")

    all_insights = {
        'timestamp': datetime.now().isoformat(),
        'keywords_searched': keywords,
        'subreddits_searched': subreddits,
        'total_posts_analyzed': 0,
        'total_comments_analyzed': 0,
        'insights': []
    }

    for keyword in keywords:
        print(f"\n🔍 Searching for: '{keyword}'")
        keyword_data = {
            'keyword': keyword,
            'posts': [],
            'common_wants': [],
            'common_problems': [],
            'price_mentions': [],
            'competitor_mentions': [],
            'sentiment_positive': 0,
            'sentiment_negative': 0,
            'sentiment_neutral': 0
        }

        for subreddit_name in subreddits:
            try:
                subreddit = reddit.subreddit(subreddit_name)

                # Search posts
                for post in subreddit.search(keyword, limit=limit, sort='relevance', time_filter='year'):

                    # Filter by quality
                    if post.score < min_score:
                        continue

                    all_insights['total_posts_analyzed'] += 1

                    post_data = {
                        'title': post.title,
                        'text': post.selftext[:500] if post.selftext else '',  # First 500 chars
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'url': f"https://reddit.com{post.permalink}",
                        'created': datetime.fromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
                        'subreddit': subreddit_name,
                        'top_comments': []
                    }

                    # Get top comments (real sentiment!)
                    post.comments.replace_more(limit=0)  # Don't expand all "more comments"
                    top_comments = sorted(post.comments.list(), key=lambda x: x.score, reverse=True)[:10]

                    for comment in top_comments:
                        if hasattr(comment, 'body') and comment.score > 2:
                            all_insights['total_comments_analyzed'] += 1

                            comment_text = comment.body.lower()

                            post_data['top_comments'].append({
                                'text': comment.body[:300],
                                'score': comment.score,
                                'author': str(comment.author) if comment.author else '[deleted]'
                            })

                            # Extract insights from comments

                            # WANTS - What people are looking for
                            if any(word in comment_text for word in ['looking for', 'need', 'want', 'recommend', 'suggestion']):
                                keyword_data['common_wants'].append(comment.body[:200])

                            # PROBLEMS - Pain points
                            if any(word in comment_text for word in ['expensive', 'difficult', 'hard to find', 'disappointed', 'issue', 'problem']):
                                keyword_data['common_problems'].append(comment.body[:200])
                                keyword_data['sentiment_negative'] += 1

                            # PRICE MENTIONS
                            if '$' in comment_text or 'price' in comment_text or 'cost' in comment_text:
                                keyword_data['price_mentions'].append(comment.body[:200])

                            # COMPETITOR MENTIONS (venue names, services)
                            if any(word in comment_text for word in ['peerspace', 'airbnb', 'venue', 'photographer', 'catering']):
                                keyword_data['competitor_mentions'].append(comment.body[:200])

                            # Sentiment (simple heuristic)
                            if any(word in comment_text for word in ['love', 'great', 'amazing', 'perfect', 'beautiful', 'awesome']):
                                keyword_data['sentiment_positive'] += 1
                            elif any(word in comment_text for word in ['bad', 'terrible', 'awful', 'disappointing', 'poor']):
                                keyword_data['sentiment_negative'] += 1
                            else:
                                keyword_data['sentiment_neutral'] += 1

                    keyword_data['posts'].append(post_data)

                    print(f"  ✓ Found post: '{post.title}' ({post.score} upvotes, {post.num_comments} comments)")

            except Exception as e:
                print(f"  ✗ Error searching r/{subreddit_name}: {e}")
                continue

        all_insights['insights'].append(keyword_data)

    return all_insights


def analyze_insights(insights):
    """
    Analyze extracted insights and generate actionable recommendations
    """

    print("\n\n📊 ANALYSIS RESULTS\n" + "="*60 + "\n")

    for keyword_data in insights['insights']:
        keyword = keyword_data['keyword']

        print(f"\n🔑 Keyword: '{keyword}'")
        print(f"   Posts found: {len(keyword_data['posts'])}")
        print(f"   Sentiment: {keyword_data['sentiment_positive']} positive, {keyword_data['sentiment_negative']} negative, {keyword_data['sentiment_neutral']} neutral")

        # Top wants
        if keyword_data['common_wants']:
            print(f"\n   🎯 WHAT PEOPLE WANT (Top 5):")
            for i, want in enumerate(keyword_data['common_wants'][:5], 1):
                print(f"      {i}. {want[:150]}...")

        # Top problems
        if keyword_data['common_problems']:
            print(f"\n   ⚠️  COMMON PROBLEMS (Top 5):")
            for i, problem in enumerate(keyword_data['common_problems'][:5], 1):
                print(f"      {i}. {problem[:150]}...")

        # Price insights
        if keyword_data['price_mentions']:
            print(f"\n   💰 PRICE DISCUSSIONS (Top 3):")
            for i, price_mention in enumerate(keyword_data['price_mentions'][:3], 1):
                print(f"      {i}. {price_mention[:150]}...")

        # Competitors mentioned
        if keyword_data['competitor_mentions']:
            print(f"\n   🏢 COMPETITORS MENTIONED (Top 3):")
            for i, competitor in enumerate(keyword_data['competitor_mentions'][:3], 1):
                print(f"      {i}. {competitor[:150]}...")

    print("\n" + "="*60)
    print(f"\n📈 TOTAL: Analyzed {insights['total_posts_analyzed']} posts and {insights['total_comments_analyzed']} comments")


def generate_content_ideas(insights):
    """
    Generate blog post and TikTok ideas from real Reddit insights
    """

    print("\n\n💡 CONTENT IDEAS (Data-Driven)\n" + "="*60 + "\n")

    blog_ideas = []
    tiktok_ideas = []

    for keyword_data in insights['insights']:
        keyword = keyword_data['keyword']

        # Blog ideas from common wants
        if keyword_data['common_wants']:
            blog_ideas.append(f"How to Find the Perfect {keyword.title()} in Raleigh (2025 Guide)")
            blog_ideas.append(f"Common Mistakes When Choosing a {keyword.title()}")

        # Blog ideas from problems
        if keyword_data['common_problems']:
            blog_ideas.append(f"Why {keyword.title()} is So Hard to Find in Raleigh (And How We Solved It)")

        # TikTok ideas from sentiment
        if keyword_data['sentiment_negative'] > keyword_data['sentiment_positive']:
            tiktok_ideas.append(f"POV: You're searching for '{keyword}' in Raleigh and everything is either booked or expensive...")
            tiktok_ideas.append(f"I listened to your complaints about {keyword} and built the solution")

        # TikTok from price discussions
        if keyword_data['price_mentions']:
            tiktok_ideas.append(f"Let's talk about {keyword} pricing in Raleigh (honest breakdown)")

    print("📝 BLOG POST IDEAS (Top 10):\n")
    for i, idea in enumerate(blog_ideas[:10], 1):
        print(f"   {i}. {idea}")

    print("\n🎬 TIKTOK IDEAS (Top 10):\n")
    for i, idea in enumerate(tiktok_ideas[:10], 1):
        print(f"   {i}. {idea}")


def main():
    """
    Main execution: Extract insights for Skyline Society
    """

    print("🚀 Skyline Society Reddit Intelligence Extractor\n")
    print("Extracting real wants, problems, and opportunities from Reddit...\n")

    # Define search parameters (customize these!)
    keywords = [
        "proposal venue raleigh",
        "anniversary dinner raleigh",
        "luxury event space raleigh",
        "private dining raleigh",
        "rooftop venue raleigh",
        "photoshoot location raleigh",
        "intimate wedding raleigh",
        "birthday party venue raleigh"
    ]

    subreddits = [
        "raleigh",
        "WeddingPlanning",
        "weddingplanning",  # Both caps versions exist
        "engaged",
        "wedding",
        "raleighweddings"  # If it exists
    ]

    # Extract insights
    insights = extract_reddit_insights(
        keywords=keywords,
        subreddits=subreddits,
        min_score=3,  # At least 3 upvotes (quality filter)
        limit=50      # Max 50 posts per keyword (adjust based on rate limits)
    )

    # Save raw data
    with open('_outputs/reddit_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)

    print(f"\n💾 Saved raw data to: _outputs/reddit_insights.json")

    # Analyze and display
    analyze_insights(insights)

    # Generate content ideas
    generate_content_ideas(insights)

    print("\n✅ Done! Check _outputs/reddit_insights.json for full data.")


if __name__ == "__main__":
    # Create outputs directory
    os.makedirs('_outputs', exist_ok=True)

    # Run main extraction
    main()
