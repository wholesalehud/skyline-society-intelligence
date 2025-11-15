# Tool Selection Guide

## 🎯 Decision Framework

This guide helps you choose the right Claude Code feature or tool for any specific task. Follow the decision trees and use case patterns for optimal results.

## 🔄 Primary Decision Tree

```
What's your primary goal?

📊 ANALYSIS & RESEARCH
├─ Single conversation → Interactive Mode + Standard Tools
├─ Cross-session learning → Memory Tools + Interactive
├─ Systematic exploration → Sub-Agents (Explore type)
└─ Documentation generation → Agent Skills + Memory

🔧 DEVELOPMENT & CODING
├─ Real-time coding → Interactive Mode + Checkpointing
├─ Code review automation → Sub-Agents + Hooks
├─ Team standardization → Plugins + Slash Commands
└─ CI/CD integration → Headless Mode + GitHub Actions

🤖 PRODUCTION APPLICATIONS
├─ Custom agent systems → Agent SDK + MCP Servers
├─ Business workflow automation → Agent SDK + Memory Tools
├─ Multi-user applications → Agent SDK + Security Controls
└─ High-scale deployment → Agent SDK + Performance Optimization

💰 FINANCIAL ANALYSIS
├─ Market research → Financial Applications + Web Tools
├─ Portfolio analysis → Risk Assessment + Data Integration
├─ Report generation → Agent Skills (Excel/PowerPoint) + Memory
└─ Trading systems → Multi-Agent Architecture + Risk Controls

🏢 ENTERPRISE & TEAMS
├─ Organization standards → Plugin Marketplaces + Security
├─ Knowledge management → Memory Tools + Agent Skills
├─ Compliance & audit → Hooks + Security Guidelines
└─ Training & onboarding → Documentation + Examples
```

## 🛠️ Tool Capability Matrix

### Core Tools Comparison

| Tool | Primary Use | Context Scope | Persistence | Learning | Complexity |
|------|-------------|---------------|-------------|-----------|------------|
| **Interactive Mode** | Development sessions | Single conversation | Session only | None | 🟢 Low |
| **Headless Mode** | Automation/CI/CD | Single operation | None | None | 🟡 Medium |
| **Sub-Agents** | Specialized tasks | Isolated contexts | None | None | 🟡 Medium |
| **Memory Tools** | Cross-session data | Unlimited | File-based | Continuous | 🟡 Medium |
| **Agent Skills** | Reusable capabilities | Progressive disclosure | None | Packaged expertise | 🟡 Medium |
| **Agent SDK** | Custom applications | Full control | Configurable | Programmable | 🔴 High |

### Feature Interaction Matrix

| Feature A | Feature B | Synergy Level | Combined Benefits |
|-----------|-----------|---------------|-------------------|
| **Memory Tools** | **Agent Skills** | ⭐⭐⭐⭐⭐ | Cross-session skill improvement |
| **Sub-Agents** | **Hooks** | ⭐⭐⭐⭐⭐ | Automated specialist deployment |
| **Agent SDK** | **MCP Servers** | ⭐⭐⭐⭐⭐ | Production-ready integrations |
| **Interactive Mode** | **Checkpointing** | ⭐⭐⭐⭐ | Safe experimentation |
| **Plugins** | **Slash Commands** | ⭐⭐⭐⭐ | Team workflow standardization |
| **Headless Mode** | **GitHub Actions** | ⭐⭐⭐⭐ | Complete automation pipeline |

## 📋 Use Case Patterns

### Research & Analysis

#### 🔍 **Exploratory Analysis**
- **Best tools**: Interactive Mode + Sub-Agents (Explore type)
- **Pattern**: Start broad → narrow focus → deep dive
- **Example**: Codebase understanding, market research, technical investigation

```bash
# Start interactive session
claude "Analyze this codebase architecture"

# Deploy explore sub-agent for systematic search
/agents → create explore agent → "Find all API endpoints"

# Use memory to capture insights
#memory Key architecture: microservices with GraphQL gateway
```

#### 📊 **Comparative Analysis**
- **Best tools**: Agent Skills + Memory Tools
- **Pattern**: Define comparison framework → apply systematically → synthesize
- **Example**: Technology evaluation, competitive analysis, performance benchmarking

```python
# Use skills for structured analysis
skill_response = invoke_skill("comparison-analyzer", {
    "targets": ["option_a", "option_b", "option_c"],
    "criteria": ["performance", "cost", "maintainability"]
})

# Store findings in memory
memory.create("/analysis/comparison_results.md", findings)
```

#### 🔬 **Deep Research**
- **Best tools**: Memory Tools + Multiple Sub-Agents + Agent Skills
- **Pattern**: Divide research domains → parallel investigation → synthesis
- **Example**: Due diligence, scientific literature review, technical feasibility

### Development & Coding

#### ⚡ **Rapid Prototyping**
- **Best tools**: Interactive Mode + Checkpointing
- **Pattern**: Experiment freely → checkpoint successes → iterate boldly
- **Example**: Feature development, proof-of-concept, algorithm testing

```bash
# Interactive with safety net
claude "Implement real-time chat feature"
# Work iteratively
Esc Esc  # Revert if needed
```

#### 🏗️ **Production Development**
- **Best tools**: Agent SDK + Sub-Agents + Hooks + Memory
- **Pattern**: Structured development → automated review → persistent learning
- **Example**: Feature implementation, refactoring, system integration

```python
# SDK for production patterns
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"],
    hooks={"PostToolUse": [code_review_hook]},
    sub_agents={"reviewer": review_agent_config}
)
```

#### 🔧 **Code Review & Quality**
- **Best tools**: Sub-Agents + Hooks + GitHub Actions
- **Pattern**: Automated triggers → specialist review → actionable feedback
- **Example**: PR review, security scanning, style enforcement

```yaml
# GitHub Actions integration
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review for security and maintainability"
    claude_args: '--max-turns 3'
```

### Business Applications

#### 💼 **Workflow Automation**
- **Best tools**: Agent SDK + MCP Servers + Hooks
- **Pattern**: Define triggers → process automation → human handoff points
- **Example**: Customer support, data processing, report generation

```python
# Business workflow automation
mcp_servers = [
    slack_mcp_server,
    salesforce_mcp_server,
    email_mcp_server
]

options = ClaudeAgentOptions(
    mcp_servers=mcp_servers,
    hooks={"PreToolUse": [compliance_validator]}
)
```

#### 📈 **Financial Analysis**
- **Best tools**: Financial Applications + Agent Skills + Memory Tools
- **Pattern**: Data integration → analysis → reporting → learning retention
- **Example**: Portfolio analysis, market research, risk assessment

```python
# Financial analysis pipeline
from claude_agent_sdk import ClaudeSDKClient

# Load financial skills and memory
options = ClaudeAgentOptions(
    skills=["financial-analyzer", "risk-assessor", "report-generator"],
    memory_enabled=True,
    system_prompt={"type": "text", "text": "Financial analysis expert..."}
)
```

#### 🏢 **Enterprise Integration**
- **Best tools**: Agent SDK + Security Controls + Plugin Marketplaces
- **Pattern**: Secure deployment → governed access → scalable distribution
- **Example**: Internal tools, knowledge management, compliance systems

## 🚨 Anti-Patterns (What NOT to Use)

### ❌ **Wrong Tool Choices**

| Scenario | Wrong Choice | Why It Fails | Right Choice |
|----------|--------------|--------------|--------------|
| One-off automation | Agent SDK | Overengineered | Headless mode |
| Learning across sessions | Standard tools | No persistence | Memory tools |
| Team standardization | Individual settings | No sharing | Plugins + marketplace |
| Production deployment | Interactive mode | No automation | Agent SDK |
| Complex research | Single agent | Limited capability | Sub-agents + skills |
| Financial calculations | General prompting | Inconsistent | Agent skills |

### ❌ **Feature Misuse**

#### Memory Tools Misuse
```bash
# ❌ Don't store temporary data
memory.create("/temp/session_vars.json", {...})

# ✅ Store learning patterns
memory.create("/patterns/auth_debugging.md", insights)
```

#### Sub-Agent Misuse
```python
# ❌ Don't create agents for every small task
create_agent("simple_formatter")

# ✅ Create for specialized domains
create_agent("security_reviewer", expertise="AppSec, OWASP")
```

#### Hook Misuse
```json
// ❌ Don't block everything
"hooks": {
  "PreToolUse": [{"matcher": "*", "hooks": [blocking_validator]}]
}

// ✅ Target specific risks
"hooks": {
  "PreToolUse": [{"matcher": "Bash(rm:*)", "hooks": [deletion_validator]}]
}
```

## 🎯 Quick Selection Heuristics

### By Task Duration
- **< 30 minutes**: Interactive Mode
- **30min - 2 hours**: Interactive + Sub-Agents
- **2+ hours**: Memory Tools + Skills
- **Multi-day**: Agent SDK + Full stack

### By Team Size
- **Individual**: Interactive + Checkpointing
- **Small team (2-5)**: Plugins + Shared settings
- **Large team (5+)**: Marketplace + Sub-agents
- **Enterprise**: Agent SDK + Security + Governance

### By Complexity
- **Simple tasks**: Standard tools
- **Multi-step workflows**: Sub-agents
- **Domain expertise**: Agent skills
- **Business integration**: Agent SDK

### By Frequency
- **One-time**: Headless mode
- **Occasional**: Interactive + Memory
- **Regular**: Slash commands + Hooks
- **Continuous**: Agent SDK + Automation

## 🔍 Performance Considerations

### Token Efficiency Ranking
1. **Agent Skills** (90% reduction for repeated tasks)
2. **Memory Tools** (offload context externally)
3. **Sub-Agents** (focused context windows)
4. **Standard Tools** (baseline efficiency)

### Latency Considerations
1. **CLI commands** (fastest: <100ms)
2. **Hooks** (fast: <500ms)
3. **Sub-agent creation** (medium: 1-3s)
4. **Skill loading** (medium: 1-2s)
5. **Memory operations** (fast: <200ms)

### Scaling Characteristics
- **Horizontal**: Agent SDK + MCP servers
- **Vertical**: Memory + Context management
- **Team**: Plugins + Marketplaces
- **Domain**: Agent Skills + Sub-agents

## 🔗 Implementation Pathways

### Beginner → Intermediate
1. Master Interactive Mode
2. Add Checkpointing for safety
3. Create first Sub-Agent
4. Implement Memory Tools
5. Build simple Agent Skill

### Intermediate → Advanced
1. Deploy Agent SDK application
2. Design custom MCP server
3. Implement security controls
4. Build plugin marketplace
5. Optimize for production scale

### Team → Enterprise
1. Standardize on plugin system
2. Implement governance hooks
3. Deploy security frameworks
4. Create training documentation
5. Monitor and optimize performance

---

## 🔗 Quick Links

- **Feature Matrix**: [Complete capabilities overview](./feature-matrix.md)
- **Commands**: [Essential command reference](./command-cheat-sheet.md)
- **Implementation**: [Step-by-step guides](../implementation-guides/README.md)
- **Examples**: [Working implementations](../reference/examples/README.md)