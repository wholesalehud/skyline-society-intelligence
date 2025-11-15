# Fabric Integration Quick Reference

**Last Updated:** 2025-10-26
**Status:** Ready for Implementation

---

## 5-Minute Summary

**What is Fabric?**
Open-source framework for AI augmentation using structured, reusable prompts called "patterns." Think of it as a battle-tested library of 228 AI prompts for common tasks.

**Why use it for Portfolio Validation?**
- Pre-built analysis frameworks (claims verification, risk assessment, predictions extraction)
- Proven prompt engineering (used by thousands, continuously refined)
- Consistent outputs (standardized analysis across all stocks)
- Fast implementation (copy/paste patterns vs. months of prompt engineering)

**Key Concept:**
```
Pattern = Structured prompt with:
1. Identity (who the AI is)
2. Steps (what to do)
3. Output format (how to structure results)
4. Input placeholder (where user content goes)
```

---

## Essential Patterns for Financial Analysis

| Pattern Name | Use For | Output | Priority |
|-------------|---------|--------|----------|
| **analyze_claims** | Verify analyst claims, news | Markdown with evidence + ratings | HIGH |
| **analyze_risk** | Company risk assessment | Risk score + mitigations | HIGH |
| **extract_predictions** | Track forecasts/guidance | JSON table with confidence | HIGH |
| **extract_recommendations** | Generate trade ideas | Bulleted action items | HIGH |
| **rate_content** | Rate research quality | Tiered rating + score | MEDIUM |
| **summarize_micro** | Quick earnings summary | < 50 word summary | MEDIUM |
| **compare_and_contrast** | Compare stocks | Markdown table | MEDIUM |
| **find_logical_fallacies** | Detect flawed reasoning | List of fallacies | LOW |

---

## Pattern to Slash Command Mapping

```
Fabric Pattern              →  Claude Code Slash Command
─────────────────────────────────────────────────────────
analyze_claims              →  /analyze-claims
analyze_risk                →  /analyze-risk
extract_predictions         →  /extract-predictions
analyze_earnings_call       →  /analyze-earnings (custom)
generate_trade_ticket       →  /generate-ticket (custom)
extract_financial_metrics   →  /extract-metrics (custom)
```

---

## Pattern Structure Template

```markdown
# IDENTITY and PURPOSE
[Who the AI is and what it does]

# STEPS
[Step-by-step instructions]

# OUTPUT INSTRUCTIONS
[Format requirements]

# INPUT
INPUT:
```

**Example:**
```markdown
# IDENTITY and PURPOSE
You are an expert earnings analyst.

# STEPS
1. Extract revenue, EPS, guidance
2. Analyze management tone
3. Generate BUY/SELL/HOLD recommendation

# OUTPUT INSTRUCTIONS
- Executive Summary (3 sentences)
- Key Metrics (table)
- Recommendation (BUY/SELL/HOLD with conviction %)

# INPUT
INPUT:
```

---

## Implementation Checklist

### Day 1: Setup (2 hours)
- [ ] `mkdir -p patterns/financial workflows strategies .claude/commands`
- [ ] Clone Fabric patterns: `git clone --depth 1 https://github.com/danielmiessler/fabric.git temp-fabric`
- [ ] Copy relevant patterns: `cp -r temp-fabric/data/patterns/* patterns/`
- [ ] Copy strategies: `cp -r temp-fabric/data/strategies/* strategies/`
- [ ] Create first slash command: `.claude/commands/analyze-earnings.md`
- [ ] Test with sample earnings call

### Week 1: Core Patterns (10 hours)
- [ ] Create `analyze_earnings_call` pattern
- [ ] Create `extract_financial_metrics` pattern
- [ ] Create `generate_trade_ticket` pattern
- [ ] Test with 5 different earnings transcripts
- [ ] Refine based on results
- [ ] Document usage

### Week 2: Integration (15 hours)
- [ ] Build pattern engine (Python)
- [ ] Create earnings analysis workflow
- [ ] Create risk assessment workflow
- [ ] Integrate with existing skills
- [ ] Add UV scripts for automation
- [ ] Build test suite

### Week 3: Scale (10 hours)
- [ ] Add 10-15 more patterns
- [ ] Create automated pipeline
- [ ] Add result caching
- [ ] Performance testing
- [ ] Team training

---

## File Structure

```
portfolio_validation_engine/
├── patterns/                      # Fabric-style patterns
│   ├── financial/
│   │   ├── analyze_earnings_call/
│   │   │   └── system.md
│   │   ├── extract_financial_metrics/
│   │   │   └── system.md
│   │   └── generate_trade_ticket/
│   │       └── system.md
│   └── analysis/
│       ├── analyze_claims/
│       ├── analyze_risk/
│       └── rate_content/
│
├── strategies/                    # Prompt strategies
│   ├── cot.json                  # Chain-of-Thought
│   ├── reflexion.json            # Self-critique
│   └── self-consistent.json      # Multi-path reasoning
│
├── workflows/                     # Pattern chains
│   ├── earnings_analysis.yaml
│   ├── risk_assessment.yaml
│   └── sentiment_analysis.yaml
│
├── .claude/
│   ├── commands/                 # Slash commands
│   │   ├── analyze-earnings.md
│   │   ├── analyze-claims.md
│   │   └── generate-ticket.md
│   └── skills/                   # Agent skills
│       ├── financial-analyzer/
│       └── risk-assessor/
│
└── scripts/
    └── run_pattern.py            # UV script for execution
```

---

## Quick Commands

### Clone Patterns
```bash
cd /path/to/project
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/danielmiessler/fabric.git temp
cd temp
git sparse-checkout set data/patterns data/strategies
cp -r data/patterns ../patterns/
cp -r data/strategies ../strategies/
cd .. && rm -rf temp
```

### Run Pattern (Python)
```python
from patterns.engine import PatternEngine

engine = PatternEngine(patterns_dir="patterns", api_key=API_KEY)

result = engine.apply_pattern(
    pattern_name="financial/analyze_earnings_call",
    input_text=earnings_transcript,
    strategy="cot"  # Optional: Chain-of-Thought
)
```

### Run Pattern (UV Script)
```bash
uv run scripts/run_pattern.py \
  analyze_earnings_call \
  earnings_transcript.txt \
  --strategy cot \
  --output analysis.md
```

### Run Workflow
```bash
uv run scripts/run_pattern.py \
  earnings_pipeline \
  transcript.txt \
  --workflow \
  --ticker AAPL \
  --output AAPL_ticket.json
```

---

## Workflow Example

**earnings_pipeline.yaml:**
```yaml
name: Earnings Analysis Pipeline

steps:
  - id: summarize
    pattern: summarize_micro
    input: ${transcript}

  - id: extract_metrics
    pattern: extract_financial_metrics
    input: ${transcript}
    strategy: cot

  - id: verify_claims
    pattern: analyze_claims
    input: ${transcript}
    strategy: reflexion

  - id: generate_ticket
    pattern: generate_trade_ticket
    inputs:
      - summarize
      - extract_metrics
      - verify_claims
    output: trade_ticket
```

**Execute:**
```bash
uv run scripts/run_pattern.py earnings_pipeline transcript.txt --workflow
```

---

## Prompt Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| **cot** (Chain-of-Thought) | Step-by-step reasoning | Complex analysis requiring logical steps |
| **reflexion** | Self-critique + refinement | High-stakes decisions, verification needed |
| **self-consistent** | Multiple reasoning paths | Checking consistency across approaches |
| **tot** (Tree-of-Thought) | Multi-path exploration | Scenario analysis, exploring alternatives |

**Usage:**
```python
# Apply strategy to any pattern
result = engine.apply_pattern(
    "analyze_claims",
    input_text,
    strategy="reflexion"  # Add strategy
)
```

---

## Common Patterns

### Single Pattern Execution
```python
# Analyze earnings call
analysis = engine.apply_pattern(
    "financial/analyze_earnings_call",
    transcript
)

# Extract metrics
metrics = engine.apply_pattern(
    "financial/extract_financial_metrics",
    transcript
)

# Verify claims
claims = engine.apply_pattern(
    "analyze_claims",
    analyst_report,
    strategy="reflexion"
)
```

### Pattern Chaining
```python
# Chain patterns manually
summary = engine.apply_pattern("summarize_micro", text)
predictions = engine.apply_pattern("extract_predictions", text)
claims = engine.apply_pattern("analyze_claims", text, strategy="cot")

# Combine results
combined = f"{summary}\n\n{predictions}\n\n{claims}"
ticket = engine.apply_pattern("generate_trade_ticket", combined)
```

### Workflow Execution
```python
# Execute pre-defined workflow
results = engine.chain_patterns(
    workflow_file=Path("workflows/earnings_pipeline.yaml"),
    inputs={"transcript": text, "ticker": "AAPL"}
)

trade_ticket = results['trade_ticket']
```

---

## Testing Patterns

### Quick Test
```bash
# Test pattern with sample input
echo "Revenue grew 15% YoY to $5.2B" | \
  uv run scripts/run_pattern.py extract_financial_metrics -
```

### Validate Output
```python
import json

result = engine.apply_pattern("extract_financial_metrics", text)
metrics = json.loads(result)  # Should parse without error

assert len(metrics) > 0, "No metrics extracted"
assert "metric" in metrics[0], "Missing metric field"
```

### Compare to Expected
```python
expected = Path("tests/expected_outputs/earnings_analysis.json").read_text()
actual = engine.apply_pattern("analyze_earnings_call", test_transcript)

# Compare structure, not exact match (AI outputs vary)
assert "EXECUTIVE SUMMARY" in actual
assert "RECOMMENDATION" in actual
```

---

## Troubleshooting

### Pattern Not Found
```
FileNotFoundError: Pattern not found: analyze_earnings_call
```
**Fix:** Check pattern path matches directory structure
```bash
ls patterns/financial/analyze_earnings_call/system.md
```

### Invalid JSON Output
```
JSONDecodeError: Expecting value: line 1 column 1
```
**Fix:** Pattern output includes markdown code blocks. Update pattern to output pure JSON:
```markdown
# OUTPUT INSTRUCTIONS
Output ONLY valid JSON. No markdown code blocks.
Do NOT include ```json, just the JSON object.
```

### Strategy Not Found
```
FileNotFoundError: Strategy not found: cot
```
**Fix:** Copy strategy files from Fabric:
```bash
cp -r temp-fabric/data/strategies/* strategies/
```

---

## Performance Tips

1. **Use appropriate models:**
   - Simple tasks (summarize): GPT-4o-mini
   - Complex analysis (claims): Claude Sonnet 4
   - Critical decisions (trade ticket): Claude Opus 4

2. **Cache results:**
   - Store pattern outputs
   - Reuse analysis across workflows
   - Avoid re-running expensive patterns

3. **Parallel execution:**
   - Run independent patterns in parallel
   - Example: Extract metrics + analyze sentiment simultaneously

4. **Optimize prompts:**
   - Remove unnecessary instructions
   - Use strategies selectively (they add tokens)
   - Test shorter vs. longer patterns

---

## Resources

### Documentation
- **Main Analysis:** `/FABRIC_REPOSITORY_ANALYSIS.md`
- **Implementation Guide:** `/FABRIC_IMPLEMENTATION_GUIDE.md`
- **Pattern Examples:** `/FABRIC_PATTERN_EXAMPLES.md`
- **This Reference:** `/FABRIC_QUICK_REFERENCE.md`

### Fabric Repository
- **GitHub:** https://github.com/danielmiessler/fabric
- **Patterns:** https://github.com/danielmiessler/fabric/tree/main/data/patterns
- **Strategies:** https://github.com/danielmiessler/fabric/tree/main/data/strategies

### Key Files
- **Pattern Engine:** `patterns/engine.py`
- **UV Script:** `scripts/run_pattern.py`
- **Workflows:** `workflows/*.yaml`
- **Tests:** `tests/patterns/`

---

## Next Steps

**Right Now (30 min):**
1. Clone Fabric patterns
2. Create first slash command (`/analyze-earnings`)
3. Test with sample earnings call

**Today (2 hours):**
1. Create 3 financial patterns
2. Test with real data
3. Refine outputs

**This Week:**
1. Build pattern engine
2. Create workflows
3. Integrate with skills

**This Month:**
1. Scale to 20+ patterns
2. Automate pipelines
3. Team adoption

**Start here:**
```bash
cd /home/primemeridianlabs/Development/Projects/portfolio_validation_engine
mkdir -p patterns workflows .claude/commands
# Then follow implementation guide
```

---

**Quick Reference Status:** Complete ✓
**Ready for:** Immediate Implementation
**Estimated First Value:** 2-4 hours
**Full Implementation:** 2-4 weeks
