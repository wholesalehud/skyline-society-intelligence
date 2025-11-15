---
description: Research any market/niche with dynamic parameters
---

# Market Intelligence Research (Dynamic)

You are a market research specialist.

## Expected Input Format

Provide your research parameters (or use defaults for Skyline Society):

```yaml
location: raleigh          # City/region to research
niche: proposals           # Industry/niche (proposals, weddings, events, baby showers, etc.)
timeframe: nov-feb         # When (q1, nov-feb, year-round, etc.)
competitors: peerspace     # Competitor platforms to analyze (optional)
budget_range: 200-500      # Target price range per hour/event (optional)
```

$ARGUMENTS

---

## Your Mission

Conduct comprehensive market research for the specified niche in the given location.

**If no arguments provided**: Use defaults (Raleigh, proposals, Nov-Feb, luxury tier $200-500/hr)

## Research Areas

### 1. **Competitive Landscape Analysis**

Search for and analyze competitors in {location} for {niche}:
- Venue/service listings (Peerspace, Airbnb Experiences, local directories)
- Similar businesses offering {niche} services
- Pricing per hour/event
- Average review ratings
- Unique selling points
- Availability patterns

**Extract for each competitor**:
| Competitor | Price/Hour | Features | Reviews | Bookings/Month (est) |
|-----------|-----------|---------|---------|---------------------|

### 2. **Search Demand Analysis**

Research Google Trends and search patterns for:
- "{location} {niche}"
- Related queries in the area
- Seasonal patterns (when do searches spike for {timeframe}?)
- Geographic breakdown (nearby cities)

### 3. **Community Intelligence (Reddit/Forums)**

Search Reddit discussions:
- r/{location} (local community)
- Niche-specific subreddits related to {niche}
- Common complaints about existing options
- Price sensitivity discussions
- Underserved needs

**What to extract**:
- Wants: "Looking for...", "Need...", "Recommend..."
- Problems: "Too expensive", "Hard to find", "Disappointed with..."
- Price mentions: Actual dollar amounts discussed
- Competitor mentions: What venues/services are people using?

### 4. **Pricing Intelligence**

Current market rates in {location} for {niche}:
- Budget tier: $X-X
- Mid-range: $X-X
- Luxury tier: $X-X
- What's included at each tier?

### 5. **Trend Identification**

Search for emerging trends:
- TikTok viral trends related to {niche}
- Instagram aesthetics (#hashtags)
- Event industry publications
- Seasonal demand shifts

---

## Output Format

### Executive Summary
**Market**: {location} - {niche} ({timeframe})
**Top 3 Opportunities**:
1. [Opportunity] - Demand: [High/Med/Low], Competition: [Low/Med/High]
2. ...
3. ...

### Competitive Analysis
| Venue/Service | Price/Hour | Unique Features | Review Score | Est. Bookings |
|--------------|-----------|-----------------|--------------|---------------|
| ...          | ...       | ...             | ...          | ...           |

**Market Gap Analysis**:
- Underserved price point: $[range]
- Missing features: [list]
- Booking friction: [problems identified]

### Underserved Niches
1. **[Niche Name]**
   - Market demand: [High/Medium/Low] - Evidence: [Reddit threads, Google Trends]
   - Competition level: [Low/Medium/High]
   - Potential pricing: $[range]
   - Recommended offering: [specific proposal]
   - First steps to test: [validation actions]

2. [Repeat for 3-5 niches]

### Seasonal Insights
- **Peak Season**: [Months] - Why: [Valentine's, wedding season, etc.]
- **Shoulder Season**: [Months] - Opportunities: [off-peak packages]
- **Off-Season**: [Months] - Strategies: [how to drive bookings]

### Pricing Recommendations
**For {location} {niche} market:**
- **Premium Tier**: $[X]/hour - For: [target customer]
- **Standard Tier**: $[X]/hour - For: [target customer]
- **Off-Peak Special**: $[X]/hour - When: [days/times]

**Rationale**: [Based on competitive analysis + demand research]

### Content Strategy Insights

**Top 5 Blog Post Topics** (SEO-driven):
1. **[Topic]** - Keyword: "[search term]" - Volume: [estimate] - Intent: [informational/transactional]
   - Why it works: [Reddit discussions show people asking this]
   - Headline: "[SEO-optimized title]"

2. [Continue for 5 topics]

**Top 5 TikTok Content Ideas** (Trend-driven):
1. **[Idea]** - Hook: "[First 3 seconds]" - Why it will perform: [trending sound/format]
   - Hashtags: #hashtag1 #hashtag2 #location
   - CTA: [Save for later / Book now / DM for pricing]

2. [Continue for 5 ideas]

### Action Items

**Immediate (This Week)**:
- [ ] [Specific action from findings] - Impact: [metric]
- [ ] ...

**Short-term (This Month)**:
- [ ] ...

**Long-term (This Quarter)**:
- [ ] ...

---

## Research Sources to Use

- **Web search**: "{location} {niche}", "best {niche} in {location}"
- **Google Trends**: Track search volume for key terms
- **Reddit**: r/{location}, niche-specific subreddits
- **Instagram**: #{location}{niche}, location hashtags
- **TikTok**: Search {niche} + location tags
- **Competitor sites**: Peerspace, Airbnb Experiences, local directories
- **Industry sites**: The Knot, WeddingWire (if wedding-related), Yelp

---

**Output this research to**: `_outputs/market/market_research_{location}_{niche}_{date}.md`

**Run frequency**: Weekly during high season, monthly otherwise

**Next step**: Feed insights into `/mine-monetization-ideas` and `/generate-innovation-concepts`

---

## Examples of Usage

**Default (Skyline Society)**:
```bash
/research-market
# Uses: raleigh, proposals, nov-feb, $200-500/hr
```

**Custom niche**:
```bash
/research-market
location: charlotte
niche: baby showers
timeframe: q2-q3
budget_range: 150-300
```

**Different city, same niche**:
```bash
/research-market
location: durham
niche: proposals
timeframe: year-round
competitors: peerspace, airbnb
```

This makes the command **reusable for ANY location and niche**!
