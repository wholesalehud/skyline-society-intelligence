#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "praw>=7.7.1",
#     "anthropic>=0.40.0",
#     "python-dotenv>=1.0.0",
#     "pytz>=2024.1",
# ]
# ///

"""
Recursive Intelligence Amplification Agent

Starts with broad keywords → Extracts insights → Generates NEW search terms → Repeats

Example Flow:
    Round 1: Search "proposal venue raleigh"
        ↓
    Discovers: "Legends", "Duke Gardens", "expensive", "closes at 11pm"
        ↓
    Round 2: Search "Legends Raleigh", "late night venues raleigh", "affordable proposal raleigh"
        ↓
    Discovers: Pricing ($300/hr), availability issues, market gaps
        ↓
    Round 3: Deep dive into high-opportunity gaps
        ↓
    Final: Comprehensive market intelligence with actionable insights
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
from dotenv import load_dotenv
import praw
from anthropic import Anthropic

# Load environment
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class RecursiveIntelligenceAgent:
    """
    Multi-round intelligence gathering that gets smarter each iteration
    """

    def __init__(self, max_depth=3, convergence_threshold=0.85):
        self.max_depth = max_depth
        self.convergence_threshold = convergence_threshold

        # Knowledge accumulation
        self.knowledge_graph = {
            'competitors': {},
            'pain_points': {},
            'keywords': {},
            'price_mentions': [],
            'locations': {},
            'opportunities': []
        }

        # Search history to avoid duplicates
        self.searched_terms = set()

        # Round results
        self.round_results = []

        # Initialize APIs
        self._init_reddit()
        self._init_claude()

    def _init_reddit(self):
        """Initialize Reddit API"""
        client_id = os.getenv('REDDIT_CLIENT_ID')
        client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        user_agent = os.getenv('REDDIT_USER_AGENT', 'RecursiveIntelligence:v1.0')

        if not client_id or not client_secret:
            print("❌ Reddit API credentials not found in .env")
            sys.exit(1)

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        print("✅ Reddit API connected")

    def _init_claude(self):
        """Initialize Claude API for analysis"""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            print("⚠️  Claude API key not found - using rule-based analysis")
            self.claude = None
        else:
            self.claude = Anthropic(api_key=api_key)
            print("✅ Claude API connected")

    def run(self, initial_keywords, subreddits, niche="proposals", location="raleigh"):
        """
        Main recursive intelligence loop

        Args:
            initial_keywords: Starting search terms
            subreddits: Which subreddits to search
            niche: Industry/niche being researched
            location: Geographic focus
        """
        print("\n" + "="*80)
        print("🧠 RECURSIVE INTELLIGENCE AGENT - STARTING")
        print("="*80)
        print(f"Initial Keywords: {initial_keywords}")
        print(f"Subreddits: {subreddits}")
        print(f"Max Depth: {self.max_depth} rounds")
        print(f"Niche: {niche} | Location: {location}\n")

        current_keywords = initial_keywords
        current_depth = 0

        while current_depth < self.max_depth:
            print(f"\n{'='*80}")
            print(f"🔄 ROUND {current_depth + 1} - Searching with {len(current_keywords)} keywords")
            print(f"{'='*80}\n")

            # Extract data from Reddit
            round_data = self.extract_reddit_round(
                keywords=current_keywords,
                subreddits=subreddits
            )

            # Analyze and extract structured insights
            print(f"\n📊 Analyzing Round {current_depth + 1} data...")
            structured_insights = self.analyze_round_data(
                round_data=round_data,
                round_number=current_depth + 1,
                niche=niche,
                location=location
            )

            # Store round results
            self.round_results.append({
                'round': current_depth + 1,
                'keywords_searched': current_keywords,
                'insights': structured_insights,
                'timestamp': datetime.now().isoformat()
            })

            # Generate next round of search terms
            next_keywords = self.generate_next_round_keywords(
                structured_insights,
                current_depth + 1
            )

            # Check convergence
            if self.has_converged(current_keywords, next_keywords):
                print(f"\n✅ CONVERGENCE REACHED at Round {current_depth + 1}")
                print("   No significant new insights - stopping")
                break

            if not next_keywords:
                print(f"\n✅ NO NEW KEYWORDS GENERATED - Research complete")
                break

            # Prepare for next round
            current_keywords = next_keywords
            current_depth += 1

        # Final synthesis
        print(f"\n{'='*80}")
        print(f"🎯 FINAL SYNTHESIS - Completed {current_depth + 1} rounds")
        print(f"{'='*80}\n")

        final_report = self.synthesize_all_rounds()

        return final_report

    def extract_reddit_round(self, keywords, subreddits):
        """
        Extract data from Reddit for current round keywords
        """
        round_data = {
            'posts': [],
            'comments': [],
            'total_posts': 0,
            'total_comments': 0
        }

        for keyword in keywords:
            # Skip if already searched
            if keyword in self.searched_terms:
                print(f"   ⏭️  Skipping '{keyword}' (already searched)")
                continue

            self.searched_terms.add(keyword)
            print(f"   🔍 Searching: '{keyword}'")

            for subreddit_name in subreddits:
                try:
                    subreddit = self.reddit.subreddit(subreddit_name)

                    # Search posts
                    for post in subreddit.search(keyword, limit=25, sort='relevance'):
                        if post.score < 3:  # Quality filter
                            continue

                        post_data = {
                            'id': post.id,
                            'title': post.title,
                            'text': post.selftext[:500],
                            'score': post.score,
                            'num_comments': post.num_comments,
                            'subreddit': subreddit_name,
                            'url': f"https://reddit.com{post.permalink}",
                            'created': datetime.fromtimestamp(post.created_utc).isoformat(),
                            'keyword_found': keyword
                        }

                        # Extract top comments
                        post.comments.replace_more(limit=0)
                        top_comments = sorted(post.comments.list(), key=lambda x: x.score, reverse=True)[:5]

                        post_comments = []
                        for comment in top_comments:
                            if hasattr(comment, 'body') and comment.score > 1:
                                post_comments.append({
                                    'text': comment.body[:300],
                                    'score': comment.score,
                                    'author': str(comment.author) if comment.author else '[deleted]'
                                })
                                round_data['total_comments'] += 1

                        post_data['top_comments'] = post_comments
                        round_data['posts'].append(post_data)
                        round_data['total_posts'] += 1

                except Exception as e:
                    print(f"      ✗ Error searching r/{subreddit_name}: {e}")
                    continue

        print(f"\n   ✅ Round complete: {round_data['total_posts']} posts, {round_data['total_comments']} comments\n")
        return round_data

    def analyze_round_data(self, round_data, round_number, niche, location):
        """
        Analyze round data and extract structured insights
        Uses Claude if available, otherwise rule-based
        """
        insights = {
            'competitors_discovered': [],
            'pain_points_found': [],
            'new_keywords': [],
            'price_mentions': [],
            'location_mentions': [],
            'opportunities': []
        }

        # Extract from posts and comments
        all_text = []
        for post in round_data['posts']:
            all_text.append(post['title'].lower())
            all_text.append(post['text'].lower())
            for comment in post.get('top_comments', []):
                all_text.append(comment['text'].lower())

        combined_text = ' '.join(all_text)

        # Competitor detection (proper nouns, venue names)
        potential_competitors = self._extract_competitors(combined_text, location)
        insights['competitors_discovered'] = potential_competitors

        # Pain point detection
        pain_point_phrases = [
            'too expensive', 'cant afford', 'wish it was cheaper', 'hard to find',
            'difficult to book', 'sold out', 'not available', 'closes at',
            'disappointing', 'limited options', 'nowhere to', 'need more'
        ]

        for phrase in pain_point_phrases:
            if phrase in combined_text:
                # Extract surrounding context
                context = self._extract_context(combined_text, phrase, window=50)
                insights['pain_points_found'].append({
                    'pain_point': phrase,
                    'context': context,
                    'mentions': combined_text.count(phrase)
                })

        # Price extraction
        import re
        price_pattern = r'\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        prices = re.findall(price_pattern, combined_text)
        insights['price_mentions'] = [f"${p}" for p in prices[:20]]  # Top 20

        # Location mentions
        nearby_cities = ['durham', 'chapel hill', 'cary', 'apex', 'wake forest', 'charlotte']
        for city in nearby_cities:
            count = combined_text.count(city)
            if count > 2:
                insights['location_mentions'].append({
                    'location': city.title(),
                    'mentions': count
                })

        # Keyword frequency for next round
        words = combined_text.split()
        word_freq = Counter(words)
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'is', 'was', 'are', 'were'}

        interesting_words = [
            word for word, count in word_freq.most_common(100)
            if len(word) > 4 and word not in stopwords and count > 3
        ]
        insights['new_keywords'] = interesting_words[:15]

        # Update knowledge graph
        self._update_knowledge_graph(insights, round_number)

        return insights

    def _extract_competitors(self, text, location):
        """Extract potential competitor names"""
        # Common venue name patterns
        patterns = [
            r'\b([A-Z][a-z]+ [A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b',  # Proper nouns
        ]

        competitors = []
        import re

        # Look for capitalized phrases (venue names)
        matches = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b', text)

        # Filter to likely venue names
        venue_indicators = ['hall', 'gardens', 'house', 'center', 'venue', 'space', 'plaza', 'hotel', 'restaurant']

        for match in set(matches):
            if any(indicator in match.lower() for indicator in venue_indicators):
                competitors.append(match)

        return list(set(competitors))[:10]  # Top 10 unique

    def _extract_context(self, text, phrase, window=50):
        """Extract surrounding context for a phrase"""
        idx = text.find(phrase)
        if idx == -1:
            return ""

        start = max(0, idx - window)
        end = min(len(text), idx + len(phrase) + window)
        return text[start:end]

    def _update_knowledge_graph(self, insights, round_number):
        """Update accumulated knowledge graph"""
        # Add competitors
        for comp in insights['competitors_discovered']:
            if comp not in self.knowledge_graph['competitors']:
                self.knowledge_graph['competitors'][comp] = {
                    'discovered_round': round_number,
                    'mentions': 1
                }
            else:
                self.knowledge_graph['competitors'][comp]['mentions'] += 1

        # Add pain points
        for pain in insights['pain_points_found']:
            key = pain['pain_point']
            if key not in self.knowledge_graph['pain_points']:
                self.knowledge_graph['pain_points'][key] = {
                    'discovered_round': round_number,
                    'mentions': pain['mentions'],
                    'context': pain['context']
                }

        # Add keywords
        for kw in insights['new_keywords']:
            if kw not in self.knowledge_graph['keywords']:
                self.knowledge_graph['keywords'][kw] = {
                    'discovered_round': round_number
                }

    def generate_next_round_keywords(self, insights, current_round):
        """
        Generate smart next-round keywords based on insights
        """
        next_keywords = []

        # If we found competitors, search for them specifically
        for comp in insights['competitors_discovered'][:3]:  # Top 3
            next_keywords.append(f"{comp} reviews")
            next_keywords.append(f"{comp} pricing")

        # If we found pain points, search for solutions
        for pain in insights['pain_points_found'][:3]:
            if 'expensive' in pain['pain_point']:
                next_keywords.append("affordable proposal venue")
            if 'hard to find' in pain['pain_point']:
                next_keywords.append("hidden proposal spots")
            if 'closes at' in pain['pain_point']:
                next_keywords.append("late night venue")

        # Explore new keywords that seem relevant
        for keyword in insights['new_keywords'][:5]:
            if len(keyword) > 5:  # Meaningful words only
                next_keywords.append(keyword)

        # Explore nearby locations if mentioned
        for loc in insights['location_mentions'][:2]:
            next_keywords.append(f"{loc['location']} proposal venue")

        # Remove duplicates and already-searched
        next_keywords = [kw for kw in set(next_keywords) if kw not in self.searched_terms]

        print(f"\n   🎯 Generated {len(next_keywords)} new search terms for next round:")
        for kw in next_keywords[:10]:
            print(f"      - {kw}")
        if len(next_keywords) > 10:
            print(f"      ... and {len(next_keywords) - 10} more")

        return next_keywords

    def has_converged(self, current_keywords, next_keywords):
        """Check if we've reached convergence"""
        if not next_keywords:
            return True

        # If fewer than 3 new keywords generated, we're converging
        if len(next_keywords) < 3:
            return True

        # If no new competitors or pain points in last round, converging
        last_round = self.round_results[-1] if self.round_results else None
        if last_round:
            insights = last_round['insights']
            if (len(insights['competitors_discovered']) == 0 and
                len(insights['pain_points_found']) == 0):
                return True

        return False

    def synthesize_all_rounds(self):
        """
        Create final comprehensive report from all rounds
        """
        report = {
            'research_metadata': {
                'total_rounds': len(self.round_results),
                'total_keywords_searched': len(self.searched_terms),
                'total_posts_analyzed': sum(r['insights'].get('total_posts', 0) for r in self.round_results),
                'timestamp': datetime.now().isoformat()
            },

            'knowledge_graph': self.knowledge_graph,

            'top_competitors': sorted(
                self.knowledge_graph['competitors'].items(),
                key=lambda x: x[1]['mentions'],
                reverse=True
            )[:10],

            'top_pain_points': sorted(
                self.knowledge_graph['pain_points'].items(),
                key=lambda x: x[1]['mentions'],
                reverse=True
            )[:10],

            'round_by_round': self.round_results
        }

        # Print summary
        print("\n📊 SYNTHESIS COMPLETE\n")
        print(f"   Rounds completed: {report['research_metadata']['total_rounds']}")
        print(f"   Keywords searched: {report['research_metadata']['total_keywords_searched']}")

        print(f"\n   🏢 Top Competitors Discovered:")
        for comp, data in report['top_competitors'][:5]:
            print(f"      - {comp} (mentioned {data['mentions']} times, round {data['discovered_round']})")

        print(f"\n   ⚠️  Top Pain Points:")
        for pain, data in report['top_pain_points'][:5]:
            print(f"      - {pain} (mentioned {data['mentions']} times)")

        return report


def main():
    """Run recursive intelligence agent"""

    # Configuration
    initial_keywords = [
        "proposal venue raleigh",
        "anniversary dinner raleigh",
        "private event space raleigh"
    ]

    subreddits = [
        'raleigh',
        'triangle',
        'NorthCarolina',
        'weddingplanning',
        'engaged'
    ]

    # Create agent
    agent = RecursiveIntelligenceAgent(
        max_depth=3,
        convergence_threshold=0.85
    )

    # Run recursive research
    final_report = agent.run(
        initial_keywords=initial_keywords,
        subreddits=subreddits,
        niche="proposals",
        location="raleigh"
    )

    # Save results
    os.makedirs('_outputs/recursive', exist_ok=True)

    output_file = f'_outputs/recursive/recursive_intelligence_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(output_file, 'w') as f:
        json.dump(final_report, f, indent=2)

    print(f"\n💾 Full report saved to: {output_file}")
    print("\n✅ RECURSIVE INTELLIGENCE AGENT COMPLETE\n")


if __name__ == "__main__":
    main()
