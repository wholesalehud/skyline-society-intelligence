---
description: Recursive intelligence agent - discovers insights across multiple rounds
---

# Deep Recursive Research (Self-Improving Intelligence)

You are launching a recursive intelligence agent that gets smarter with each iteration.

## How It Works

**Traditional Research**: Search once → Get results → Done

**Recursive Research**:
```
Round 1: Search "proposal venue raleigh"
    ↓
Discover: "Legends", "Duke Gardens", "expensive", "closes at 11pm"
    ↓
Round 2: Auto-search "Legends reviews", "late night venues raleigh", "affordable proposal"
    ↓
Discover: Pricing ($300/hr), specific issues, market gaps
    ↓
Round 3: Deep dive into opportunities
    ↓
Final: Comprehensive intelligence with actionable insights
```

---

## Expected Input Format

Provide research parameters:

```yaml
keywords: ["proposal venue", "anniversary dinner"]  # Starting search terms
location: raleigh                                    # Geographic focus
niche: proposals                                     # Industry
subreddits: ["raleigh", "weddingplanning"]          # Where to search
max_depth: 3                                         # How many rounds (1-5)
```

$ARGUMENTS

**If no arguments**: Uses Skyline Society defaults

---

## What the Agent Does

### **Round 1: Initial Extraction**
- Searches Reddit with your initial keywords
- Extracts posts, comments, sentiment
- Identifies: Competitors, pain points, new keywords

### **Round 2: Smart Follow-Up**
- AUTO-GENERATES new search terms based on Round 1
- Example discoveries:
  - Found "Legends" mentioned → Search "Legends Raleigh reviews"
  - Found "too expensive" → Search "affordable proposal venue"
  - Found "closes at 11pm" → Search "late night venues raleigh"

### **Round 3+: Deep Dive**
- Continues until convergence (no new insights) or max depth
- Builds comprehensive knowledge graph
- Cross-validates findings

---

## Example Output

After 3 rounds, you'll get:

```json
{
  "research_metadata": {
    "total_rounds": 3,
    "keywords_searched": 28,
    "posts_analyzed": 247,
    "comments_analyzed": 1,543
  },

  "top_competitors_discovered": [
    {
      "name": "Legends",
      "mentions": 15,
      "sentiment": "mixed",
      "price_range": "$300-400/hr",
      "issues": ["expensive", "hard to book"],
      "discovered_in_round": 1
    },
    {
      "name": "Duke Gardens",
      "mentions": 12,
      "sentiment": "positive",
      "issues": ["outdoor only", "weather dependent"],
      "discovered_in_round": 1
    }
  ],

  "top_pain_points": [
    {
      "pain_point": "venues close at 11pm",
      "mentions": 12,
      "severity": "high",
      "market_gap": true,
      "opportunity": "Late-night venue service"
    },
    {
      "pain_point": "too expensive",
      "mentions": 28,
      "price_sensitivity": "$200-300 sweet spot",
      "opportunity": "Mid-range offering"
    }
  ],

  "opportunities_identified": [
    {
      "opportunity": "Late-night venue gap",
      "evidence": "12 mentions across 3 rounds, no competitors offer",
      "target_price": "$250/hr after 10pm",
      "estimated_demand": "High",
      "next_steps": ["Test with extended hours package", "Survey demand"]
    }
  ]
}
```

---

## Run the Agent

### **Option 1: Via Slash Command** (You're doing this)

```bash
/deep-research
keywords: ["proposal venue", "private dining"]
location: raleigh
niche: proposals
subreddits: ["raleigh", "weddingplanning", "engaged"]
max_depth: 3
```

### **Option 2: Direct Script** (After restart)

```bash
cd /home/primemeridianlabs/Development/Erika_TikTok
chmod +x scripts/recursive_intelligence_agent.py
./scripts/recursive_intelligence_agent.py
```

---

## Advanced Usage

### **Research Different Market**

```bash
/deep-research
keywords: ["baby shower venue", "gender reveal"]
location: charlotte
niche: baby-showers
subreddits: ["charlotte", "Mommit", "BabyBumps"]
max_depth: 4
```

### **Competitor Deep Dive**

```bash
/deep-research
keywords: ["Legends Raleigh", "Transfer Co Food Hall"]
location: raleigh
niche: venues
subreddits: ["raleigh", "triangle"]
max_depth: 2
```

### **Pain Point Research**

```bash
/deep-research
keywords: ["affordable proposal venue", "budget wedding venue"]
location: raleigh
niche: budget-events
subreddits: ["Frugal", "Weddingsunder10k", "raleigh"]
max_depth: 3
```

---

## What Makes This Powerful

1. **Self-Improving**: Each round generates smarter searches
2. **Cross-Validation**: Validates insights across multiple rounds
3. **Knowledge Graph**: Builds comprehensive competitive map
4. **Convergence Detection**: Stops when no new insights (efficient)
5. **Multi-Source**: Can extend to YouTube, Web, TikTok (future)

---

## Output Location

Results saved to: `_outputs/recursive/recursive_intelligence_YYYYMMDD_HHMMSS.json`

---

## Integration with Other Commands

**After deep research, feed insights into**:
- `/mine-monetization-ideas` - Turn pain points into revenue
- `/discover-partners` - Found competitors? Partner with them
- `/forecast-revenue` - Model opportunities discovered

---

## Tips

- **Start broad** (Round 1): "proposal venue"
- **Agent narrows** (Round 2): "Legends Raleigh pricing"
- **Agent deepens** (Round 3): "affordable alternatives to Legends"

Let the agent guide itself based on what it discovers!

---

**This is the future of research - intelligence that compounds with each iteration** 🚀
