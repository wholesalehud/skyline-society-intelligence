# Fabric Implementation Guide: Practical Integration for Portfolio Validation Engine

**Created:** 2025-10-26
**Status:** Ready for Implementation
**Complexity:** Moderate
**Time to First Value:** 1-2 days

---

## Quick Start: Your First Pattern in 30 Minutes

### Step 1: Clone Fabric Patterns (5 minutes)

```bash
# Navigate to your project
cd /home/primemeridianlabs/Development/Projects/portfolio_validation_engine

# Create patterns directory
mkdir -p patterns/fabric-core
cd patterns/fabric-core

# Clone just the patterns directory from Fabric
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/danielmiessler/fabric.git
cd fabric
git sparse-checkout set data/patterns
git sparse-checkout set data/strategies

# Copy to your project
cp -r data/patterns ../../
cp -r data/strategies ../../

# Cleanup
cd ../../../
rm -rf patterns/fabric-core/fabric
```

### Step 2: Create Your First Slash Command (10 minutes)

Create `/home/primemeridianlabs/Development/Projects/portfolio_validation_engine/claude_code_comprehensive_guide/.claude/commands/analyze-claims.md`:

```markdown
# Analyze Claims

Analyze the following content for truth claims, evidence, and logical quality.

## Instructions

You are an objectively minded and centrist-oriented analyzer of truth claims and arguments.

You specialize in analyzing and rating truth claims made in the input and providing both evidence in support of those claims, as well as counter-arguments and counter-evidence.

## Analysis Steps

1. Deeply analyze the truth claims and arguments being made
2. Separate the truth claims from the arguments
3. For each claim:
   - State the claim (< 16 words)
   - Provide solid, verifiable supporting evidence with references
   - Provide solid, verifiable refuting evidence with references
   - List logical fallacies with quoted examples
   - Rate quality: A (Definitely True) | B (High) | C (Medium) | D (Low) | F (Definitely False)
   - Label the claim (e.g., specious, weak, baseless, etc.)

## Output Format

### ARGUMENT SUMMARY
(< 30 words summary)

### TRUTH CLAIMS

#### CLAIM 1
**CLAIM:** [claim text]

**SUPPORT EVIDENCE:**
- [evidence with reference]

**REFUTATION EVIDENCE:**
- [counter-evidence with reference]

**LOGICAL FALLACIES:**
- [fallacy]: [quoted example]

**RATING:** [A|B|C|D|F]

**LABELS:** [label1, label2, label3]

[Repeat for each claim]

### OVERALL SCORE
**LOWEST:** [rating]
**HIGHEST:** [rating]
**AVERAGE:** [rating]

### OVERALL ANALYSIS
(30-word summary of argument quality, weaknesses, strengths, and recommendation)

---

## Content to Analyze

{{input}}
```

### Step 3: Test the Command (5 minutes)

In Claude Code, run:

```
/analyze-claims

[Paste an analyst report or earnings call excerpt here]
```

### Step 4: Create a Financial-Specific Pattern (10 minutes)

Create `patterns/financial/analyze_earnings_call/system.md`:

```markdown
# IDENTITY and PURPOSE

You are an expert financial analyst specializing in earnings call analysis. You extract key financial metrics, forward guidance, management sentiment, and generate actionable insights.

Take a step back and think step-by-step about how to achieve the best analysis.

# STEPS

1. Extract all quantitative metrics mentioned (revenue, EPS, margins, growth rates, etc.)
2. Identify forward guidance with specific dates and confidence levels
3. Analyze management tone and sentiment (bullish, neutral, bearish)
4. List all disclosed risks and concerns
5. Compare metrics to prior quarter and analyst expectations
6. Identify positive and negative surprises
7. Extract strategic initiatives and business updates
8. Generate investment recommendation

# OUTPUT INSTRUCTIONS

## EXECUTIVE SUMMARY
Provide a 3-sentence summary of the earnings call outcome and investment implication.

## KEY METRICS

| Metric | Actual | Prior Q | YoY Change | Analyst Est | Beat/Miss |
|--------|--------|---------|------------|-------------|-----------|
| Revenue | | | | | |
| EPS | | | | | |
| Operating Margin | | | | | |
| Free Cash Flow | | | | | |
| [Add others] | | | | | |

## FORWARD GUIDANCE

| Metric | Guidance | Period | Confidence | Commentary |
|--------|----------|--------|------------|------------|
| | | | HIGH/MED/LOW | |

## MANAGEMENT SENTIMENT

**Overall Tone:** [Bullish/Neutral/Bearish] (1-10 scale: [score])

**Confidence Level:** [High/Medium/Low]

**Key Quotes:**
- "[Quote supporting sentiment assessment]"
- "[Quote supporting sentiment assessment]"

## STRATEGIC UPDATES

**New Initiatives:**
- [Initiative 1]
- [Initiative 2]

**Business Developments:**
- [Development 1]
- [Development 2]

## RISK FACTORS DISCLOSED

**Critical Risks:**
- [Risk with potential impact]

**Medium Risks:**
- [Risk with moderate impact]

## SURPRISES & HIGHLIGHTS

**Positive Surprises:**
- [Unexpected good news]

**Negative Surprises:**
- [Unexpected concerns]

**Key Takeaways:**
- [Insight 1]
- [Insight 2]
- [Insight 3]

## INVESTMENT THESIS UPDATE

**Bull Case:**
- [Argument for buying]

**Bear Case:**
- [Argument against buying]

**Base Case:**
- [Most likely outcome]

## RECOMMENDATION

**Action:** BUY | SELL | HOLD | PASS

**Confidence:** [0-100%]

**Rationale:** (50 words explaining recommendation)

**Price Target Impact:** RAISE | LOWER | MAINTAIN

**Position Sizing:** INCREASE | DECREASE | MAINTAIN

# INPUT

INPUT:
```

---

## Implementation Patterns

### Pattern 1: Slash Command → Pattern Mapping

**File Structure:**
```
.claude/
└── commands/
    ├── analyze-claims.md        → patterns/analysis/analyze_claims/
    ├── analyze-earnings.md      → patterns/financial/analyze_earnings_call/
    ├── analyze-risk.md          → patterns/analysis/analyze_risk/
    ├── extract-predictions.md   → patterns/extraction/extract_predictions/
    └── rate-quality.md          → patterns/rating/rate_content/
```

**Command Template:**
```markdown
# [Command Name]

[Brief description]

## Instructions
[Pattern system.md content]

## Output Format
[Expected output structure]

---

## Input
{{input}}
```

### Pattern 2: Agent Skill → Pattern Integration

**Skill Directory:**
```
skills/
└── financial-analyzer/
    ├── skill.yaml                  # Skill configuration
    ├── patterns/
    │   ├── analyze_earnings.md
    │   ├── extract_metrics.md
    │   └── rate_quality.md
    └── workflows/
        └── earnings_pipeline.yaml
```

**skill.yaml:**
```yaml
name: financial-analyzer
description: "Analyzes financial reports using structured patterns"
version: "1.0.0"

patterns:
  - name: analyze_earnings
    file: patterns/analyze_earnings.md
    output: json
  - name: extract_metrics
    file: patterns/extract_metrics.md
    output: json
  - name: rate_quality
    file: patterns/rate_quality.md
    output: json

workflows:
  earnings_analysis:
    file: workflows/earnings_pipeline.yaml
    patterns:
      - analyze_earnings
      - extract_metrics
      - rate_quality

variables:
  ticker: ${TICKER}
  sector: ${SECTOR}
  analyst: ${ANALYST_NAME}
```

**earnings_pipeline.yaml:**
```yaml
name: Earnings Analysis Pipeline
description: "Complete earnings call analysis workflow"

steps:
  - id: summarize
    pattern: summarize_micro
    input: ${transcript}
    output: summary

  - id: extract_metrics
    pattern: extract_financial_metrics
    input: ${transcript}
    output: metrics
    strategy: cot

  - id: extract_guidance
    pattern: extract_predictions
    input: ${transcript}
    output: guidance

  - id: analyze_sentiment
    pattern: analyze_sentiment
    input: ${transcript}
    output: sentiment

  - id: verify_claims
    pattern: analyze_claims
    input: ${transcript}
    output: claims
    strategy: reflexion

  - id: generate_ticket
    pattern: generate_trade_ticket
    inputs:
      - summary
      - metrics
      - guidance
      - sentiment
      - claims
    output: trade_ticket
    format: json

output:
  file: "${ticker}_${date}_trade_ticket.json"
  format: json
  schema: trade_ticket_v1
```

### Pattern 3: Python Integration

**patterns/engine.py:**
```python
from pathlib import Path
from typing import Dict, List, Optional
import yaml
import anthropic

class PatternEngine:
    """Execute Fabric-style patterns with Claude API"""

    def __init__(self, patterns_dir: Path, api_key: str):
        self.patterns_dir = Path(patterns_dir)
        self.client = anthropic.Anthropic(api_key=api_key)

    def load_pattern(self, pattern_path: str) -> str:
        """Load pattern system prompt from Markdown file"""
        full_path = self.patterns_dir / pattern_path / "system.md"
        if not full_path.exists():
            raise FileNotFoundError(f"Pattern not found: {full_path}")
        return full_path.read_text()

    def load_strategy(self, strategy_name: str) -> dict:
        """Load prompt strategy from JSON"""
        strategy_path = self.patterns_dir.parent / "strategies" / f"{strategy_name}.json"
        import json
        return json.loads(strategy_path.read_text())

    def apply_pattern(
        self,
        pattern_name: str,
        input_text: str,
        strategy: Optional[str] = None,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4000
    ) -> str:
        """Apply a pattern to input text with optional strategy"""

        # Load pattern system prompt
        system_prompt = self.load_pattern(pattern_name)

        # Apply strategy if specified
        if strategy:
            strategy_config = self.load_strategy(strategy)
            system_prompt = f"{system_prompt}\n\n{strategy_config['prompt']}"

        # Replace INPUT placeholder
        full_prompt = system_prompt.replace("INPUT:", input_text)

        # Execute with Claude API
        response = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )

        return response.content[0].text

    def chain_patterns(
        self,
        workflow_file: Path,
        inputs: Dict[str, str],
        model: str = "claude-sonnet-4-5-20250929"
    ) -> Dict[str, str]:
        """Execute a workflow of chained patterns"""

        workflow = yaml.safe_load(workflow_file.read_text())
        results = {}

        for step in workflow['steps']:
            step_id = step['id']
            pattern = step['pattern']
            strategy = step.get('strategy')

            # Get input for this step
            if 'inputs' in step:
                # Combine multiple previous results
                step_input = "\n\n---\n\n".join(
                    results[inp] for inp in step['inputs']
                )
            elif 'input' in step:
                # Use specified input (could be variable)
                input_ref = step['input']
                if input_ref.startswith('${') and input_ref.endswith('}'):
                    var_name = input_ref[2:-1]
                    step_input = inputs.get(var_name, "")
                else:
                    step_input = results.get(input_ref, input_ref)
            else:
                raise ValueError(f"No input specified for step: {step_id}")

            # Execute pattern
            result = self.apply_pattern(
                pattern,
                step_input,
                strategy=strategy,
                model=model
            )

            # Store result
            output_key = step.get('output', step_id)
            results[output_key] = result

        return results


# Example usage
if __name__ == "__main__":
    import os

    engine = PatternEngine(
        patterns_dir=Path("patterns"),
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    # Single pattern execution
    transcript = Path("sample_earnings_call.txt").read_text()

    analysis = engine.apply_pattern(
        pattern_name="financial/analyze_earnings_call",
        input_text=transcript,
        strategy="cot"
    )

    print("EARNINGS ANALYSIS:")
    print(analysis)

    # Workflow execution
    workflow = Path("workflows/earnings_pipeline.yaml")
    results = engine.chain_patterns(
        workflow_file=workflow,
        inputs={"transcript": transcript}
    )

    print("\nTRADE TICKET:")
    print(results['trade_ticket'])
```

**Usage Example:**
```python
# earnings_analyzer.py
from patterns.engine import PatternEngine
from pathlib import Path
import os

def analyze_earnings_call(transcript_file: Path, ticker: str):
    """Analyze earnings call and generate trade ticket"""

    engine = PatternEngine(
        patterns_dir=Path("patterns"),
        api_key=os.environ["ANTHROPIC_API_KEY"]
    )

    transcript = transcript_file.read_text()

    # Execute complete workflow
    results = engine.chain_patterns(
        workflow_file=Path("workflows/earnings_pipeline.yaml"),
        inputs={
            "transcript": transcript,
            "ticker": ticker,
            "date": "2025-10-26"
        }
    )

    # Save results
    output_file = Path(f"output/{ticker}_analysis.json")
    output_file.write_text(results['trade_ticket'])

    print(f"Analysis complete: {output_file}")
    return results

# Run analysis
if __name__ == "__main__":
    analyze_earnings_call(
        transcript_file=Path("data/AAPL_Q3_2025_transcript.txt"),
        ticker="AAPL"
    )
```

### Pattern 4: UV Script Integration

Since you use UV for scripting, here's a UV-compatible pattern executor:

**scripts/run_pattern.py:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic>=0.39.0",
#     "pyyaml>=6.0.1",
# ]
# ///

"""
Run Fabric patterns using UV for dependency management

Usage:
    uv run scripts/run_pattern.py analyze_earnings_call input.txt
    uv run scripts/run_pattern.py --workflow earnings_pipeline --ticker AAPL input.txt
"""

import argparse
import json
import sys
from pathlib import Path
import anthropic
import yaml

def load_pattern(pattern_name: str, patterns_dir: Path = Path("patterns")) -> str:
    """Load pattern system.md file"""
    pattern_file = patterns_dir / pattern_name / "system.md"
    if not pattern_file.exists():
        # Try with .md extension
        pattern_file = patterns_dir / f"{pattern_name}.md"

    if not pattern_file.exists():
        raise FileNotFoundError(f"Pattern not found: {pattern_name}")

    return pattern_file.read_text()

def load_strategy(strategy_name: str, strategies_dir: Path = Path("strategies")) -> dict:
    """Load strategy JSON"""
    strategy_file = strategies_dir / f"{strategy_name}.json"
    if not strategy_file.exists():
        raise FileNotFoundError(f"Strategy not found: {strategy_name}")

    return json.loads(strategy_file.read_text())

def execute_pattern(
    pattern_name: str,
    input_text: str,
    strategy: str | None = None,
    model: str = "claude-sonnet-4-5-20250929",
    api_key: str | None = None
) -> str:
    """Execute a single pattern"""

    client = anthropic.Anthropic(api_key=api_key)

    # Load pattern
    system_prompt = load_pattern(pattern_name)

    # Apply strategy if specified
    if strategy:
        strategy_config = load_strategy(strategy)
        system_prompt = f"{system_prompt}\n\n{strategy_config['prompt']}"

    # Replace INPUT placeholder
    full_prompt = system_prompt.replace("INPUT:", input_text)

    # Execute
    response = client.messages.create(
        model=model,
        max_tokens=4000,
        messages=[{"role": "user", "content": full_prompt}]
    )

    return response.content[0].text

def execute_workflow(
    workflow_name: str,
    inputs: dict,
    workflows_dir: Path = Path("workflows"),
    model: str = "claude-sonnet-4-5-20250929",
    api_key: str | None = None
) -> dict:
    """Execute a workflow of chained patterns"""

    workflow_file = workflows_dir / f"{workflow_name}.yaml"
    if not workflow_file.exists():
        raise FileNotFoundError(f"Workflow not found: {workflow_name}")

    workflow = yaml.safe_load(workflow_file.read_text())
    results = {}

    print(f"Executing workflow: {workflow['name']}")

    for step in workflow['steps']:
        step_id = step['id']
        pattern = step['pattern']
        strategy = step.get('strategy')

        print(f"  Step {step_id}: {pattern}{'(' + strategy + ')' if strategy else ''}")

        # Determine input
        if 'inputs' in step:
            step_input = "\n\n---\n\n".join(results[inp] for inp in step['inputs'])
        elif 'input' in step:
            input_ref = step['input']
            if input_ref.startswith('${') and input_ref.endswith('}'):
                var_name = input_ref[2:-1]
                step_input = inputs.get(var_name, "")
            else:
                step_input = results.get(input_ref, input_ref)
        else:
            raise ValueError(f"No input for step: {step_id}")

        # Execute
        result = execute_pattern(pattern, step_input, strategy, model, api_key)
        output_key = step.get('output', step_id)
        results[output_key] = result

    return results

def main():
    parser = argparse.ArgumentParser(description="Execute Fabric patterns")
    parser.add_argument("pattern_or_workflow", help="Pattern name or workflow file")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("--workflow", action="store_true", help="Execute as workflow")
    parser.add_argument("--strategy", help="Prompt strategy (cot, reflexion, etc.)")
    parser.add_argument("--model", default="claude-sonnet-4-5-20250929", help="Claude model")
    parser.add_argument("--output", "-o", help="Output file")
    parser.add_argument("--ticker", help="Stock ticker (for workflows)")

    args = parser.parse_args()

    # Read input
    input_text = Path(args.input_file).read_text()

    # Execute
    if args.workflow:
        inputs = {"transcript": input_text}
        if args.ticker:
            inputs["ticker"] = args.ticker
            inputs["date"] = "2025-10-26"

        results = execute_workflow(
            args.pattern_or_workflow,
            inputs,
            model=args.model
        )

        # Output final result
        output = results.get('trade_ticket', results)
        print("\n" + "="*80)
        print("WORKFLOW RESULTS")
        print("="*80 + "\n")
        print(output)

        if args.output:
            Path(args.output).write_text(output)
            print(f"\nSaved to: {args.output}")

    else:
        result = execute_pattern(
            args.pattern_or_workflow,
            input_text,
            strategy=args.strategy,
            model=args.model
        )

        print("\n" + "="*80)
        print("PATTERN RESULT")
        print("="*80 + "\n")
        print(result)

        if args.output:
            Path(args.output).write_text(result)
            print(f"\nSaved to: {args.output}")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
# Single pattern
uv run scripts/run_pattern.py analyze_earnings_call earnings_transcript.txt

# With strategy
uv run scripts/run_pattern.py analyze_claims analyst_report.txt --strategy cot

# Workflow execution
uv run scripts/run_pattern.py earnings_pipeline earnings.txt --workflow --ticker AAPL -o output/AAPL_ticket.json
```

---

## Sample Patterns for Financial Analysis

### Pattern: Extract Financial Metrics

**patterns/financial/extract_financial_metrics/system.md:**
```markdown
# IDENTITY and PURPOSE

You extract all financial metrics from unstructured text into a structured, machine-readable format.

# STEPS

1. Scan text for all numerical financial data
2. Identify metric names and values
3. Extract time periods and comparisons
4. Note units (millions, billions, percentage, etc.)
5. Determine confidence based on source clarity
6. Extract context and qualifiers

# OUTPUT INSTRUCTIONS

Output as JSON array with this schema:

```json
[
  {
    "metric": "string (e.g., 'Revenue', 'EPS', 'Operating Margin')",
    "value": "number",
    "unit": "string (e.g., 'millions', 'billions', 'percent')",
    "period": "string (e.g., 'Q3 2025', '2025', 'TTM')",
    "comparison_type": "YoY|QoQ|Expected|null",
    "comparison_value": "number|null",
    "source": "string (where in document this came from)",
    "confidence": "HIGH|MEDIUM|LOW",
    "context": "string (additional context if important)"
  }
]
```

Rules:
- Extract ALL numerical metrics, even if they seem minor
- If value is a range, use midpoint and note in context
- If confidence is LOW, explain why in context
- Always include units
- For percentages, use decimal (e.g., 15.5 for 15.5%)

# INPUT

INPUT:
```

### Pattern: Generate Trade Ticket

**patterns/financial/generate_trade_ticket/system.md:**
```markdown
# IDENTITY and PURPOSE

You synthesize all analysis results into a Master Trade Ticket with clear BUY/SELL/HOLD/PASS recommendation.

# STEPS

1. Review all provided analysis results
2. Weigh evidence from each analysis type
3. Identify consensus and conflicts
4. Determine conviction level
5. Calculate appropriate position sizing
6. Set entry, exit, and stop loss levels
7. List key risks and catalysts
8. Draft board review notes

# OUTPUT INSTRUCTIONS

Output in JSON format with this exact schema:

```json
{
  "ticker": "string",
  "company_name": "string",
  "analysis_date": "YYYY-MM-DD",
  "recommendation": "BUY|SELL|HOLD|PASS",
  "conviction": "number (0-100)",
  "rationale": "string (50-100 words)",

  "pricing": {
    "current_price": "number",
    "entry_price_range": {
      "low": "number",
      "high": "number"
    },
    "price_targets": [
      {
        "target": "number",
        "timeframe": "string (e.g., '6 months', '1 year')",
        "probability": "number (0-100)"
      }
    ],
    "stop_loss": "number"
  },

  "position_sizing": {
    "recommended_weight": "string (e.g., '2-3%', '5%')",
    "position_size_rationale": "string",
    "risk_budget": "string (e.g., '1% portfolio risk')"
  },

  "analysis_summary": {
    "technical_score": "number (0-100)",
    "fundamental_score": "number (0-100)",
    "sentiment_score": "number (0-100)",
    "risk_score": "number (0-100, higher = more risk)",
    "quality_score": "number (0-100)"
  },

  "catalysts": [
    {
      "catalyst": "string",
      "timeframe": "string",
      "impact": "HIGH|MEDIUM|LOW",
      "probability": "number (0-100)"
    }
  ],

  "risks": [
    {
      "risk": "string",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "mitigation": "string"
    }
  ],

  "execution_plan": {
    "entry_strategy": "string (e.g., 'Scale in over 2-3 days', 'Single entry')",
    "monitoring_frequency": "string (e.g., 'Daily', 'Weekly')",
    "review_triggers": ["string"],
    "exit_strategy": "string"
  },

  "board_notes": "string (200-300 words for investment committee)",

  "supporting_analysis": {
    "earnings_analysis": "summary|null",
    "technical_analysis": "summary|null",
    "risk_assessment": "summary|null",
    "sentiment_analysis": "summary|null"
  },

  "metadata": {
    "analyst": "string",
    "model_version": "string",
    "patterns_used": ["string"],
    "data_sources": ["string"]
  }
}
```

Rules:
- PASS recommendation should be used liberally (better to pass than force)
- Conviction must match recommendation strength
- Stop loss is REQUIRED for BUY/SELL
- Board notes must be standalone summary
- All scores 0-100, calibrated across portfolio

# INPUT

Provide all analysis results in the following format:

EARNINGS ANALYSIS:
[results]

TECHNICAL ANALYSIS:
[results]

RISK ASSESSMENT:
[results]

SENTIMENT ANALYSIS:
[results]

INPUT:
```

---

## Testing & Validation

### Test Suite Structure

```
tests/
├── patterns/
│   ├── test_analyze_earnings.py
│   ├── test_extract_metrics.py
│   └── test_generate_ticket.py
├── workflows/
│   ├── test_earnings_pipeline.py
│   └── test_risk_assessment.py
├── fixtures/
│   ├── sample_earnings_transcript.txt
│   ├── sample_10k.txt
│   └── sample_analyst_report.txt
└── expected_outputs/
    ├── earnings_analysis.json
    └── trade_ticket.json
```

### Sample Test

**tests/patterns/test_analyze_earnings.py:**
```python
#!/usr/bin/env uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic>=0.39.0",
#     "pytest>=8.0.0",
# ]
# ///

import pytest
from pathlib import Path
from patterns.engine import PatternEngine
import json

@pytest.fixture
def engine():
    return PatternEngine(
        patterns_dir=Path("patterns"),
        api_key="sk-ant-test"  # Use env var in production
    )

def test_analyze_earnings_output_format(engine):
    """Test that earnings analysis produces expected output structure"""

    sample_transcript = Path("tests/fixtures/sample_earnings_transcript.txt").read_text()

    result = engine.apply_pattern(
        pattern_name="financial/analyze_earnings_call",
        input_text=sample_transcript
    )

    # Check for required sections
    assert "EXECUTIVE SUMMARY" in result
    assert "KEY METRICS" in result
    assert "FORWARD GUIDANCE" in result
    assert "RECOMMENDATION" in result

def test_extract_metrics_json_output(engine):
    """Test that metrics extraction produces valid JSON"""

    sample_text = """
    Revenue for Q3 was $5.2 billion, up 15% year-over-year.
    Operating margin improved to 18.5% from 16.2% last quarter.
    Free cash flow was $850 million.
    """

    result = engine.apply_pattern(
        pattern_name="financial/extract_financial_metrics",
        input_text=sample_text
    )

    # Should be valid JSON
    metrics = json.loads(result)

    # Should have 3+ metrics
    assert len(metrics) >= 3

    # Check structure
    required_fields = ["metric", "value", "unit", "period", "confidence"]
    for metric in metrics:
        for field in required_fields:
            assert field in metric

def test_earnings_workflow_integration(engine):
    """Test complete earnings analysis workflow"""

    transcript = Path("tests/fixtures/sample_earnings_transcript.txt").read_text()

    results = engine.chain_patterns(
        workflow_file=Path("workflows/earnings_pipeline.yaml"),
        inputs={"transcript": transcript, "ticker": "TEST"}
    )

    # Should have all expected outputs
    assert "summary" in results
    assert "metrics" in results
    assert "trade_ticket" in results

    # Trade ticket should be valid JSON
    ticket = json.loads(results["trade_ticket"])
    assert "recommendation" in ticket
    assert ticket["recommendation"] in ["BUY", "SELL", "HOLD", "PASS"]
    assert "conviction" in ticket
    assert 0 <= ticket["conviction"] <= 100

# Run with: uv run pytest tests/patterns/test_analyze_earnings.py
```

---

## Deployment Checklist

### Week 1: Foundation
- [ ] Clone Fabric patterns repository
- [ ] Create patterns/ directory structure
- [ ] Port 5 core patterns (analyze_claims, analyze_risk, extract_predictions, rate_content, summarize_micro)
- [ ] Create 2 financial patterns (analyze_earnings_call, extract_financial_metrics)
- [ ] Set up pattern engine (Python)
- [ ] Create 3 slash commands
- [ ] Test with sample data

### Week 2: Integration
- [ ] Integrate patterns with existing skills
- [ ] Create earnings analysis workflow
- [ ] Create risk assessment workflow
- [ ] Build UV scripts for pattern execution
- [ ] Add test suite
- [ ] Document usage

### Week 3: Scale
- [ ] Add 10 more patterns
- [ ] Create generate_trade_ticket pattern
- [ ] Build automated pipeline
- [ ] Add result caching
- [ ] Performance testing

### Week 4: Refinement
- [ ] Collect user feedback
- [ ] Refine patterns based on results
- [ ] Add pattern versioning
- [ ] Build pattern analytics
- [ ] Team training

---

## Next Steps

1. **Right Now (30 min):**
   - Clone Fabric patterns
   - Create first slash command
   - Test with sample earnings call

2. **Today (2 hours):**
   - Create analyze_earnings_call pattern
   - Test with 3 real earnings transcripts
   - Refine based on results

3. **This Week:**
   - Build pattern engine
   - Create workflows
   - Integrate with skills

4. **This Month:**
   - Scale to 20+ patterns
   - Automate pipelines
   - Team adoption

**Start here:**
```bash
cd /home/primemeridianlabs/Development/Projects/portfolio_validation_engine
mkdir -p patterns workflows .claude/commands
# Then follow Quick Start above
```

---

**Implementation Status:** Ready to Execute
**Estimated Time to Production:** 2-4 weeks
**Complexity:** Moderate (good documentation, proven patterns)
**Risk Level:** Low (incremental adoption, well-tested framework)
