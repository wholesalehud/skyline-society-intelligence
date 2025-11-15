# Agent Architecture Quick Reference

**Fast lookup for agent patterns, configurations, and best practices**

---

## Agent YAML Templates

### Basic Agent Template
```yaml
---
name: agent-name
description: Clear description with activation keywords
tools: [Read, Write, Bash]
model: sonnet
---
```

### Production Agent Template
```yaml
---
name: production-agent
description: PROACTIVELY handles X when user mentions Y. Use immediately for Z scenarios.
tools: [Bash, Read, Write, WebFetch, Grep, mcp__memory__*]
model: sonnet
color: blue
proactive: true
---
```

### Financial Agent Template
```yaml
---
name: financial-intelligence-agent
description: Analyzes market data, sentiment, and technical indicators for trading decisions
tools: [Bash, Read, Write, WebFetch, mcp__yfinance__*, mcp__memory__*]
model: sonnet
color: green
proactive: true
---
```

---

## Model Selection Guide

| Task Type | Model | Cost | Use When |
|-----------|-------|------|----------|
| **Filtering** | haiku | $ | Screening tickers, data validation |
| **Analysis** | sonnet | $$ | Trade analysis, sentiment scoring |
| **Strategy** | opus | $$$ | Portfolio optimization, complex decisions |
| **Orchestration** | opus | $$$ | Multi-agent coordination, planning |

**Cost Reference**: $ = $0.01-0.10, $$ = $0.10-0.50, $$$ = $0.50+

---

## 15-Layer Pattern Taxonomy (Condensed)

| Layer | Pattern | Portfolio Application |
|-------|---------|----------------------|
| 1 | UV Scripts | Market data fetchers |
| 2 | Programmable Claude | Multi-broker coordination |
| 3 | Multi-Model (HOP/LOP) | Cost optimization |
| 4 | Context & Config | Efficient context loading |
| 5 | Sub-Agents | Specialized validation |
| 6 | Hooks | Automated storage/alerts |
| 7 | Plan Mode | Complex workflows |
| 8 | MCP Servers | Broker APIs, market data |
| 9 | Observability | Workflow monitoring |
| 10 | Parallel Execution | Batch portfolio validation |
| 11 | Context Architecture | Knowledge organization |
| 12 | Tool Transparency | Cost tracking |
| 13 | Infinite Loop | Adaptive validation |
| 14 | Custom Commands | Reusable workflows |
| 15 | Voice-First | Hands-free monitoring |

---

## Agent Coordination Patterns

### Sequential Workflow
```yaml
Step_1: market-data-validator
Step_2: sentiment-analyzer
Step_3: technical-analyzer
Step_4: risk-assessor
Step_5: trade-ticket-generator
```

### Parallel Workflow
```yaml
Wave_1_Parallel:
  - market-data-validator
  - sentiment-analyzer
  - technical-analyzer

Wave_2_Sequential:
  - risk-assessor (uses Wave_1 results)
  - trade-ticket-generator
```

### Meta-Orchestration
```yaml
Orchestrator: portfolio-validation-orchestrator

Research_Phase:
  - Discover available tools
  - Generate optimal pipeline

Execution_Phase:
  - Launch parallel agents
  - Coordinate results
  - Generate final report
```

---

## Parallel Execution Strategy

### Git Worktree Setup
```bash
# Create parallel workers
git worktree add ../validator_worker_1 main
git worktree add ../validator_worker_2 main
git worktree add ../validator_worker_3 main
```

### Assignment Matrix
```yaml
Worker_1: {tickers: 1-20, model: "sonnet"}
Worker_2: {tickers: 21-40, model: "sonnet"}
Worker_3: {tickers: 41-50, model: "haiku"}
```

### Performance
- **Sequential**: 50 tickers × 5 min = 250 min (4.2 hours)
- **Parallel (3 workers)**: 50 tickers / 3 = ~17 tickers × 5 min = 85 min (1.4 hours)
- **Speed Improvement**: 3x faster

---

## MCP Server Integration

### Common MCP Servers for Finance

#### YFinance (Market Data)
```json
{
  "mcpServers": {
    "yfinance": {
      "command": "uvx",
      "args": ["mcp-server-yfinance"]
    }
  }
}
```

**Available Tools**:
- `mcp__yfinance__get_quote` - Real-time quotes
- `mcp__yfinance__get_historical` - Historical data
- `mcp__yfinance__get_info` - Company information

#### ChromaDB (Vector Storage)
```json
{
  "mcpServers": {
    "chromadb": {
      "command": "mcp-server-chromadb",
      "args": ["--path", "./chroma_db"]
    }
  }
}
```

#### Memory (Persistent Knowledge)
```json
{
  "mcpServers": {
    "memory": {
      "command": "mcp-server-memory"
    }
  }
}
```

---

## Hook Patterns

### On Validation Complete
```python
# .claude/hooks/on_validation_complete.py
#!/usr/bin/env python3
import json
import sys

def handle_completion(trade_ticket):
    # Store in database
    save_to_db(trade_ticket)

    # Send notification
    notify_user(trade_ticket)

    # Update dashboard
    update_dashboard(trade_ticket)

if __name__ == "__main__":
    trade_ticket = json.loads(sys.stdin.read())
    handle_completion(trade_ticket)
```

### On Market Event
```python
# .claude/hooks/on_market_event.py
#!/usr/bin/env python3
import subprocess

def trigger_validation(ticker, event_type):
    if event_type in ['price_alert', 'earnings', 'news']:
        subprocess.run([
            "claude",
            "/validate-ticker",
            f"$TICKER={ticker}"
        ])
```

---

## Context Management

### Project CLAUDE.md (Keep <1000 tokens)
```markdown
# Portfolio Validation Engine

**Mission**: Automated validation with web intelligence

## Architecture
- **Agents**: Data collectors
- **Skills**: Validation logic
- **Commands**: Orchestration

## Quick Actions
- `/validate-ticker $TICKER=AAPL`
- "Validate AAPL position"
```

### Agent CLAUDE.md (Detailed Instructions)
```markdown
# Market Data Validator Agent

## Purpose
Validate market data accuracy

## Workflow
1. Fetch quote from yfinance
2. Check bid/ask spread
3. Validate volume
4. Return validation result

## Usage
```bash
uv run python validate.py --ticker AAPL
```
```

---

## Common Agent Workflows

### Single Ticker Validation
```bash
# Command
/validate-ticker $TICKER="AAPL" $VALUE=50000 $BASIS=45000

# Workflow
1. market-data-validator → validates prices
2. sentiment-analyzer → checks social sentiment
3. technical-analyzer → analyzes charts
4. risk-assessor → evaluates risk
5. trade-ticket-generator → creates report
```

### Batch Portfolio Validation
```bash
# Command
/validate-portfolio $INPUT="portfolio.csv"

# Workflow (Parallel)
Wave_1: Process tickers 1-10 (worker_1)
Wave_2: Process tickers 11-20 (worker_2)
Wave_3: Process tickers 21-30 (worker_3)
Integration: Merge results, generate report
```

### Real-Time Monitoring
```bash
# Setup webhook
/setup-alerts $TICKER="AAPL" $TYPE="price,earnings,news"

# Workflow
1. Market event occurs
2. Webhook triggers on_market_event hook
3. Hook launches validation workflow
4. Results sent to notification system
```

---

## Error Recovery Patterns

### Checkpoint System
```python
# Save checkpoint after each major step
checkpoint_manager.save_checkpoint(
    workflow_id="portfolio_validation_123",
    step=2,
    data={"tickers_processed": 10, "results": results}
)

# Resume from checkpoint on failure
step, data = checkpoint_manager.resume_from_checkpoint(
    workflow_id="portfolio_validation_123"
)
```

### Graceful Degradation
```python
# If real-time data fails, use cached data
try:
    data = fetch_real_time_data(ticker)
except Exception:
    data = load_cached_data(ticker)
    data['warning'] = 'Using cached data'
```

---

## Performance Optimization

### Token Reduction Strategies
1. **Compact Context**: Keep .claude/CLAUDE.md <1000 tokens
2. **Lazy Loading**: Load agents/skills only when needed
3. **Delegation**: Use sub-agents instead of monolithic prompts
4. **Caching**: Store frequently accessed data

### Speed Optimization
1. **Parallel Processing**: Use git worktrees for batch operations
2. **Model Selection**: Use haiku for filtering, sonnet for analysis
3. **Async Operations**: Run independent tasks concurrently
4. **MCP Integration**: Direct API access vs web scraping

### Cost Optimization
```yaml
Filtering: Use haiku ($0.01 per 1K tokens)
Analysis: Use sonnet ($0.10 per 1K tokens)
Strategy: Use opus only for critical decisions ($1.00 per 1K tokens)

Example Workflow Cost:
- 10 tickers × haiku filter = $0.10
- 3 tickers × sonnet analysis = $0.30
- 1 ticker × opus strategy = $1.00
Total: $1.40 (vs $10+ all opus)
```

---

## Agent Communication Protocol

### Shared State Files
```bash
.claude/shared/
├── agent_status.json      # Real-time agent progress
├── discovered_data.json   # Cross-agent data sharing
├── completion_signals.json # Synchronization triggers
└── metrics.json           # Performance tracking
```

### State Management
```python
# Write state
coordinator.write_state("risk-assessor", {
    "status": "processing",
    "progress": 0.5,
    "current_ticker": "AAPL"
})

# Read state
state = coordinator.read_state("sentiment-analyzer")

# Signal completion
coordinator.signal_completion("technical-analyzer", {
    "ticker": "AAPL",
    "signal": "bullish",
    "confidence": 0.78
})
```

---

## Validation Scoring Framework

### Component Scores (0-100)
```yaml
Market_Data: 0-100 (data quality)
Sentiment: 0-100 (bullish vs bearish)
Technical: 0-100 (trend strength)
Risk: 0-100 (low risk = high score)
Alpha: -100 to +100 (vs benchmark)
```

### Overall Score Calculation
```python
overall_score = (
    0.25 * market_data_score +
    0.20 * sentiment_score +
    0.20 * technical_score +
    0.20 * risk_score +
    0.15 * alpha_score
)
```

### Recommendation Thresholds
```yaml
80-100: STRONG BUY
60-79: BUY
40-59: HOLD
20-39: SELL
0-19: STRONG SELL
```

---

## Troubleshooting Quick Fixes

### Agent Not Activating
```bash
# Check frontmatter description has keywords
# Verify agent in searchPaths
# Test manual invocation: @agent-name "test"
```

### High Token Usage
```bash
# Check .claude/CLAUDE.md token count
/config autocompact false
# Use /context to inspect what's loaded
```

### Slow Execution
```bash
# Use parallel processing
# Switch to faster models for filtering
# Cache frequently accessed data
```

### MCP Server Connection Failed
```bash
# Verify MCP server installed: uvx mcp-server-yfinance --version
# Check settings.json configuration
# Restart Claude Code
```

---

## Production Deployment Checklist

### Pre-Deployment
- [ ] All agents have YAML frontmatter
- [ ] Project CLAUDE.md <1000 tokens
- [ ] MCP servers configured
- [ ] Hooks tested
- [ ] Error recovery implemented
- [ ] Metrics collection enabled

### Testing
- [ ] Single ticker validation works
- [ ] Batch validation works
- [ ] Parallel execution works
- [ ] Hooks trigger correctly
- [ ] MCP servers responding
- [ ] Error recovery works

### Monitoring
- [ ] Token usage tracking
- [ ] Execution time monitoring
- [ ] Success/failure rates
- [ ] Cost per validation
- [ ] API rate limits

---

## Quick Command Reference

### Validation Commands
```bash
# Single ticker
/validate-ticker $TICKER="AAPL" $VALUE=50000 $BASIS=45000

# Batch
/validate-portfolio $INPUT="portfolio.csv"

# Full analysis
/full-analysis $TICKER="MSFT"
```

### Agent Management
```bash
# List agents
@list-agents

# Invoke specific agent
@risk-assessor "Analyze AAPL risk"

# Check agent status
/agent-status
```

### System Commands
```bash
# Check configuration
/config

# View context
/context

# Clear context
/clear

# Help
/help agents
```

---

## Resource Links

**Core Documentation**:
- [Agent Architecture Library](/home/primemeridianlabs/Development/Projects/portfolio_validation_engine/claude_code_comprehensive_guide/AGENT_ARCHITECTURE_LIBRARY.md)
- [Multi-Agent Implementation Guide](/home/primemeridianlabs/Development/Projects/portfolio_validation_engine/docs/architecture/MULTI_AGENT_IMPLEMENTATION_GUIDE.md)
- [Video Content Integration Plan](/home/primemeridianlabs/Development/Projects/portfolio_validation_engine/claude_code_comprehensive_guide/VIDEO_CONTENT_INTEGRATION_PLAN.md)

**External Resources**:
- Trading Intel v2 Agents: `/home/primemeridianlabs/Development/Projects/trading_intel_v2/.claude/agents/`
- Web Exhaust Agents: `/home/primemeridianlabs/Development/Projects/web_exhaust_alpha/.claude/agents/`

---

**Version**: 1.0
**Last Updated**: 2025-10-26
**Maintained By**: Portfolio Validation Engine Team
