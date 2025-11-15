# BSHR Framework Integration

## ✅ What is BSHR?

**BSHR = Brainstorm, Search, Hypothesize, Refine**

A framework from library and information science that models **"information foraging"** in humans.

From the original BSHR_Loop project:
> "BSHR loop uses Large Language Models (LLMs) to automate human search behavior for addressing any information need in an arbitrarily large information domain."

---

## 🔄 The BSHR Loop Process

### **1. Brainstorm**
Accept user queries or information problems of arbitrary complexity. The LLM brainstorms a list of search queries, ensuring:
- Well-rounded search using information literacy
- Counterfactual queries (challenge assumptions)
- Informed by notes and accumulated information over time

### **2. Search**
Brainstormed queries search an information source (API, database, knowledge graph):
- Results cached locally (know what we've already seen)
- Crucial for knowing when available information is exhausted
- Each iteration improves with more cached data

### **3. Hypothesize**
LLM reads searched materials and formulates hypothesis:
- "Takes notes" (LLMs excel at this)
- Records hypothesis with citations
- Each version stored for comparison
- Renders when "good enough" and exits

### **4. Refine**
Recursion - next loop performs "informed search" vs "naive search":
- After first pass, use discoveries to write better queries
- Refine hypotheses based on new evidence
- All aspects of the loop can be refined

### **5. Satisficing Check**
At end of each loop, LLM decides if information need is **satisficed**:
- Amount and quality of evidence supporting hypothesis
- Whether new information is available
- If information domain has been exhausted

---

## 🎯 Key Concepts from Information Science

### **Information Foraging**
Just as animals forage for food, humans forage for information. BSHR models this behavior.

### **Information Literacy**
Ability to identify, locate, evaluate, and effectively use information. The LLM employs this to brainstorm comprehensive queries.

### **Satisficing** (Herbert Simon)
Decision-making strategy that aims for satisfactory result, rather than optimal. The point at which enough information has been gathered.

### **Naive Query vs Informed Query**
- **Naive Query**: Initial queries in new domain (educated guesses)
- **Informed Query**: Focused queries after gathering information (follows "information scent")

### **Precision vs Recall**
- **Precision**: Proportion of retrieved info that is relevant (quality)
- **Recall**: Proportion of all relevant info retrieved (quantity)
- Goal: Balance both (high recall + high precision)

---

## 🔥 How We've Already Implemented BSHR

### **Our Recursive Intelligence Agent = BSHR Loop!**

**File**: `scripts/recursive_intelligence_agent.py`

#### **Brainstorm Phase**
```python
def generate_next_round_keywords(self, insights, current_round):
    """Generate smart next-round keywords based on insights"""
    next_keywords = []

    # If we found competitors, search for them specifically
    for comp in insights['competitors_discovered'][:3]:
        next_keywords.append(f"{comp} reviews")
        next_keywords.append(f"{comp} pricing")

    # If we found pain points, search for solutions
    for pain in insights['pain_points_found'][:3]:
        if 'expensive' in pain['pain_point']:
            next_keywords.append("affordable proposal venue")
        if 'hard to find' in pain['pain_point']:
            next_keywords.append("hidden proposal spots")
```

**This is BRAINSTORMING**: Generating informed queries based on accumulated knowledge

---

#### **Search Phase**
```python
def extract_reddit_round(self, keywords, subreddits):
    """Extract data from Reddit for current round keywords"""
    for keyword in keywords:
        # Skip if already searched (CACHED)
        if keyword in self.searched_terms:
            print(f"   ⏭️  Skipping '{keyword}' (already searched)")
            continue

        self.searched_terms.add(keyword)

        for subreddit_name in subreddits:
            subreddit = self.reddit.subreddit(subreddit_name)
            for post in subreddit.search(keyword, limit=25, sort='relevance'):
                # Extract posts and comments
```

**This is SEARCHING**: Using brainstormed queries to search Reddit API, caching results

---

#### **Hypothesize Phase**
```python
def analyze_round_data(self, round_data, round_number, niche, location):
    """Analyze round data and extract structured insights"""
    insights = {
        'competitors_discovered': [],
        'pain_points_found': [],
        'new_keywords': [],
        'price_mentions': [],
        'location_mentions': [],
        'opportunities': []
    }

    # Competitor detection (proper nouns, venue names)
    potential_competitors = self._extract_competitors(combined_text, location)
    insights['competitors_discovered'] = potential_competitors

    # Pain point detection
    for phrase in pain_point_phrases:
        if phrase in combined_text:
            context = self._extract_context(combined_text, phrase, window=50)
            insights['pain_points_found'].append({
                'pain_point': phrase,
                'context': context,
                'mentions': combined_text.count(phrase)
            })
```

**This is HYPOTHESIZING**: Formulating structured insights (hypotheses) about competitors, pain points, opportunities

---

#### **Refine Phase**
```python
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
```

**This is REFINING**: Accumulating knowledge across rounds, building comprehensive graph

---

#### **Satisficing Phase**
```python
def has_converged(self, current_keywords, next_keywords):
    """Check if we've reached convergence (SATISFICING)"""
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
```

**This is SATISFICING**: Deciding when we've gathered enough information

---

## 🚀 BSHR Implementation Status

### ✅ **Already Implemented**

| BSHR Phase | Our Implementation | File |
|------------|-------------------|------|
| **Brainstorm** | `generate_next_round_keywords()` | `recursive_intelligence_agent.py:383` |
| **Search** | `extract_reddit_round()` with caching | `recursive_intelligence_agent.py:179` |
| **Hypothesize** | `analyze_round_data()` - structured insights | `recursive_intelligence_agent.py:245` |
| **Refine** | `_update_knowledge_graph()` - accumulate knowledge | `recursive_intelligence_agent.py:354` |
| **Satisficing** | `has_converged()` - convergence detection | `recursive_intelligence_agent.py:423` |

### 🔄 **Main Loop** (BSHR in Action)

```python
def run(self, initial_keywords, subreddits, niche="proposals", location="raleigh"):
    """Main recursive intelligence loop (BSHR LOOP)"""
    current_keywords = initial_keywords
    current_depth = 0

    while current_depth < self.max_depth:
        # SEARCH: Extract data from Reddit
        round_data = self.extract_reddit_round(
            keywords=current_keywords,
            subreddits=subreddits
        )

        # HYPOTHESIZE: Analyze and extract structured insights
        structured_insights = self.analyze_round_data(
            round_data=round_data,
            round_number=current_depth + 1,
            niche=niche,
            location=location
        )

        # REFINE: Store and accumulate knowledge
        self.round_results.append({...})

        # BRAINSTORM: Generate next round of search terms
        next_keywords = self.generate_next_round_keywords(
            structured_insights,
            current_depth + 1
        )

        # SATISFICING: Check convergence
        if self.has_converged(current_keywords, next_keywords):
            print(f"\n✅ CONVERGENCE REACHED at Round {current_depth + 1}")
            break
```

**This is the complete BSHR Loop!**

---

## 📊 Enhanced BSHR Features

### **1. Multi-Source BSHR** (Next Evolution)

Pattern from `trading_intel_v2/bshr_multi_source.py`:

```python
sources = {
    'reddit': extract_reddit_round(),
    'youtube': extract_youtube_insights(),
    'tiktok': extract_tiktok_comments(),
    'web': firecrawl_search()
}

# Cross-validate insights across sources
consensus = build_consensus(sources)

# Confidence scoring: Base 30% + 10% per source (capped at 90%)
for insight in insights:
    source_count = count_sources_mentioning(insight, sources)
    confidence = min(30 + (source_count * 10), 90)
```

**Why this is powerful**: Insights validated across Reddit + YouTube + TikTok = higher confidence

---

### **2. BSHR with Video Processing**

Pattern from `trading_intel_v2/bshr_video_processor.py`:

```python
# Extract video intelligence
video_data = {
    'transcript': extract_with_yt_dlp(),
    'comments': get_top_comments(limit=20, sort='engagement'),
    'metadata': {
        'views': video.view_count,
        'likes': video.like_count,
        'engagement_rate': calculate_engagement()
    }
}

# Apply Fabric patterns for wisdom extraction
wisdom = fabric_extract_wisdom(video_data['transcript'])
sentiment = analyze_comment_sentiment(video_data['comments'])
```

**Why this is powerful**: Video content + audience reactions = market validation

---

### **3. Satisficing Criteria** (From BSHR Framework)

Pattern from `trading_intel_v2/bshr_framework_demo.py`:

```python
def check_satisficing(state):
    """
    Satisficing criteria (3 of 4 = done):
    1. High confidence (>70%)
    2. Multi-source validation (3+ sources)
    3. Low new information rate (<10% new per round)
    4. Time/cost constraints met
    """
    criteria_met = 0

    if state['confidence'] > 0.7:
        criteria_met += 1

    if len(state['sources_validated']) >= 3:
        criteria_met += 1

    if state['new_information_rate'] < 0.1:
        criteria_met += 1

    if state['rounds_completed'] < state['max_rounds']:
        criteria_met += 1

    return criteria_met >= 3
```

**Why this is powerful**: Know exactly when to stop (don't over-research, don't under-research)

---

## 🎯 BSHR Integration Roadmap

### **Phase 1: Current State** ✅
- [x] Recursive intelligence with BSHR loop (Reddit only)
- [x] Brainstorm → Search → Hypothesize → Refine cycle
- [x] Convergence detection (satisficing)
- [x] Knowledge graph accumulation

### **Phase 2: Multi-Source BSHR** 🚧
- [ ] Integrate YouTube extraction (yt-dlp)
- [ ] Integrate TikTok extraction (yt-dlp)
- [ ] Cross-platform validation
- [ ] Confidence scoring (30% + 10% per source)

### **Phase 3: Enhanced Hypothesizing** 🔮
- [ ] Use Claude API for hypothesis generation
- [ ] Citation tracking
- [ ] Hypothesis versioning and comparison
- [ ] Contradiction detection

### **Phase 4: Advanced Satisficing** 🎓
- [ ] Implement 4-criteria satisficing (3 of 4 = done)
- [ ] Track new information rate
- [ ] Measure confidence scores
- [ ] Time/cost constraint management

---

## 💡 Use Cases for BSHR in Skyline Society

### **Use Case 1: Competitor Deep Dive**
```bash
/deep-research
keywords: ["Legends Raleigh", "Transfer Co Food Hall"]
location: raleigh
niche: venues
max_depth: 3
```

**BSHR Flow**:
1. **Brainstorm**: "Legends Raleigh reviews", "Transfer Co pricing", "competitor alternatives"
2. **Search**: Reddit r/raleigh, r/weddingplanning
3. **Hypothesize**: "Legends = $300/hr, Transfer Co = $400/hr, gap in $150-250 range"
4. **Refine**: Search "affordable venue raleigh", "budget proposal venue"
5. **Satisficing**: Found 15 competitor mentions, 12 price points, 3 market gaps → DONE

---

### **Use Case 2: Pain Point Discovery**
```bash
/deep-research
keywords: ["proposal venue too expensive", "can't find affordable venue"]
location: raleigh
niche: budget-proposals
max_depth: 2
```

**BSHR Flow**:
1. **Brainstorm**: "proposal on a budget", "affordable anniversary dinner", "cheap romantic venue"
2. **Search**: r/Frugal, r/Weddingsunder10k, r/raleigh
3. **Hypothesize**: "Users willing to pay $150-250, but only finding $300+ options"
4. **Refine**: Search "DIY proposal setup", "public proposal spots"
5. **Satisficing**: Validated pain point across 3 subreddits, 28 mentions → DONE

---

### **Use Case 3: Content Topic Validation**
```bash
/deep-research
keywords: ["how to plan a proposal", "proposal planning checklist"]
location: raleigh
niche: proposal-education
max_depth: 3
```

**BSHR Flow**:
1. **Brainstorm**: "proposal timeline", "proposal budget calculator", "surprise proposal tips"
2. **Search**: r/engaged, r/weddingplanning, YouTube search
3. **Hypothesize**: "High demand for: proposal timeline (32 mentions), budget planning (28 mentions), venue selection (45 mentions)"
4. **Refine**: Search specific questions: "when to book proposal photographer", "how much to spend on proposal venue"
5. **Satisficing**: Found 3 high-demand topics with multi-source validation → Create content calendar

---

## 🔧 How to Use BSHR Commands

### **Via Slash Command**
```bash
/deep-research
keywords: ["proposal venue", "anniversary dinner"]
location: raleigh
niche: proposals
subreddits: ["raleigh", "weddingplanning", "engaged"]
max_depth: 3
```

### **Direct Script**
```bash
cd /home/primemeridianlabs/Development/Erika_TikTok
./scripts/recursive_intelligence_agent.py
```

### **Output**
Saved to: `_outputs/recursive/recursive_intelligence_YYYYMMDD_HHMMSS.json`

Contains:
- Round-by-round discoveries
- Accumulated knowledge graph
- Top competitors (ranked by mentions)
- Top pain points (ranked by severity)
- Opportunities identified
- Satisficing metadata

---

## 📚 References

**Original BSHR Loop Project**:
- Path: `/home/primemeridianlabs/Development/Projects/BSHR_Loop`
- README: Defines Brainstorm, Search, Hypothesize, Refine framework
- Key concepts: Information foraging, satisficing, naive vs informed queries

**Trading Intel V2 BSHR Implementation**:
- `bshr_multi_source.py` - Multi-platform aggregation
- `bshr_video_processor.py` - Video intelligence extraction
- `bshr_framework_demo.py` - Orchestration and satisficing

**Our Implementation**:
- `scripts/recursive_intelligence_agent.py` - BSHR loop for Reddit
- `.claude/commands/deep-research.md` - User-facing BSHR command

---

## 🎉 Key Insight

**We accidentally built a BSHR system before knowing what BSHR was!**

The recursive intelligence agent implements:
- ✅ Brainstorming (informed query generation)
- ✅ Searching (cached Reddit extraction)
- ✅ Hypothesizing (structured insight extraction)
- ✅ Refining (knowledge graph accumulation)
- ✅ Satisficing (convergence detection)

**This validates the architecture** - we independently arrived at the same pattern that information scientists use because it's the *natural way humans forage for information*.

---

**Next**: Extend BSHR to YouTube + TikTok for multi-source validation
