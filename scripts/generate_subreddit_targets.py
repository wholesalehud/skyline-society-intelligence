#!/usr/bin/env -S uv run
# /// script
# dependencies = [
#     "praw>=7.7.1",
# ]
# ///

"""
Subreddit Target Generator for Romance/Proposal Niche
Generates prioritized list of subreddits for Skyline Society intelligence gathering
Focus: Proposals, anniversaries, Valentine's Day, romantic events (Nov - Feb peak season)
"""

import praw
import json
from datetime import datetime

def generate_subreddit_targets():
    """
    Generate comprehensive list of subreddits for romance/proposal/event intelligence
    Organized by category and priority
    """

    subreddit_targets = {
        'generated_at': datetime.now().isoformat(),
        'focus_period': 'November 2025 - February 2026 (Valentine\'s Day Peak)',
        'total_subreddits': 0,
        'categories': {}
    }

    # CATEGORY 1: Proposals & Engagements (HIGHEST PRIORITY)
    subreddit_targets['categories']['proposals_engagements'] = {
        'priority': 'HIGH',
        'description': 'People actively planning proposals',
        'subreddits': [
            {
                'name': 'engaged',
                'subscribers_est': '500K+',
                'why_useful': 'Recently engaged couples share proposal stories - learn what worked',
                'keywords_to_track': ['proposal venue', 'how he proposed', 'proposal ideas', 'proposal planning']
            },
            {
                'name': 'weddingplanning',
                'subscribers_est': '300K+',
                'why_useful': 'Engaged couples planning weddings - often need rehearsal dinner venues, bridal events',
                'keywords_to_track': ['rehearsal dinner venue', 'bridal shower', 'engagement party']
            },
            {
                'name': 'wedding',
                'subscribers_est': '200K+',
                'why_useful': 'General wedding discussions',
                'keywords_to_track': ['intimate wedding', 'micro wedding', 'small venue']
            },
            {
                'name': 'JustEngaged',
                'subscribers_est': '50K+',
                'why_useful': 'Fresh engagement stories - what venues they used',
                'keywords_to_track': ['where he proposed', 'proposal location', 'rooftop proposal']
            },
            {
                'name': 'EngagementRings',
                'subscribers_est': '150K+',
                'why_useful': 'Ring shopping = proposal planning phase',
                'keywords_to_track': ['proposal ideas', 'how to propose', 'proposal venue']
            }
        ]
    }

    # CATEGORY 2: Local Raleigh/Triangle Area (HIGH PRIORITY)
    subreddit_targets['categories']['raleigh_local'] = {
        'priority': 'HIGH',
        'description': 'Local Raleigh community - direct target market',
        'subreddits': [
            {
                'name': 'raleigh',
                'subscribers_est': '200K+',
                'why_useful': 'Main Raleigh community - proposal planning, date ideas, event venues',
                'keywords_to_track': ['proposal', 'date night', 'anniversary', 'venue', 'restaurant', 'romantic', 'downtown']
            },
            {
                'name': 'triangle',
                'subscribers_est': '50K+',
                'why_useful': 'Broader Triangle area (Raleigh, Durham, Chapel Hill)',
                'keywords_to_track': ['raleigh venue', 'proposal spot', 'romantic restaurant']
            },
            {
                'name': 'NorthCarolina',
                'subscribers_est': '300K+',
                'why_useful': 'Statewide - people traveling to Raleigh for proposals',
                'keywords_to_track': ['raleigh', 'proposal destination', 'weekend trip']
            },
            {
                'name': 'raleighfood',  # If exists
                'subscribers_est': '20K+',
                'why_useful': 'Food scene discussions - private dining interest',
                'keywords_to_track': ['private dining', 'special occasion', 'anniversary dinner']
            }
        ]
    }

    # CATEGORY 3: Relationship Advice (MEDIUM-HIGH PRIORITY)
    subreddit_targets['categories']['relationship_planning'] = {
        'priority': 'MEDIUM-HIGH',
        'description': 'People planning to propose - looking for advice',
        'subreddits': [
            {
                'name': 'relationship_advice',
                'subscribers_est': '7M+',
                'why_useful': 'Massive community - proposal planning questions',
                'keywords_to_track': ['how to propose', 'proposal ideas', 'engagement planning']
            },
            {
                'name': 'relationships',
                'subscribers_est': '10M+',
                'why_useful': 'Huge community - anniversary/proposal discussions',
                'keywords_to_track': ['anniversary ideas', 'special occasion', 'proposal']
            },
            {
                'name': 'AskMen',
                'subscribers_est': '5M+',
                'why_useful': 'Men asking how to propose',
                'keywords_to_track': ['proposal ideas', 'how to propose', 'engagement ring', 'proposal venue']
            },
            {
                'name': 'AskWomen',
                'subscribers_est': '4M+',
                'why_useful': 'Women discussing dream proposals',
                'keywords_to_track': ['dream proposal', 'proposal ideas', 'romantic gestures']
            },
            {
                'name': 'dating_advice',
                'subscribers_est': '2M+',
                'why_useful': 'Serious daters planning next steps',
                'keywords_to_track': ['ready to propose', 'engagement', 'serious relationship']
            }
        ]
    }

    # CATEGORY 4: Valentine's Day Specific (SEASONAL - HIGH PRIORITY NOW)
    subreddit_targets['categories']['valentines_day'] = {
        'priority': 'HIGH (Nov-Feb)',
        'description': 'Valentine\'s Day planning - PEAK proposal season',
        'subreddits': [
            {
                'name': 'ValentinesDay',  # If exists
                'subscribers_est': 'Unknown',
                'why_useful': 'Valentine\'s planning - many propose on V-Day',
                'keywords_to_track': ['proposal', 'special plans', 'romantic ideas', 'valentines venue']
            },
            {
                'name': 'giftideas',
                'subscribers_est': '500K+',
                'why_useful': 'Gift planning = romantic occasion planning',
                'keywords_to_track': ['valentine gift', 'proposal', 'anniversary gift', 'romantic experience']
            },
            {
                'name': 'Gifts',
                'subscribers_est': '100K+',
                'why_useful': 'Experience gifts - venue bookings',
                'keywords_to_track': ['experience gift', 'romantic experience', 'proposal']
            }
        ]
    }

    # CATEGORY 5: Event Planning (MEDIUM PRIORITY)
    subreddit_targets['categories']['event_planning'] = {
        'priority': 'MEDIUM',
        'description': 'Professional and amateur event planners',
        'subreddits': [
            {
                'name': 'EventPlanning',
                'subscribers_est': '50K+',
                'why_useful': 'Event planners looking for unique venues',
                'keywords_to_track': ['intimate venue', 'private space', 'skyline view', 'downtown venue']
            },
            {
                'name': 'PartyPlanning',
                'subscribers_est': '20K+',
                'why_useful': 'Birthday, anniversary party planning',
                'keywords_to_track': ['anniversary party', 'milestone birthday', 'private venue']
            },
            {
                'name': 'DIYweddings',
                'subscribers_est': '80K+',
                'why_useful': 'Budget-conscious couples planning intimate events',
                'keywords_to_track': ['intimate venue', 'small wedding', 'micro wedding venue']
            }
        ]
    }

    # CATEGORY 6: Photography/Content Creation (MEDIUM PRIORITY)
    subreddit_targets['categories']['photography_content'] = {
        'priority': 'MEDIUM',
        'description': 'Photographers and content creators looking for locations',
        'subreddits': [
            {
                'name': 'WeddingPhotography',
                'subscribers_est': '100K+',
                'why_useful': 'Photographers recommend venues to clients',
                'keywords_to_track': ['best venues', 'skyline shots', 'indoor locations', 'proposal photography']
            },
            {
                'name': 'photography',
                'subscribers_est': '3M+',
                'why_useful': 'Photographers looking for shoot locations',
                'keywords_to_track': ['photoshoot location', 'skyline', 'urban photography', 'raleigh']
            },
            {
                'name': 'Instagram',
                'subscribers_est': '2M+',
                'why_useful': 'Instagrammable location discussions',
                'keywords_to_track': ['instagrammable', 'photo spot', 'aesthetic location', 'raleigh']
            },
            {
                'name': 'ContentCreators',  # If exists
                'subscribers_est': 'Unknown',
                'why_useful': 'Creators looking for studio space',
                'keywords_to_track': ['content studio', 'filming location', 'photoshoot space']
            }
        ]
    }

    # CATEGORY 7: Luxury & Lifestyle (MEDIUM PRIORITY)
    subreddit_targets['categories']['luxury_lifestyle'] = {
        'priority': 'MEDIUM',
        'description': 'Luxury consumers - our target demographic',
        'subreddits': [
            {
                'name': 'luxurylifestyle',
                'subscribers_est': '50K+',
                'why_useful': 'Luxury experience seekers',
                'keywords_to_track': ['luxury experience', 'private event', 'exclusive venue']
            },
            {
                'name': 'PrivateDining',  # If exists
                'subscribers_est': 'Unknown',
                'why_useful': 'Private dining enthusiasts',
                'keywords_to_track': ['private dining', 'intimate dinner', 'chef\'s table']
            },
            {
                'name': 'RoomPorn',
                'subscribers_est': '7M+',
                'why_useful': 'Beautiful space aesthetics - brand awareness',
                'keywords_to_track': ['skyline view', 'downtown living', 'luxury apartment']
            }
        ]
    }

    # CATEGORY 8: Surprise/Gift Planning (MEDIUM PRIORITY)
    subreddit_targets['categories']['surprise_gifts'] = {
        'priority': 'MEDIUM',
        'description': 'Planning surprises and special occasions',
        'subreddits': [
            {
                'name': 'SurpriseParty',  # If exists
                'subscribers_est': 'Unknown',
                'why_useful': 'Surprise event planning',
                'keywords_to_track': ['surprise venue', 'private space', 'secret location']
            },
            {
                'name': 'birthdays',
                'subscribers_est': '30K+',
                'why_useful': 'Milestone birthday planning',
                'keywords_to_track': ['special birthday', 'milestone', '30th birthday', 'private venue']
            },
            {
                'name': 'anniversary',  # If exists
                'subscribers_est': 'Unknown',
                'why_useful': 'Anniversary celebration planning',
                'keywords_to_track': ['anniversary ideas', 'anniversary venue', 'special dinner']
            }
        ]
    }

    # CATEGORY 9: Budget & Deals (LOW-MEDIUM PRIORITY)
    subreddit_targets['categories']['budget_conscious'] = {
        'priority': 'LOW-MEDIUM',
        'description': 'Budget planners - may need affordable packages',
        'subreddits': [
            {
                'name': 'Frugal',
                'subscribers_est': '3M+',
                'why_useful': 'Budget-conscious event planning',
                'keywords_to_track': ['affordable proposal', 'budget wedding', 'cheap venue']
            },
            {
                'name': 'Weddingsunder10k',
                'subscribers_est': '150K+',
                'why_useful': 'Budget wedding planning - intimate venue interest',
                'keywords_to_track': ['small venue', 'intimate wedding', 'affordable space']
            }
        ]
    }

    # Count total subreddits
    total = 0
    for category in subreddit_targets['categories'].values():
        total += len(category['subreddits'])
    subreddit_targets['total_subreddits'] = total

    return subreddit_targets


def verify_subreddits_exist(subreddit_list):
    """
    Verify which subreddits actually exist (requires PRAW setup)
    """
    # This would require Reddit API credentials
    # For now, return the list as-is
    pass


def generate_monitoring_schedule(subreddit_targets):
    """
    Generate a monitoring schedule for different subreddits
    """

    schedule = {
        'daily_monitoring': [],
        'weekly_monitoring': [],
        'monthly_monitoring': []
    }

    for category_name, category_data in subreddit_targets['categories'].items():
        priority = category_data['priority']

        for sub in category_data['subreddits']:
            if 'HIGH' in priority:
                schedule['daily_monitoring'].append(sub['name'])
            elif 'MEDIUM-HIGH' in priority:
                schedule['weekly_monitoring'].append(sub['name'])
            else:
                schedule['monthly_monitoring'].append(sub['name'])

    return schedule


def print_subreddit_report(subreddit_targets):
    """
    Print formatted report of subreddit targets
    """

    print("="*80)
    print("🎯 SKYLINE SOCIETY SUBREDDIT INTELLIGENCE TARGETS")
    print("="*80)
    print(f"\nGenerated: {subreddit_targets['generated_at']}")
    print(f"Focus Period: {subreddit_targets['focus_period']}")
    print(f"Total Subreddits: {subreddit_targets['total_subreddits']}")

    for category_name, category_data in subreddit_targets['categories'].items():
        print(f"\n\n📂 {category_name.upper().replace('_', ' ')}")
        print(f"   Priority: {category_data['priority']}")
        print(f"   {category_data['description']}")
        print(f"   Total: {len(category_data['subreddits'])} subreddits\n")

        for sub in category_data['subreddits']:
            print(f"   r/{sub['name']}")
            print(f"      Subscribers: ~{sub['subscribers_est']}")
            print(f"      Why: {sub['why_useful']}")
            print(f"      Track: {', '.join(sub['keywords_to_track'][:3])}")
            print()

    # Print monitoring schedule
    schedule = generate_monitoring_schedule(subreddit_targets)

    print("\n" + "="*80)
    print("📅 RECOMMENDED MONITORING SCHEDULE")
    print("="*80)

    print(f"\n🔴 DAILY (Check every day - Nov-Feb peak season):")
    for sub in schedule['daily_monitoring'][:10]:  # Top 10
        print(f"   - r/{sub}")

    print(f"\n🟡 WEEKLY (Check once a week):")
    for sub in schedule['weekly_monitoring'][:10]:
        print(f"   - r/{sub}")

    print(f"\n🟢 MONTHLY (Check once a month for trends):")
    for sub in schedule['monthly_monitoring'][:5]:
        print(f"   - r/{sub}")


def main():
    """
    Generate and save subreddit targets
    """

    print("🚀 Generating Subreddit Intelligence Targets for Skyline Society...\n")

    # Generate targets
    targets = generate_subreddit_targets()

    # Print report
    print_subreddit_report(targets)

    # Save to JSON
    import os
    os.makedirs('_outputs', exist_ok=True)

    with open('_outputs/subreddit_targets.json', 'w') as f:
        json.dump(targets, f, indent=2)

    print(f"\n\n💾 Saved to: _outputs/subreddit_targets.json")

    # Generate copy-paste list for Reddit monitoring scripts
    print("\n" + "="*80)
    print("📋 COPY-PASTE LIST FOR SCRIPTS")
    print("="*80)

    all_subreddits = []
    for category in targets['categories'].values():
        for sub in category['subreddits']:
            all_subreddits.append(sub['name'])

    print("\nPython list format:")
    print("subreddits = [")
    for sub in all_subreddits:
        print(f"    '{sub}',")
    print("]")

    print("\n✅ Done! Use this list in extract_reddit_insights.py")


if __name__ == "__main__":
    main()
