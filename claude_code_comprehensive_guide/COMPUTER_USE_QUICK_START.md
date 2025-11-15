# Computer Use Quick Start Guide

## 5-Minute Setup

### Prerequisites
```bash
# Install Docker
sudo apt-get update
sudo apt-get install docker.io

# Clone reference implementation
git clone https://github.com/anthropics/anthropic-quickstarts
cd anthropic-quickstarts/computer-use-demo

# Set API key
export ANTHROPIC_API_KEY='your-api-key'
```

### Launch Demo
```bash
# Build and run
./setup.sh
docker build . -t computer-use-demo:local
docker run -p 8501:8501 -p 5900:5900 -p 6080:6080 \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  computer-use-demo:local
```

### Access Interfaces
- **Streamlit UI**: http://localhost:8501
- **VNC Desktop**: http://localhost:6080/vnc.html
- **Combined View**: http://localhost:8080

---

## Essential Commands

### Basic Computer Use Actions

```python
# Take screenshot
{
  "action": "screenshot"
}

# Click at coordinates
{
  "action": "left_click",
  "coordinate": [640, 400]
}

# Type text
{
  "action": "type",
  "text": "Hello, World!"
}

# Press key
{
  "action": "key",
  "text": "Return"
}

# Scroll
{
  "action": "scroll",
  "direction": "down",
  "amount": 5
}
```

---

## Common Patterns

### Pattern 1: Navigate and Extract Data

```python
prompt = """
1. Take screenshot to see current state
2. Open Firefox browser
3. Navigate to example.com
4. Wait 2 seconds for page load
5. Click login button at top right
6. Type username: "testuser"
7. Press Tab to move to password field
8. Type password: "testpass"
9. Press Enter to submit
10. Wait 3 seconds for page load
11. Take screenshot of logged-in state
12. Navigate to /data page
13. Extract visible data and save to JSON
"""
```

### Pattern 2: Visual Validation

```python
prompt = """
Visual validation workflow:
1. Take screenshot of application
2. Verify these elements are present:
   - Header with logo
   - Navigation menu
   - Main content area
   - Footer
3. Check for any error messages or warnings
4. Document any issues found
5. Return validation report
"""
```

### Pattern 3: Form Automation

```python
prompt = """
Fill out registration form:
1. Screenshot form to verify it's loaded
2. Click first name field
3. Type: "John"
4. Press Tab
5. Type last name: "Doe"
6. Press Tab
7. Type email: "john@example.com"
8. Click Submit button
9. Wait for confirmation
10. Screenshot result
"""
```

---

## Claude Code Integration

### MCP Server Setup

```json
{
  "mcpServers": {
    "computer_use": {
      "command": "python",
      "args": ["-m", "computer_use_mcp_server"],
      "env": {
        "DISPLAY": ":1",
        "DISPLAY_WIDTH": "1280",
        "DISPLAY_HEIGHT": "800"
      }
    }
  }
}
```

### Headless Execution

```bash
# Single task
claude -p "Take screenshot and describe what you see" \
  --output-format json \
  --allowedTools "mcp__computer_use"

# Multi-turn workflow
SESSION_ID=$(claude -p "Navigate to example.com" \
  --output-format json \
  --allowedTools "mcp__computer_use" \
  | jq -r '.session_id')

claude --resume $SESSION_ID \
  --continue "Now click the login button"
```

---

## Portfolio Validation Examples

### Example 1: Collect Broker Positions

```python
prompt = """
Collect positions from Schwab:
1. Navigate to schwab.com
2. Click login
3. Enter credentials from environment
4. Navigate to Positions tab
5. Wait for table to load
6. For each position row:
   - Extract symbol
   - Extract quantity
   - Extract current value
7. Save data to ./data/schwab_positions.json
8. Screenshot final positions view
"""
```

### Example 2: Visual Reconciliation

```python
prompt = """
Reconcile portfolio display with database:
1. Read expected positions from ./data/expected_positions.json
2. Navigate to broker platform
3. Screenshot positions view
4. Compare screenshot data with expected data
5. For each discrepancy:
   - Document symbol
   - Expected vs actual
   - Screenshot with annotation
6. Generate reconciliation report
"""
```

### Example 3: Dashboard Validation

```python
prompt = """
Validate portfolio dashboard:
1. Launch dashboard at localhost:3000
2. Take screenshot of overview
3. Verify all sections present:
   - Portfolio value card
   - Position table
   - Performance chart
   - Risk metrics
4. Click on first position to drill down
5. Verify detail view renders correctly
6. Screenshot and return validation results
"""
```

---

## Error Handling

### Retry Pattern

```python
def execute_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = claude_computer_use(prompt)
            if result['success']:
                return result
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Verification Pattern

```python
prompt = """
Execute action with verification:
1. Take screenshot of initial state
2. Perform action: [specific action]
3. Wait 1 second
4. Take screenshot of result
5. Verify expected change occurred
6. If not successful, try alternative approach
7. Return success status and screenshots
"""
```

---

## Performance Tips

### Optimize Resolution
```python
# Use 1024x768 for best balance
DISPLAY_CONFIG = {
  "display_width_px": 1024,
  "display_height_px": 768
}
```

### Minimize Screenshots
```python
# Bad: Screenshot after every action
# Good: Screenshot only when state changes

prompt = """
1. Click button A
2. Click button B
3. Click button C
4. Now take screenshot to verify all clicks succeeded
"""
```

### Batch Actions
```python
prompt = """
Execute sequence without intermediate screenshots:
1. Type username
2. Tab to password
3. Type password
4. Click submit
5. Now wait and screenshot result
"""
```

---

## Security Checklist

- [ ] Running in isolated container/VM
- [ ] Network restricted to necessary domains only
- [ ] Using test credentials (never production)
- [ ] Audit logging enabled
- [ ] No sensitive data in screenshots
- [ ] Human approval for consequential actions

---

## Troubleshooting

### Issue: Clicks Not Accurate
**Solution**: Reduce resolution to 1024x768 or lower

### Issue: Screenshots Failing
**Solution**: Check virtual display is running
```bash
ps aux | grep Xvfb
export DISPLAY=:1
```

### Issue: High Latency
**Solution**:
- Minimize screenshot frequency
- Use optimal resolution
- Batch related actions

### Issue: Action Failures
**Solution**: Add explicit wait times
```python
{
  "action": "wait",
  "duration": 2000  # 2 seconds
}
```

---

## Cost Estimation

**Typical Workflow** (10 actions):
- System prompt: $0.001
- Tool definition: $0.002
- Screenshots (5x): $0.025-0.075
- Tool results: $0.010
- **Total**: $0.10-0.30 per workflow

**Optimization**:
- Reduce screenshots: 50% cost reduction
- Optimal resolution: 30% cost reduction
- Batch workflows: 40% cost reduction

---

## Next Steps

1. **Test basic capabilities** with demo environment
2. **Design your first workflow** for portfolio validation
3. **Build MCP server integration** for Claude Code
4. **Create reusable skill package** for team
5. **Scale to production** with proper security

---

## Quick Reference Card

| Task | Command Pattern |
|------|----------------|
| **Screenshot** | `{"action": "screenshot"}` |
| **Click** | `{"action": "left_click", "coordinate": [x, y]}` |
| **Type** | `{"action": "type", "text": "..."}` |
| **Key** | `{"action": "key", "text": "Return"}` |
| **Scroll** | `{"action": "scroll", "direction": "down", "amount": 5}` |
| **Wait** | `{"action": "wait", "duration": 1000}` |

### Optimal Settings
- **Resolution**: 1024x768
- **Model**: claude-sonnet-4-5-20250929
- **Beta Flag**: computer-use-2025-01-24
- **Max Actions**: 10-20 per workflow

### Common Shortcuts
- `Alt+Tab` - Switch windows
- `Ctrl+L` - Browser address bar
- `Ctrl+T` - New browser tab
- `Ctrl+W` - Close tab
- `F5` - Refresh page
- `F12` - Developer console

---

**See [COMPUTER_USE_RESEARCH.md](./COMPUTER_USE_RESEARCH.md) for comprehensive documentation**
