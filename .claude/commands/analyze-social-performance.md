---
description: Analyze any social media account's performance dynamically
---

# Social Media Performance Analyzer (Dynamic)

You are a social media growth strategist.

## Expected Input Format

Provide account details to analyze:

```yaml
platform: tiktok                    # tiktok, instagram, youtube
account: @skylinesociety27          # Handle/username
niche: event-venue                  # Content niche
goal: growth                        # growth, engagement, conversions, monetization
timeframe: last-28-days             # Analysis period
```

$ARGUMENTS

---

## Your Mission

Analyze the specified social media account and generate actionable growth tactics.

**If no arguments provided**: Use Skyline Society TikTok defaults

## Analysis Framework

### 1. **Current Performance Baseline**

Request from user (or guide them to get):
- {platform} analytics access
- Top 10 performing posts (last {timeframe})
- Current follower count, engagement rate
- Any recent viral posts or momentum

**If analytics not available**: Guide them to:
1. Switch to Business/Creator account on {platform}
2. Download analytics data
3. Share screenshots or CSV export

### 2. **Content Performance Analysis**

For each top-performing post, extract:

**Engagement Metrics**:
- Views, watch time %
- Likes, comments, shares, saves
- Comment sentiment (positive/negative/questions)

**Content Patterns**:
- Video/post length (what's the sweet spot?)
- Hook effectiveness (first 3 seconds analysis)
- Music/sound used (trending or original?)
- Hashtags used (which drove traffic?)
- Post timing (when published?)
- Content type (educational, entertainment, behind-scenes, transformation)

**Winner Analysis**:
Identify TOP 3 performing posts:
1. **[Post Title/Description]**
   - Views: [X], Engagement: [%]
   - Why it succeeded: [specific elements - hook, trend, emotion, timing]
   - Replicate-able pattern?: [Yes/No + how]
   - Content format: [Tutorial / Story / Transformation / POV / etc.]

### 3. **Competitor Benchmarking**

Search {platform} for competitors in {niche}:
- What content formats get highest engagement?
- What sounds/music are they using?
- Posting frequency?
- What's their unique angle?
- Gaps we can exploit?

**Find 5-10 competitors**:
| Account | Followers | Avg Views | Top Content Type | Unique Angle |
|---------|-----------|-----------|------------------|--------------|
| ...     | ...       | ...       | ...              | ...          |

### 4. **Trending Content Research**

Current {platform} trends in {niche}:
- Viral formats (POV, Day in the life, Before/After)
- Trending sounds/songs (specific to niche)
- Popular hashtags (niche + location)
- Emerging content styles

**Trend Opportunities**:
1. [Trend name] - Why it fits {niche}: [reason] - How to adapt: [specific angle]
2. ...

### 5. **Hashtag Strategy**

Research and recommend mix for {platform} + {niche}:
- **Niche hashtags** (10K-100K): #specific #targeted
- **Mid-tier** (100K-1M): #growing #moderate
- **Broad** (1M+): #popular #reach
- **Trending**: Current viral tags that fit

**Recommended Sets** (copy-paste ready):
```
Set 1 - [Use case]:
#hashtag1 #hashtag2 #hashtag3 ...

Set 2 - [Use case]:
#hashtag4 #hashtag5 ...
```

---

## Output Format

### Performance Summary
**Account**: @{account} ({platform})
**Niche**: {niche}
**Current Stats**:
- Followers: [X]
- Avg engagement rate: [%]
- Best performing content type: [format]
- Growth rate: [+X followers/week]

**Since Last Viral Post** (if any):
- New followers: [+X]
- Conversion source: [specific post/topic]
- Momentum: [Accelerating/Stable/Declining]

### Top 3 Winning Content Analysis

**Post 1: [Title]**
- **Metrics**: [Views], [Engagement %], [Saves]
- **Why it worked**:
  1. Hook: "[First 3 seconds analysis]"
  2. Format: [What made it engaging]
  3. Emotion: [What feeling it evoked]
  4. Timing: [Why it was timely]
- **Replicate by**:
  1. [Actionable step]
  2. [Actionable step]
  3. [Actionable step]

[Repeat for posts 2-3]

### Growth Tactics (Ranked by Impact)

**IMMEDIATE (This Week)** - Quick wins:
1. **[Tactic Name]**
   - Estimated impact: [High/Med/Low] - [+X followers or +X% engagement]
   - Time required: [X hours]
   - How to execute: [Step-by-step]
   - Success metric: [What to measure]

2. [Continue for 3-5 tactics]

**SHORT-TERM (This Month)** - Strategic moves:
1. [Tactic]
2. ...

### Posting Schedule Recommendation

Based on analytics + competitor research:

| Day | Time | Content Type | Hook Style | Hashtags | Goal |
|-----|------|-------------|-----------|----------|------|
| Mon | 7pm | Behind-scenes | "You won't believe..." | Set 1 | Awareness |
| Wed | 12pm | Transformation | "POV: ..." | Set 2 | Engagement |
| Fri | 6pm | Educational | "Here's how..." | Set 3 | Saves |
| Sun | 4pm | Aesthetic | "[Emotion]..." | Set 1 | Growth |

**Optimal posting times** (based on when YOUR audience is active):
- Best: [Time windows]
- Good: [Time windows]
- Avoid: [Time windows with low engagement]

### Hook Library (First 3 Seconds)

Test these hooks (rotate to avoid fatigue):

**Problem-aware hooks**:
1. "POV: You're searching for {niche-service} in {location} and..."
2. "This is what ${X} gets you in {location}..."
3. "Stop doing {common mistake} when {niche-activity}..."

**Curiosity hooks**:
1. "You won't believe what happened when..."
2. "The secret to {desired outcome} in {location}..."
3. "I did {X} so you don't have to..."

**Value hooks**:
1. "How to {achieve goal} without {pain point}..."
2. "{Number} things nobody tells you about {niche}..."
3. "Here's exactly how we {achievement}..."

### Content Calendar (Next 7-14 Days)

**Day 1**: [Specific content idea] - Format: [type] - Goal: [metric target]
**Day 2**: [Idea] - Format: [type] - Goal: [metric]
...[Continue for 7-14 days]

Each with:
- Hook (first 3 seconds)
- Content outline
- Hashtags to use
- Sound/music suggestion
- CTA (call-to-action)

### Monetization Opportunities

Based on follower count and engagement:

**Current opportunities** (at [{follower-count}] followers):
1. **Affiliate marketing** - Revenue: $[X]/month - Products: [specific]
2. **Brand partnerships** - When: [follower milestone] - Brands: [types]
3. **Digital products** - Ideas: [specific to niche] - Price: $[X]

**Next milestone** (at [{next-milestone}] followers):
- Unlock: [platform feature or opportunity]
- Estimated revenue: $[X]/month
- Timeline: [X weeks/months at current growth]

### Next Steps Checklist

- [ ] Implement top 3 tactics this week
- [ ] Post [X] times using new schedule
- [ ] Test [X] new hooks from library
- [ ] Reply to ALL comments within 2 hours (algorithm boost)
- [ ] Film [X] pieces of content in batch
- [ ] Run `/analyze-social-performance` again in 7 days

---

**Output this analysis to**: `_outputs/social/{platform}_{account}_analysis_{date}.md`

**Run frequency**: Daily during growth sprints, weekly for maintenance

**Integration**: Feed findings into `/mine-monetization-ideas` for new revenue streams

---

## Examples of Usage

**Default (Skyline Society TikTok)**:
```bash
/analyze-social-performance
# Uses: TikTok, @skylinesociety27, event-venue niche
```

**Custom account**:
```bash
/analyze-social-performance
platform: instagram
account: @your_handle
niche: wedding-photography
goal: conversions
timeframe: last-90-days
```

**YouTube analysis**:
```bash
/analyze-social-performance
platform: youtube
account: YourChannelName
niche: event-planning-tips
goal: monetization
```

**Reusable for ANY social account in ANY niche**!
