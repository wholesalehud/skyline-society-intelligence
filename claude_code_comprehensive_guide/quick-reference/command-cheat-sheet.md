# Claude Code Command Cheat Sheet

## 🚀 Essential Commands

### CLI Invocation Patterns
```bash
# Interactive modes
claude                                    # Launch REPL
claude "initial prompt"                   # Start with prompt
claude -c                                 # Continue last session
claude -r <session-id> "prompt"          # Resume specific session

# Headless/automation modes
claude -p "task"                          # Non-interactive (print mode)
cat file | claude -p "analyze this"      # Process piped input
claude -p "task" --output-format json    # Structured output

# Configuration
claude --model sonnet                     # Set model
claude --max-turns 5                     # Limit iterations
claude --verbose                         # Debug logging
claude update                            # Update to latest
```

### In-Session Quick Commands
```bash
# Memory shortcuts
#memory This gets stored in CLAUDE.md

# Slash commands
/help                                     # Available commands
/clear                                    # Clear conversation
/model                                    # Change model
/cost                                     # Token usage
/agents                                   # Manage sub-agents
/plugin                                   # Plugin management
/vim                                      # Enable vim mode

# Direct execution
!git status                               # Direct bash
@src/file.js                             # File autocomplete

# Background operations
Ctrl+B                                    # Background current task
/bashes                                   # List running shells
```

## 🔧 Configuration Commands

### Settings Management
```bash
# View current settings
cat ~/.claude/settings.json
cat ./.claude/settings.json

# Common settings patterns
{
  "model": "claude-sonnet-4-5-20250929",
  "permissions": {
    "allow": ["Bash(npm:*)", "Read(~/.zshrc)"],
    "ask": ["Bash(git push:*)"],
    "deny": ["Read(./.env)", "WebFetch"]
  },
  "sandbox": {"enabled": true},
  "outputStyle": "Explanatory"
}
```

### Permission Patterns
```bash
# Tool permissions
"ToolName(pattern:*)"                    # Prefix matching
"Bash(git:*)"                           # Git commands
"Read(src/**/*.py)"                     # Python files only
"Write(./.claude/**)"                   # Project config only
```

## 🤖 Sub-Agent Commands

### Agent Management
```bash
# Interactive management
/agents                                  # View/create/edit/delete

# File-based (create .claude/agents/name.md)
---
name: code-reviewer
description: Expert code review specialist
tools: Read, Grep, Bash
---
Your detailed prompt here...
```

### Agent CLI Configuration
```bash
claude --agents '{
  "reviewer": {
    "description": "Code reviewer",
    "prompt": "You are a senior code reviewer...",
    "tools": ["Read", "Grep"],
    "model": "sonnet"
  }
}'
```

## 🪝 Hook Commands

### Hook Configuration (.claude/settings.json)
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/start.sh",
        "timeout": 60
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash(rm:*)",
      "hooks": [{"type": "command", "command": "./validate.sh"}]
    }]
  }
}
```

### Common Hook Scripts
```bash
#!/bin/bash
# SessionStart hook example
echo 'export NODE_ENV=development' >> "$CLAUDE_ENV_FILE"
git status
npm run lint

# PreToolUse validation
if echo "$1" | grep -q "rm -rf"; then
  echo '{"decision": "deny", "reason": "Dangerous delete"}'
  exit 2
fi
```

## 🔌 Plugin Commands

### Plugin Management
```bash
/plugin                                  # Browse/install interactively
/plugin install name@marketplace         # Install specific
/plugin marketplace add owner/repo       # Add GitHub marketplace
```

### Plugin Structure
```
.claude-plugin/
├── plugin.json                         # Manifest
├── commands/deploy.md                   # Slash commands
├── agents/reviewer.md                   # Sub-agents
├── skills/analyzer/SKILL.md            # Skills
└── hooks/hooks.json                     # Hooks
```

## 💾 Memory & Context Commands

### Memory Tool Usage (API/SDK)
```python
# Memory operations
{"type": "memory_20250818", "name": "memory"}

# Common patterns
view("/memories")                        # List memories
create("/memories/patterns/bug.md", content)
str_replace("/memories/file.md", old, new)
```

### Context Management
```json
{
  "context_management": {
    "edits": [{
      "type": "clear_tool_uses_20250919",
      "trigger": {"type": "input_tokens", "value": 5000},
      "keep": {"type": "tool_uses", "value": 1}
    }]
  }
}
```

## 🎯 Agent Skills Commands

### Skill Creation
```markdown
# SKILL.md format
---
name: financial-analyzer
description: Analyzes financial data and generates reports
---

# Financial Analyzer Skill
When to use: Process quarterly results...
Instructions:
1. Load data from CSV/JSON
2. Calculate metrics...
```

### Skill Directory Structure
```
skill-name/
├── SKILL.md                            # Core instructions
├── reference.md                        # Additional docs
└── scripts/process.py                  # Executable helpers
```

## 🔗 GitHub Actions Integration

### Workflow Configuration
```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]

jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          claude_args: '--max-turns 5'
```

### Comment Triggers
```
@claude review this PR for security
@claude implement feature from issue
@claude fix the TypeError in dashboard
@claude /review
```

## 🐍 Agent SDK Commands

### Basic SDK Usage
```python
from claude_agent_sdk import query, ClaudeSDKClient, ClaudeAgentOptions

# One-shot
async for message in query("prompt"):
    handle(message)

# Stateful conversation
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"]
)

async with ClaudeSDKClient(options) as client:
    await client.query("prompt")
    async for msg in client.receive_response():
        process(msg)
```

### Custom Tool Definition
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("calculator", "Arithmetic operations", {"op": str, "a": int, "b": int})
async def calc(args):
    result = eval(f"{args['a']} {args['op']} {args['b']}")
    return {"content": [{"type": "text", "text": str(result)}]}

server = create_sdk_mcp_server("math", [calc])
```

## 📊 Performance & Monitoring

### Token Usage Tracking
```bash
# JSON output includes usage
claude -p "task" --output-format json | jq '.total_cost_usd'

# Context budget monitoring (Claude 4.5)
# Automatic notifications: "Token usage: 35000/200000; 165000 remaining"
```

### Cost Optimization
```bash
# Batch processing (50% cost reduction)
curl -X POST https://api.anthropic.com/v1/messages/batch

# Extended thinking (start minimal)
{
  "thinking": {"type": "enabled", "budget_tokens": 1024},
  "max_tokens": 4096
}
```

## 🛠️ Troubleshooting Commands

### Common Diagnostics
```bash
# Check installation
claude --version
which claude

# Debug mode
claude --verbose -p "test task"

# Check settings hierarchy
ls ~/.claude/
ls ./.claude/
echo $ANTHROPIC_API_KEY

# Session management
claude -c --output-format json | jq '.session_id'
```

### Error Resolution
```bash
# Permission denied
chmod +x .claude/hooks/script.sh

# Context exceeded
claude -p "task" --max-turns 3

# Tool access issues
cat .claude/settings.json | jq '.permissions'
```

## 🔍 Quick Reference Links

- **Feature Matrix**: [Complete capabilities overview](./feature-matrix.md)
- **Tool Selection**: [When to use what tool](./tool-selection-guide.md)
- **Troubleshooting**: [Common issues & solutions](./troubleshooting-index.md)
- **Best Practices**: [Proven patterns](../reference/best-practices/README.md)