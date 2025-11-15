# Video Analysis: Claude Code Skills vs MCP vs Sub-Agents vs Slash Commands
## Application to Portfolio Validation Engine

**Video Source:** Analysis of Claude Code feature comparison video
**Transcript Analysis Date:** 2025-10-28
**Relevance:** Critical for portfolio validation architecture decisions

---

## 🎯 **Core Insight: The Composition Hierarchy**

The video reveals a crucial hierarchy for Claude Code features:

```
┌──────────────────────────────────────┐
│         SKILLS (Top Level)           │  ← Automatic, Repeat Solutions
│  Can compose: MCP + Sub-agents +     │
│               Slash Commands         │
└──────────────┬───────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
┌───▼────────┐    ┌──────▼─────────┐
│ SUB-AGENTS │    │  MCP SERVERS   │  ← External Integrations
│ (Parallel/ │    │ (Data Sources) │
│  Isolated) │    └────────────────┘
└────────────┘
    │
┌───▼──────────────────────────────────┐
│    SLASH COMMANDS (THE PRIMITIVE)    │  ← Foundation of Everything
│  "Everything is a prompt in the end" │
└──────────────────────────────────────┘
```

**Key Quote:** *"The prompt is the fundamental unit of knowledge work. If you don't know how to build and manage prompts, you will lose."*

---

## 🔑 **The Core 4 of Agentic Coding**

Every Claude Code feature is built on these fundamentals:

1. **Context** - What information is available
2. **Model** - Which LLM is processing
3. **Prompt** - The instructions (THE PRIMITIVE)
4. **Tools** - Available capabilities (MCP, skills, etc.)

**Critical Understanding:** All features = Context + Model + Prompt + Tools in different configurations.

---

## 📊 **Feature Comparison Matrix (From Video)**

| Capability | Skills | MCP | Sub-Agents | Slash Commands |
|-----------|--------|-----|------------|----------------|
| **Agent Triggered** | ✅ Auto | ❌ Manual | ✅ Auto | ❌ Manual |
| **Context Efficient** | ✅ Progressive | ❌ Explodes | ✅ Isolated | ✅ Efficient |
| **Context Persistence** | ✅ Keeps | ✅ Keeps | ❌ Loses | ✅ Keeps |
| **Modularity** | ✅ High | ✅ High | ⚠️ Manual | ⚠️ Manual |
| **Composability** | ✅ All | ⚠️ Limited | ❌ No Sub-Agents | ✅ All |
| **Specialization** | ✅ | ✅ | ✅ | ✅ |
| **Shareability** | ✅ | ✅ | ✅ | ✅ |
| **Parallel Execution** | ❌ | ❌ | ✅ ONLY | ❌ |

**Winner for Parallelization:** Sub-agents (ONLY option)
**Winner for Modularity:** Skills + MCP
**Winner for Simplicity:** Slash Commands (the primitive)

---

## 🎯 **Decision Framework: When to Use What**

### **Use SKILLS When:**
- ✅ Automatic behavior needed
- ✅ Repeat solution (not one-off)
- ✅ Managing multiple related operations
- ✅ Domain-specific expertise to encode
- ✅ Composing multiple slash commands/MCP/sub-agents

**Example from video:** Git work tree manager (create, list, remove, manage)

### **Use MCP Servers When:**
- ✅ External integrations (APIs, databases)
- ✅ Third-party services (Schwab, Webull, market data)
- ✅ Bundling multiple external capabilities

**Example from video:** Jira connection, database queries, weather APIs

### **Use Sub-Agents When:**
- ✅ Parallel processing needed
- ✅ Context isolation required
- ✅ Scalable independent tasks
- ✅ OK with losing context afterward

**Example from video:** Fix failing tests at scale, security audits

### **Use Slash Commands When:**
- ✅ One-off manual trigger
- ✅ Simple single-step task
- ✅ Starting point (the primitive)
- ✅ Need full control over execution

**Example from video:** Generate commit message, create UI component

---

## ⚠️ **Critical Video Warnings**

### **Mistake #1: Converting All Slash Commands to Skills**

**Quote:** *"There are a lot of engineers right now that are going all in on skills. They're converting all their slash commands to skills. I think that's a huge mistake."*

**Why It's Wrong:**
- Slash commands are the PRIMITIVE
- Skills should COMPOSE slash commands, not replace them
- You lose the simplicity and manual control
- Over-engineering simple one-off tasks

**Correct Approach:**
```
✅ Slash Command (primitive)
    ↓ (when repeat problem emerges)
✅ Skill (composes multiple slash commands)

❌ DON'T: Convert single slash command → skill (unnecessary)
```

### **Mistake #2: Using Skills for One-Off Tasks**

**Quote:** *"If you can do the job with a sub agent or custom slash command and it's a one-off job, do not use a skill. This is not what skills are for."*

**Example from video:**
- Creating ONE git work tree → Slash Command ✅
- Managing MANY git work trees → Skill ✅

### **Mistake #3: Forgetting the Prompt is King**

**Quote:** *"Do not give away the prompt. The prompt is the fundamental unit of knowledge work and of programming."*

**Danger:** Getting distracted by features (skills, MCP, sub-agents) and forgetting prompts are the foundation.

---

## 💡 **Application to Portfolio Validation Engine**

Based on the video's framework, here's the optimal architecture:

### **Current Overcomplicated System (WRONG):**

```python
# Your 800-line orchestrator
class HybridM5Orchestrator:
    async def execute_m5_validation(...):
        # Manual coordination
        for gate in validation_gates:
            await asyncio.sleep(0.075)  # Simulated!
            result = hardcoded_response()
```

**Problem:** You built infrastructure (K8s, Kafka) when you needed PROMPTS.

---

### **Correct Approach (Video Framework):**

#### **Step 1: Start with Slash Command (The Primitive)**

```bash
# .claude/commands/validate-portfolio.md
---
description: Validate a single portfolio with full analysis
---

Validate portfolio for account {{account_id}}:

1. Fetch positions from Schwab/Webull
2. Validate market data quality (M1 gate)
3. Calculate portfolio alpha vs SPY (M5 gate)
4. Assess concentration risk (M3 gate)
5. Generate trade recommendations

Provide detailed findings with confidence scores.
```

**Use Case:** Validating ONE portfolio manually

---

#### **Step 2: Add MCP Servers (External Integrations)**

```python
# mcp_servers/market_data/server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MarketDataServer")

@mcp.tool()
async def fetch_schwab_positions(account_id: str) -> dict:
    """External integration with Schwab API"""
    # SnapTrade integration
    pass

@mcp.tool()
async def validate_market_data(symbols: list[str]) -> dict:
    """M1 validation gate"""
    # Real validation logic (not asyncio.sleep!)
    pass
```

**Use Case:** Connecting to external data sources (Schwab, Webull, yfinance)

---

#### **Step 3: Add Sub-Agents (Parallel Validation)**

```python
# When validating MULTIPLE portfolios in parallel
async def validate_portfolios_parallel(account_ids: list[str]):
    """Use sub-agents for parallel portfolio validation"""

    # Launch sub-agents for each portfolio
    sub_agents = [
        launch_sub_agent(f"Validate portfolio {account_id}")
        for account_id in account_ids
    ]

    # All run in parallel, isolated contexts
    results = await asyncio.gather(*sub_agents)
    return results
```

**Use Case:** Validating 10+ portfolios simultaneously

---

#### **Step 4: Graduate to Skill (Repeat Management)**

```
.claude/skills/portfolio-validator/
├── skill.md                      # Main instructions
├── instructions/
│   ├── validation-workflow.md    # How to validate
│   └── risk-assessment.md        # Risk calculation logic
├── prompts/
│   ├── validate-single.md        # Slash command (primitive!)
│   ├── generate-report.md        # Report generation
│   └── calculate-alpha.md        # Alpha calculation
└── resources/
    ├── validation-rules.json     # Business rules
    └── risk-thresholds.yaml      # Risk limits
```

**skill.md:**
```markdown
---
name: portfolio-validator
description: Comprehensive portfolio validation and management
---

# Portfolio Validator Skill

This skill manages the complete portfolio validation lifecycle.

## Instructions

Use the following slash commands (THE PRIMITIVES):
- `/validate-single` - Validate one portfolio
- `/calculate-alpha` - Calculate alpha vs benchmark
- `/generate-report` - Create trade ticket

Use MCP servers:
- market-data-server (external data)
- broker-server (Schwab/Webull integration)

For parallel validation, use sub-agents.

## Workflow

1. Detect if single or multiple portfolios
2. If single: Use `/validate-single` slash command
3. If multiple: Launch sub-agents for parallel processing
4. Aggregate results
5. Generate final report with `/generate-report`
```

**Use Case:** Managing portfolio validation as a REPEAT operation (daily, weekly)

---

## 🎯 **Revised Architecture for Your Portfolio Validation**

### **Composition Strategy (From Video Framework):**

```
┌────────────────────────────────────────────────┐
│  PORTFOLIO VALIDATOR SKILL (Top Level)         │
│  - Automatic invocation                        │
│  - Manages repeat validation workflows         │
│  - Composes everything below                   │
└──────────────────┬─────────────────────────────┘
                   │
    ┌──────────────┼─────────────┐
    │              │             │
┌───▼─────┐   ┌───▼──────┐  ┌──▼──────────────┐
│ /validate│   │market-data│  │Sub-Agents       │
│ /alpha   │   │broker     │  │(parallel        │
│ /report  │   │forecast   │  │ validation)     │
│          │   │           │  │                 │
│PRIMITIVES│   │MCP SERVERS│  │PARALLEL         │
└──────────┘   └───────────┘  └─────────────────┘
```

**Key Insight from Video:** Skills should COMPOSE slash commands (primitives), not replace them!

---

## 📋 **Implementation Roadmap (Video-Aligned)**

### **Phase 1: Build Primitives (Week 1)**

**Create Slash Commands (Foundation):**
```bash
.claude/commands/
├── validate-portfolio.md      # Single portfolio validation
├── calculate-alpha.md         # Alpha calculation primitive
├── assess-risk.md             # Risk assessment primitive
├── generate-trade-ticket.md   # Trade recommendation primitive
└── fetch-positions.md         # Position retrieval primitive
```

**Why Start Here:** *"Everything is a prompt in the end. It's tokens in, tokens out."*

---

### **Phase 2: Add MCP Servers (Week 2)**

**External Integrations:**
```python
mcp_servers/
├── market_data/      # yfinance, Alpha Vantage, FinnHub
├── broker/           # SnapTrade (Schwab + Webull)
└── forecast/         # Neural forecasting (optional)
```

**Why MCP:** External integrations (Schwab, Webull, market data APIs)

---

### **Phase 3: Add Sub-Agents (Week 3, if needed)**

**Only if:**
- ✅ Need to validate 10+ portfolios in parallel
- ✅ OK with losing context (results saved elsewhere)
- ✅ Want isolated execution environments

**If not needed:** Skip this! Keep it simple.

---

### **Phase 4: Graduate to Skill (Week 4, when repeat problem emerges)**

**Create Portfolio Validator Skill:**
```
.claude/skills/portfolio-validator/
├── skill.md                    # Orchestration logic
├── prompts/                    # Your slash commands (primitives!)
│   ├── validate-portfolio.md
│   ├── calculate-alpha.md
│   └── generate-report.md
└── resources/
    └── validation-rules.json
```

**Key Point:** Skill COMPOSES your slash commands, doesn't replace them!

---

## ⚠️ **What NOT to Do (Video Lessons)**

### **❌ WRONG: Your Current Approach**

```python
# 800 lines of custom orchestration
class HybridM5Orchestrator:
    validation_gates = [...]

    async def execute_m5_validation(...):
        for gate in self.validation_gates:
            await self.skill_interface.call_skill(...)  # SIMULATED!
```

**Problems:**
1. Built infrastructure before primitives (backwards!)
2. Simulated agent responses (`asyncio.sleep()`)
3. 800 lines when slash command would do
4. No composition strategy

---

### **❌ WRONG: Converting Everything to Skills**

**Quote from video:** *"I think that's a huge mistake."*

Don't do this:
```bash
# Converting every slash command to a skill (WRONG)
.claude/skills/
├── validate-one-portfolio/     # ❌ Overkill for one-off
├── calculate-alpha-once/       # ❌ Should be slash command
└── generate-single-report/     # ❌ Unnecessary complexity
```

---

### **✅ CORRECT: Compositional Approach**

```bash
# Start with slash commands (primitives)
.claude/commands/
├── validate-portfolio.md       # ✅ Use this first!
├── calculate-alpha.md
└── generate-report.md

# Graduate to skill when managing multiple operations
.claude/skills/portfolio-manager/
├── skill.md                    # Composes commands above
└── prompts/                    # Includes slash commands
    ├── validate-portfolio.md   # Same primitive!
    └── ...
```

**Key:** Skills COMPOSE primitives, don't replace them.

---

## 🎯 **Video Quote Highlights**

### **On Prompts as Primitives:**

> *"Everything is a prompt in the end. It's tokens in, tokens out. If you master the fundamentals, you'll master the compositional units, you'll master the features, and then you'll master the tools."*

### **On Starting Simple:**

> *"When you're starting out, I always recommend you just build a prompt. Don't build a skill. Don't build a sub agent. Don't build out an MCP server. Keep it simple."*

### **On Skills vs Slash Commands:**

> *"If you can do the job with a sub agent or custom slash command and it's a one-off job, do not use a skill. This is not what skills are for."*

### **On Composition:**

> *"Skills can use prompts. Skills can use other skills. Skills can use MCP servers and of course skills can use sub agents."*

### **On the Core 4:**

> *"If you understand these [Context, Model, Prompt, Tools], if you can build and manage these, you will win. Every agent is the core 4."*

---

## 📊 **Skill Rating (From Video)**

**Overall: 8/10**

### **Pros:**
✅ Agent-invoked (autonomous)
✅ Context protection (progressive disclosure)
✅ Dedicated file system pattern (modularity)
✅ Can compose other features
✅ Agentic approach (agent decides)

### **Cons:**
❌ Doesn't go all the way (can't nest prompts/sub-agents in dedicated dirs)
❌ Reliability concerns when chaining multiple skills
❌ Not much actual innovation (opinionated file structure + prompt engineering)
❌ Could do everything with prompts + slash commands + MCP already

**Verdict:** Useful, but don't over-use. Start with slash commands, graduate to skills when repeat problem emerges.

---

## 🎯 **Final Recommendation for Portfolio Validation**

Based on video analysis:

### **Don't Build:**
❌ Kubernetes infrastructure
❌ Kafka message brokers
❌ Custom 800-line orchestrator
❌ Simulated agent skills
❌ Skills for one-off validations

### **Do Build:**

**Phase 1: Slash Commands (Primitives)**
```bash
/validate-portfolio {account_id}
/calculate-alpha {portfolio} {benchmark}
/assess-risk {holdings}
/generate-report {validation_results}
```

**Phase 2: MCP Servers (External Integrations)**
```python
- market-data-mcp (yfinance, Alpha Vantage)
- broker-mcp (SnapTrade → Schwab + Webull)
- forecast-mcp (neural NHITS, optional)
```

**Phase 3: Sub-Agents (If Parallel Needed)**
```python
# Only if validating 10+ portfolios simultaneously
parallel_validate_portfolios(account_ids)
```

**Phase 4: Skill (When Repeat Management Emerges)**
```bash
.claude/skills/portfolio-manager/
└── Composes: slash commands + MCP + sub-agents
```

---

## 🔑 **Key Takeaway**

**Quote:** *"The prompt is the fundamental unit of knowledge work. There are no exceptions to this. If you understand this, you will win."*

**For Your Portfolio Validation Engine:**
1. **Start with slash commands** (your validation primitives)
2. **Add MCP servers** (Schwab/Webull/market data)
3. **Use sub-agents only if parallel** (validating many portfolios at once)
4. **Graduate to skill** when you're managing portfolio validation as a repeat workflow

**Stop building infrastructure. Start writing prompts.**

---

**Video Analysis Date:** 2025-10-28
**Transcript Length:** ~8,000 words
**Key Insights Extracted:** 15+
**Application:** Portfolio Validation Architecture
**Status:** Integrated into comprehensive recommendation
