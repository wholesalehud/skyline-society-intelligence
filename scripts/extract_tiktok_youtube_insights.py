#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "yt-dlp>=2024.1.0",
#     "pytz>=2024.1",
# ]
# ///

"""
TikTok/YouTube Comment Extractor for Skyline Society
Extracts comments from viral proposal/event content to understand:
- What people want in proposals/events
- Common questions/concerns
- Trending aesthetics and themes
Uses yt-dlp with proven patterns from trading_intel_v2
"""

import yt_dlp
import json
import sys
from datetime import datetime
from collections import Counter

def extract_comments_from_video(url, max_comments=100):
    """
    Extract comments from TikTok or YouTube video using yt-dlp

    Args:
        url: Video URL (TikTok, YouTube, Instagram, etc.)
        max_comments: Maximum number of comments to extract

    Returns:
        Video metadata + comments with sentiment data
    """

    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'getcomments': True,  # KEY: Extract comments!
        'extractor_args': {
            'youtube': {
                'comment_sort': ['top'],  # Get top comments first
                'max_comments': [str(max_comments)],
            },
            'tiktok': {
                'max_comments': [str(max_comments)],
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🔍 Extracting from: {url}")
            info = ydl.extract_info(url, download=False)

            video_data = {
                'url': url,
                'title': info.get('title', 'Unknown'),
                'platform': info.get('extractor_key', 'Unknown'),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'comment_count': info.get('comment_count', 0),
                'description': info.get('description', '')[:500],
                'upload_date': info.get('upload_date', 'Unknown'),
                'duration': info.get('duration', 0),
                'comments': [],
                'extracted_at': datetime.now().isoformat()
            }

            # Extract comments
            if 'comments' in info and info['comments']:
                for comment in info['comments'][:max_comments]:
                    comment_data = {
                        'text': comment.get('text', ''),
                        'author': comment.get('author', 'Unknown'),
                        'like_count': comment.get('like_count', 0),
                        'timestamp': comment.get('timestamp', 0),
                        'is_favorited': comment.get('is_favorited', False)
                    }
                    video_data['comments'].append(comment_data)

                print(f"  ✓ Extracted {len(video_data['comments'])} comments")
            else:
                print(f"  ⚠️  No comments found (may be disabled or need auth)")

            return video_data

    except Exception as e:
        print(f"  ✗ Error extracting from {url}: {e}")
        return None


def analyze_comment_insights(comments):
    """
    Analyze comments to extract wants, problems, and sentiment

    Returns:
        Structured insights from comment analysis
    """

    insights = {
        'total_comments': len(comments),
        'wants': [],  # What people want/desire
        'problems': [],  # Pain points mentioned
        'questions': [],  # Questions people ask
        'price_mentions': [],  # Any price/cost discussions
        'location_mentions': [],  # Location requests
        'sentiment_positive': 0,
        'sentiment_negative': 0,
        'sentiment_neutral': 0,
        'top_keywords': [],
        'engagement_triggers': []  # What makes people comment
    }

    all_text = ' '.join([c['text'].lower() for c in comments])
    words = all_text.split()
    word_freq = Counter(words)

    # Most common keywords (excluding stopwords)
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'this', 'that', 'it', 'i', 'you', 'so', 'my', 'me', 'your'}
    insights['top_keywords'] = [
        word for word, count in word_freq.most_common(20)
        if word not in stopwords and len(word) > 3
    ]

    for comment in comments:
        text = comment['text'].lower()

        # WANTS/DESIRES
        if any(phrase in text for phrase in ['i want', 'i need', 'i wish', 'where can i', 'how do i get', 'i would love']):
            insights['wants'].append(comment['text'])

        # PROBLEMS/PAIN POINTS
        if any(phrase in text for phrase in ['too expensive', 'cant afford', 'hard to find', 'wish it was', 'if only', 'but', 'unfortunately']):
            insights['problems'].append(comment['text'])
            insights['sentiment_negative'] += 1

        # QUESTIONS
        if '?' in text:
            insights['questions'].append(comment['text'])

        # PRICE MENTIONS
        if any(word in text for word in ['$', 'price', 'cost', 'expensive', 'cheap', 'affordable', 'budget', 'how much']):
            insights['price_mentions'].append(comment['text'])

        # LOCATION MENTIONS
        if any(word in text for word in ['raleigh', 'durham', 'charlotte', 'nc', 'north carolina', 'near me', 'where is this']):
            insights['location_mentions'].append(comment['text'])

        # SENTIMENT (simple heuristic)
        positive_words = ['love', 'amazing', 'beautiful', 'perfect', 'gorgeous', 'stunning', 'dream', 'goals', '😍', '❤️', '🔥']
        negative_words = ['hate', 'ugly', 'bad', 'terrible', 'awful', 'disappointing', 'meh', '😢', '😡']

        if any(word in text for word in positive_words):
            insights['sentiment_positive'] += 1
        elif any(word in text for word in negative_words):
            insights['sentiment_negative'] += 1
        else:
            insights['sentiment_neutral'] += 1

        # ENGAGEMENT TRIGGERS (high-engagement comments)
        if comment['like_count'] > 10:  # Popular comments
            insights['engagement_triggers'].append({
                'text': comment['text'],
                'likes': comment['like_count']
            })

    return insights


def extract_batch_insights(urls, category="proposal"):
    """
    Extract insights from multiple videos in a category

    Args:
        urls: List of video URLs
        category: Category name (proposal, wedding, event, etc.)

    Returns:
        Aggregated insights across all videos
    """

    batch_insights = {
        'category': category,
        'total_videos': len(urls),
        'total_comments': 0,
        'videos': [],
        'aggregated_insights': {
            'all_wants': [],
            'all_problems': [],
            'all_questions': [],
            'all_price_mentions': [],
            'all_location_mentions': [],
            'top_keywords_overall': [],
            'sentiment_summary': {'positive': 0, 'negative': 0, 'neutral': 0}
        }
    }

    for url in urls:
        video_data = extract_comments_from_video(url, max_comments=100)

        if video_data and video_data['comments']:
            insights = analyze_comment_insights(video_data['comments'])

            video_summary = {
                'url': url,
                'title': video_data['title'],
                'platform': video_data['platform'],
                'views': video_data['view_count'],
                'likes': video_data['like_count'],
                'comment_count': len(video_data['comments']),
                'insights': insights
            }

            batch_insights['videos'].append(video_summary)
            batch_insights['total_comments'] += len(video_data['comments'])

            # Aggregate insights
            batch_insights['aggregated_insights']['all_wants'].extend(insights['wants'])
            batch_insights['aggregated_insights']['all_problems'].extend(insights['problems'])
            batch_insights['aggregated_insights']['all_questions'].extend(insights['questions'])
            batch_insights['aggregated_insights']['all_price_mentions'].extend(insights['price_mentions'])
            batch_insights['aggregated_insights']['all_location_mentions'].extend(insights['location_mentions'])

            # Aggregate sentiment
            batch_insights['aggregated_insights']['sentiment_summary']['positive'] += insights['sentiment_positive']
            batch_insights['aggregated_insights']['sentiment_summary']['negative'] += insights['sentiment_negative']
            batch_insights['aggregated_insights']['sentiment_summary']['neutral'] += insights['sentiment_neutral']

    return batch_insights


def generate_content_strategy(batch_insights):
    """
    Generate blog and TikTok content ideas from extracted insights
    """

    print("\n\n💡 CONTENT STRATEGY (Based on Real Comments)\n" + "="*60 + "\n")

    insights = batch_insights['aggregated_insights']

    # Blog ideas from wants
    print("📝 BLOG POST IDEAS (Address What People Want):\n")
    if insights['all_wants']:
        wants_sample = insights['all_wants'][:5]
        for i, want in enumerate(wants_sample, 1):
            print(f"   {i}. How to Get {extract_topic(want)} (Complete Guide)")

    # Blog ideas from problems
    print("\n📝 BLOG POST IDEAS (Solve Their Problems):\n")
    if insights['all_problems']:
        problems_sample = insights['all_problems'][:5]
        for i, problem in enumerate(problems_sample, 1):
            print(f"   {i}. Why {extract_topic(problem)} is Hard (And Our Solution)")

    # TikTok ideas from questions
    print("\n🎬 TIKTOK IDEAS (Answer Their Questions):\n")
    if insights['all_questions']:
        questions_sample = insights['all_questions'][:5]
        for i, question in enumerate(questions_sample, 1):
            clean_q = question.replace('?', '').strip()
            print(f"   {i}. '{clean_q}' - Let me answer that...")

    # TikTok ideas from location mentions
    print("\n🎬 TIKTOK IDEAS (Local SEO):\n")
    if insights['all_location_mentions']:
        print(f"   1. Yes, we're in Raleigh! Here's what makes our location special...")
        print(f"   2. Raleigh vs Durham vs Charlotte - where should you have your event?")
        print(f"   3. Downtown Raleigh hidden gems (including us)")

    # Sentiment-based strategy
    sentiment = insights['sentiment_summary']
    total = sentiment['positive'] + sentiment['negative'] + sentiment['neutral']
    if total > 0:
        positive_pct = (sentiment['positive'] / total) * 100

        print(f"\n📊 SENTIMENT: {positive_pct:.1f}% positive")

        if positive_pct > 70:
            print("   → Strategy: Amplify the love! Share testimonials, user-generated content")
        elif positive_pct < 40:
            print("   → Strategy: Address concerns! Create content solving pain points")
        else:
            print("   → Strategy: Balanced approach - show value while addressing concerns")


def extract_topic(text):
    """Helper to extract topic from a want/problem statement"""
    # Simple extraction - could be improved with NLP
    if 'venue' in text.lower():
        return 'the Perfect Venue'
    elif 'proposal' in text.lower():
        return 'a Memorable Proposal'
    elif 'price' in text.lower() or 'cost' in text.lower():
        return 'Affordable Event Planning'
    else:
        return 'This'


def main():
    """
    Main execution: Extract TikTok/YouTube insights for Skyline Society
    """

    print("🚀 Skyline Society TikTok/YouTube Intelligence Extractor\n")
    print("Extracting real comments to understand wants, problems, and sentiment...\n")

    # Example URLs to analyze (replace with actual trending content)
    proposal_videos = [
        # "https://www.tiktok.com/@user/video/123456789",  # Viral proposal video
        # "https://www.youtube.com/watch?v=EXAMPLE1",      # Proposal planning video
        # "https://www.youtube.com/watch?v=EXAMPLE2",      # Raleigh venue tour
    ]

    event_videos = [
        # "https://www.tiktok.com/@user/video/987654321",  # Event setup video
        # "https://www.youtube.com/watch?v=EXAMPLE3",      # Event planning tips
    ]

    if not proposal_videos and not event_videos:
        print("⚠️  No URLs provided yet. Add URLs to analyze in the script.")
        print("\n📝 HOW TO USE:")
        print("   1. Find viral TikToks/YouTube videos about proposals, events, venues")
        print("   2. Add their URLs to the proposal_videos and event_videos lists")
        print("   3. Run this script to extract comments")
        print("   4. Get content ideas based on what people actually want/ask")
        print("\n   Example URLs to search for:")
        print("   - TikTok: Search 'raleigh proposal', 'event venue tour', 'luxury dinner setup'")
        print("   - YouTube: 'proposal planning', 'how to plan an event', 'venue tour raleigh'")
        return

    # Extract insights
    proposal_insights = extract_batch_insights(proposal_videos, category="proposal")
    event_insights = extract_batch_insights(event_videos, category="events")

    # Save raw data
    with open('_outputs/tiktok_youtube_insights.json', 'w') as f:
        json.dump({
            'proposal_insights': proposal_insights,
            'event_insights': event_insights,
            'extracted_at': datetime.now().isoformat()
        }, f, indent=2)

    print(f"\n💾 Saved raw data to: _outputs/tiktok_youtube_insights.json")

    # Generate content strategy
    if proposal_insights['total_comments'] > 0:
        generate_content_strategy(proposal_insights)

    print("\n✅ Done! Add more URLs to analyze more content.")


if __name__ == "__main__":
    import os
    os.makedirs('_outputs', exist_ok=True)
    main()
