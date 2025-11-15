# Troubleshooting Index

## 🚨 Quick Problem Resolution

### Most Common Issues

| Problem | Symptoms | Quick Fix | Detailed Guide |
|---------|----------|-----------|----------------|
| **API Key Issues** | Authentication errors | Check `$ANTHROPIC_API_KEY` | [API Setup](../implementation-guides/claude-code-features/basic-usage.md#api-setup) |
| **Permission Denied** | Tool access blocked | Review `.claude/settings.json` | [Permissions](../implementation-guides/claude-code-features/settings.md#permissions) |
| **Context Overflow** | Token limit exceeded | Enable context compaction | [Context Management](../implementation-guides/context-management/README.md) |
| **Sub-Agent Fails** | Agent won't load | Check `.claude/agents/` syntax | [Sub-Agents](../implementation-guides/claude-code-features/sub-agents.md) |
| **Hook Errors** | Scripts not executing | Verify permissions & paths | [Hooks](../implementation-guides/claude-code-features/hooks.md) |
| **Plugin Issues** | Commands not found | Check plugin installation | [Plugins](../implementation-guides/claude-code-features/plugins.md) |

## 🔍 Diagnostic Commands

### Health Check Sequence
```bash
# 1. Check installation
claude --version
which claude

# 2. Verify API access
claude -p "test" --output-format json

# 3. Check configuration
cat ~/.claude/settings.json
cat ./.claude/settings.json

# 4. Test permissions
claude -p "read a simple file" --verbose

# 5. Verify sub-agents
ls ./.claude/agents/
/agents

# 6. Check plugin status
/plugin
```

### Debug Mode Analysis
```bash
# Enable detailed logging
claude --verbose -p "problematic task"

# Check session state
claude -c --output-format json | jq '{session_id, turns, cost}'

# Verify tool access
claude -p "list available tools" --verbose
```

## 🔧 Installation & Setup Issues

### Claude Code Not Found
```bash
# Check installation
which claude
echo $PATH

# Reinstall if needed
curl -fsSL https://claude.com/install.sh | sh
# or
brew install claude

# Add to PATH if needed
echo 'export PATH="$HOME/.claude/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### API Authentication
```bash
# Set API key
export ANTHROPIC_API_KEY="your-api-key"

# Persist in shell profile
echo 'export ANTHROPIC_API_KEY="your-key"' >> ~/.bashrc

# Verify access
claude -p "hello" --output-format json | jq '.result'
```

### Permission Setup
```json
// ~/.claude/settings.json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(./.claude/**)",
      "Bash(git:*)",
      "Bash(npm:*)"
    ],
    "ask": [
      "Write(**/*.py)",
      "Bash(rm:*)"
    ],
    "deny": [
      "Read(./.env)",
      "Read(**/*secret*)",
      "WebFetch"
    ]
  }
}
```

## 🤖 Sub-Agent Issues

### Agent Won't Load
```bash
# Check syntax
cat .claude/agents/agent-name.md

# Verify frontmatter
---
name: my-agent
description: Clear description here
tools: Read, Write, Bash
---
```

### Agent Not Auto-Deploying
```yaml
# Improve description for better matching
---
name: code-reviewer
description: Expert code review specialist. Use proactively after code changes for quality, security, and maintainability analysis.
---
```

### Agent Context Issues
```bash
# Agents start fresh - may need context gathering
# Add context loading to agent prompt:

You are a code reviewer. ALWAYS start by:
1. Reading the files you need to review
2. Understanding the project structure
3. Then providing your analysis
```

## 🪝 Hook Problems

### Script Not Executing
```bash
# Check permissions
chmod +x .claude/hooks/script.sh

# Verify path
ls -la .claude/hooks/

# Test script directly
./.claude/hooks/script.sh

# Check hook configuration
jq '.hooks' .claude/settings.json
```

### Hook Blocking Operations
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash(rm:*)",
      "hooks": [{
        "type": "command",
        "command": "./validate-delete.sh",
        "timeout": 30
      }]
    }]
  }
}
```

### Environment Variables
```bash
#!/bin/bash
# Hook script template
set -e

# Available variables:
# $CLAUDE_PROJECT_DIR
# $CLAUDE_ENV_FILE (SessionStart only)

echo "Hook executing in: $CLAUDE_PROJECT_DIR"
```

## 🔌 Plugin & Marketplace Issues

### Plugin Not Found
```bash
# List installed plugins
/plugin

# Check marketplace
/plugin marketplace list

# Add marketplace
/plugin marketplace add owner/repo

# Install plugin
/plugin install plugin-name@marketplace
```

### Plugin Commands Missing
```bash
# Check plugin structure
ls .claude-plugin/
cat .claude-plugin/plugin.json

# Verify enabled status
jq '.enabledPlugins' .claude/settings.json

# Reload plugins
claude # restart session
```

### Plugin Conflicts
```json
// Settings.json - disable conflicting plugins
{
  "enabledPlugins": {
    "plugin-a@marketplace": true,
    "conflicting-plugin@marketplace": false
  }
}
```

## 💾 Memory & Context Issues

### Memory Tool Errors
```python
# Path validation
if not path.startswith("/memories"):
    raise SecurityError("Invalid memory path")

# Common operations
memory.view("/memories")                    # List all
memory.create("/memories/file.md", content) # Create
memory.str_replace("/memories/file.md", old, new) # Edit
```

### Context Window Overflow
```json
// Enable auto-compaction
{
  "context_management": {
    "edits": [{
      "type": "clear_tool_uses_20250919",
      "trigger": {"type": "input_tokens", "value": 5000},
      "keep": {"type": "tool_uses", "value": 2},
      "clear_at_least": {"type": "input_tokens", "value": 100}
    }]
  }
}
```

### Memory Persistence
```bash
# Check memory storage
ls ~/.claude/memory/
ls ./.claude/memory/

# Memory files should persist across sessions
# If missing, check file permissions and storage quotas
```

## 🐍 Agent SDK Issues

### SDK Installation
```bash
# Install latest
pip install claude-agent-sdk

# With uv (preferred)
uv pip install claude-agent-sdk

# Verify installation
python -c "from claude_agent_sdk import query; print('OK')"
```

### Migration from Old SDK
```python
# OLD (claude_code_sdk)
from claude_code_sdk import ClaudeCodeOptions

# NEW (claude_agent_sdk)
from claude_agent_sdk import ClaudeAgentOptions

# Update imports and class names
options = ClaudeAgentOptions(
    system_prompt={"type": "preset", "preset": "claude_code"},
    setting_sources=["project"]  # Now explicit
)
```

### Connection Issues
```python
# Common connection patterns
try:
    async for message in query(prompt, options):
        handle_message(message)
except CLINotFoundError:
    # Claude Code not installed
    fallback_to_api_only()
except ProcessError as e:
    # Execution failure
    log_and_retry(e)
```

## 🔐 Security & Permission Issues

### Tool Access Denied
```json
// Check permission hierarchy (highest to lowest):
// 1. Command-line args
// 2. .claude/settings.local.json (git-ignored)
// 3. .claude/settings.json (project)
// 4. ~/.claude/settings.json (user)

// Debug permission resolution
{
  "permissions": {
    "allow": ["Bash(git status)"],  // Specific allowed
    "ask": ["Bash(git push:*)"],    // Requires confirmation
    "deny": ["Bash(rm:*)"]          // Blocked (overrides allow)
  }
}
```

### Sandbox Issues
```json
{
  "sandbox": {
    "enabled": true,
    "excludedCommands": ["docker", "kubectl"],
    "network": {
      "allowUnixSockets": ["/var/run/docker.sock"],
      "allowLocalBinding": true
    }
  }
}
```

### File Access Problems
```bash
# Check file permissions
ls -la target-file

# Verify path patterns
"Read(src/**/*.py)"     # Python files in src/
"Write(./.claude/**)"   # Claude config only
"Bash(npm:*)"           # NPM commands only
```

## ⚡ Performance Issues

### Slow Response Times
```bash
# Check model selection
claude --model haiku  # Faster model

# Limit iterations
claude --max-turns 3

# Use batch processing for bulk operations
```

### High Token Usage
```bash
# Monitor usage
claude -p "task" --output-format json | jq '.total_cost_usd'

# Enable context compaction
# Use agent skills for repeated operations
# Implement memory tools for persistent data
```

### Memory Leaks
```bash
# Clean up old sessions
claude # check cleanupPeriodDays setting

# Clear conversation
/clear

# Background processes
/bashes  # kill unused shells
```

## 🌐 Network & Integration Issues

### GitHub Actions Failures
```yaml
# Check required permissions
permissions:
  contents: read
  issues: write
  pull-requests: write

# Verify secrets
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

# Common workflow issues
- name: Claude Code
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: '--max-turns 5'  # Prevent runaway
```

### MCP Server Issues
```json
// Check MCP configuration
{
  "enableAllProjectMcpServers": false,
  "enabledMcpjsonServers": ["approved-server"],
  "mcp_servers": [{
    "name": "custom-server",
    "command": "python",
    "args": ["-m", "my_mcp_server"]
  }]
}
```

### Web Tool Access
```json
// If WebFetch blocked
{
  "permissions": {
    "allow": ["WebFetch(domain:github.com)"],
    "deny": ["WebFetch"]  // Blocks other domains
  }
}
```

## 🔄 Recovery Procedures

### Reset to Defaults
```bash
# Backup current settings
cp ~/.claude/settings.json ~/.claude/settings.backup

# Reset to minimal config
echo '{}' > ~/.claude/settings.json

# Test basic functionality
claude -p "hello world"
```

### Session Recovery
```bash
# List recent sessions
claude -c --output-format json | jq '.session_id'

# Resume specific session
claude -r "session-id" "continue previous work"

# If session corrupted, start fresh
claude "summarize previous work and continue"
```

### Complete Reinstall
```bash
# Remove installation
rm -rf ~/.claude/

# Reinstall
curl -fsSL https://claude.com/install.sh | sh

# Restore settings from backup
cp settings.backup ~/.claude/settings.json
```

## 📞 Getting Help

### Self-Diagnosis
```bash
# Run comprehensive check
claude --verbose -p "perform system health check"

# Review logs
tail -f ~/.claude/logs/claude.log
```

### Community Resources
- **GitHub Issues**: [claude-code/issues](https://github.com/anthropics/claude-code/issues)
- **Documentation**: [docs.claude.com](https://docs.claude.com/en/docs/claude-code/)
- **Examples**: [claude-cookbooks](https://github.com/anthropics/claude-cookbooks)

### Reporting Issues
Include in bug reports:
- Claude Code version (`claude --version`)
- Operating system & version
- Minimal reproduction steps
- Full error output with `--verbose`
- Relevant configuration files (sanitized)

---

## 🔗 Quick Links

- **Feature Matrix**: [Complete capabilities](./feature-matrix.md)
- **Commands**: [Command reference](./command-cheat-sheet.md)
- **Tool Selection**: [When to use what](./tool-selection-guide.md)
- **Implementation**: [Step-by-step guides](../implementation-guides/README.md)