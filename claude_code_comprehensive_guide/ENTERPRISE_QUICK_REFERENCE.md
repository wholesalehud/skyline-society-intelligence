# Enterprise Scaling & Governance - Quick Reference

**Fast lookup guide for enterprise Claude Code deployment, team management, and compliance**

---

## Configuration Precedence

```bash
# Highest to Lowest Priority
1. Enterprise Managed Policies     # /etc/claude-code/managed-settings.json
2. Command Line Arguments           # --flag value
3. Local Project Settings           # .claude/settings.local.json
4. Shared Project Settings          # .claude/settings.json (version controlled)
5. User Settings                    # ~/.claude/settings.json
```

---

## Enterprise Policy Paths

| Platform | Path |
|----------|------|
| Linux/WSL | `/etc/claude-code/managed-settings.json` |
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.json` |
| Windows | `C:\ProgramData\ClaudeCode\managed-settings.json` |

---

## Organization Roles

| Role | Capabilities |
|------|--------------|
| User | Workbench access only |
| Claude Code User | Workbench + Claude Code |
| Developer | Workbench + API key management |
| Billing | Workbench + billing oversight |
| Admin | All capabilities + user management + policies |

---

## Workspace Roles

- `workspace_admin` - Full workspace control
- `workspace_developer` - Development access + API keys
- `workspace_user` - Read/execute access only

---

## SSO Integration

### Supported Protocols
- SAML 2.0
- OpenID Connect (OIDC)

### Supported IdPs
- Okta
- Azure AD / Microsoft Entra ID
- Ping Identity
- Auth0
- Google Workspace
- OneLogin
- Any SAML 2.0 / OIDC compliant IdP

### Configuration
```yaml
Entity ID: https://claude.ai/saml/metadata
ACS URL: https://claude.ai/saml/acs
SLO URL: https://claude.ai/saml/slo
```

---

## Hook Types

| Hook | Purpose | When Executed |
|------|---------|---------------|
| PreToolUse | Validation, approval | Before any tool call |
| PostToolUse | Audit, quality check | After tool execution |
| SessionStart | Environment setup | Session initialization |
| SessionEnd | Cleanup, reporting | Session termination |
| PreCommit | Linting, security scan | Before git commits |
| PostCommit | Notifications, triggers | After git commits |
| PreTask | Planning, allocation | Before task execution |
| PostTask | Verification, docs | After task completion |
| Notification | Alerts, monitoring | On specific events |

### Hook Exit Codes
```bash
0 = Allow/Approve operation
1 = Error (stop execution, show to user)
2 = Block (stop execution, show stderr to Claude)
```

---

## MCP Server Controls

### Configuration (October 2025 Update)
```json
{
  "useEnterpriseMcpConfigOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "company-internal" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ]
}
```

### Precedence Rules
1. Denylist takes absolute precedence
2. Allowlist permits explicitly listed servers
3. `useEnterpriseMcpConfigOnly: true` blocks all non-managed servers
4. Enterprise config cannot be overridden

---

## Admin API Endpoints

### Organization Management
```bash
GET    /v1/organizations/{org_id}                # Get org info
GET    /v1/organizations/{org_id}/members        # List members
PATCH  /v1/organizations/{org_id}/members/{id}   # Update member
DELETE /v1/organizations/{org_id}/members/{id}   # Remove member
POST   /v1/organizations/{org_id}/invites        # Create invite
```

### Workspace Management
```bash
GET    /v1/organizations/{org_id}/workspaces              # List workspaces
POST   /v1/organizations/{org_id}/workspaces              # Create workspace
POST   /v1/organizations/{org_id}/workspaces/{id}/archive # Archive workspace
```

### Usage & Cost
```bash
GET /v1/organizations/{org_id}/usage      # Usage report (by workspace/user/model)
GET /v1/organizations/{org_id}/cost       # Cost breakdown
GET /v1/organizations/{org_id}/claude-code-usage  # Developer productivity metrics
```

### API Keys
```bash
GET   /v1/organizations/{org_id}/api_keys         # List all keys
GET   /v1/organizations/{org_id}/api_keys/{id}    # Get key details
PATCH /v1/organizations/{org_id}/api_keys/{id}    # Update/rotate key
```

---

## Audit Log Event Types

- `user_login` / `user_logout` / `sso_auth`
- `session_start` / `session_end`
- `tool_execution` (read, edit, bash, etc.)
- `file_access` / `file_modification`
- `api_key_created` / `api_key_rotated` / `api_key_revoked`
- `permission_change` / `role_assignment`
- `policy_violation` / `security_alert`
- `mcp_server_connection` / `mcp_server_call`

**Retention:** 30 days (Enterprise plan)
**Export:** JSON, CSV, or SIEM push

---

## Memory Hierarchy

| Level | Path | Purpose | Shared? |
|-------|------|---------|---------|
| Global User | `~/.claude/CLAUDE.md` | Personal preferences across all projects | No |
| Shared Project | `.claude/CLAUDE.md` | Team standards, version controlled | Yes |
| Local Project | `.claude/CLAUDE.local.md` | Personal workspace notes, gitignored | No |

**Best Practices:**
- Keep core memory files under 500 lines
- Use imports for detailed specs
- Remove obsolete information regularly
- Update memory files before major changes (checkpoint pattern)

---

## Model Selection & Cost

| Model | Cost (per 1K input tokens) | Use Case |
|-------|---------------------------|----------|
| Opus 4 | $0.015 | Orchestration, complex analysis |
| Sonnet 4 | $0.003 | Specialized tasks, balanced |
| Haiku 4 | $0.00025 | Simple operations, high volume |

**Cost Optimization:**
- Reserve Opus for orchestration only
- Use Sonnet for specialized tasks (60% cheaper)
- Use Haiku for simple operations (90% cheaper)
- Typical savings: 40-60% with tiered approach

---

## Scaling Patterns

### Hierarchical Three-Tier
```
Strategic Orchestrator (Opus 4)
├─ Research Coordinator (Sonnet 4)
├─ Analysis Coordinator (Sonnet 4)
└─ Implementation Coordinator (Sonnet 4)
    ├─ Data Fetcher (Haiku)
    ├─ Code Analyzer (Sonnet 4)
    └─ Test Runner (Haiku)
```

### Production Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Sequential Pipeline | Analyst → Architect → Implementer → Tester → Auditor | Deterministic workflows |
| Parallel Specialization | UI + API + DB → Integrator → QA | Independent subtasks |
| Research Swarm | Researchers A/B/C → Analyst → Reporter | Multi-source gathering |
| Review Pipeline | Generator → Reviewer → Refiner → Validator → Approver | Quality-critical work |

---

## Compliance Standards

### SOX (Sarbanes-Oxley)
- Audit trails for all financial data access
- Segregation of duties enforcement
- Change management controls
- 7-year data retention

### FINRA
- Electronic communications archival (6 years)
- Trading surveillance
- Supervision and review
- Cybersecurity controls

### GDPR
- Data minimization
- Right to erasure
- Data portability
- Consent management
- Data protection by design

---

## Financial Services Use Cases

| Use Case | Sub-Agents | Key Features |
|----------|-----------|--------------|
| Due Diligence | Financial Analyst, Market Researcher, Sentiment Analyzer, Risk Assessor | Multi-source research, audit trails |
| Portfolio Validation | Alpha Calculator, Risk Assessor, Technical Analyzer, Sentiment Analyzer | Parallel validation, decision records |
| Financial Modeling | Model Builder, Data Validator, Simulator | Monte Carlo simulations, full audit |
| Trading System Modernization | Code Analyzer, Architect, Implementer, Tester, Security Auditor | Legacy migration, compliance |

---

## Key Metrics to Monitor

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Session Success Rate | > 95% | < 90% |
| Average Session Duration | 15-30 min | > 60 min |
| Tool Call Success Rate | > 98% | < 95% |
| API Response Time (p95) | < 500ms | > 2000ms |
| Cost per Session | $0.50-$2.00 | > $5.00 |
| Security Violations | 0 | > 0 |
| Hook Execution Time | < 5s | > 30s |

---

## Enterprise Policy Template

```json
{
  "useEnterpriseMcpConfigOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "company-internal" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ],
  "disableBypassPermissionsMode": true,
  "permissions": {
    "bash": "restricted",
    "read": "allowlist",
    "edit": "ask",
    "webFetch": "deny"
  },
  "excludedPaths": [
    "**/secrets/**",
    "**/.env*",
    "**/credentials/**"
  ],
  "auditMode": "comprehensive",
  "sessionRecording": true,
  "memory": {
    "enabled": true,
    "requireMemoryReview": true,
    "memoryRetentionDays": 90
  },
  "compliance": {
    "dataRetentionDays": 2555,
    "immutableLogs": true,
    "realTimeMonitoring": true
  }
}
```

---

## Common CLI Commands

```bash
# Check organization info
curl -H "Authorization: Bearer $ADMIN_API_KEY" \
  https://api.claude.com/v1/organizations/me

# List members
curl -H "Authorization: Bearer $ADMIN_API_KEY" \
  https://api.claude.com/v1/organizations/{org_id}/members

# Get usage report (last 30 days)
curl -H "Authorization: Bearer $ADMIN_API_KEY" \
  "https://api.claude.com/v1/organizations/{org_id}/usage?start_date=2025-10-01&end_date=2025-10-31"

# Export audit logs
curl -H "Authorization: Bearer $ADMIN_API_KEY" \
  "https://api.claude.com/v1/organizations/{org_id}/audit_logs?start_time=2025-10-26T00:00:00Z" \
  > audit_logs.json

# Headless mode (CI/CD)
claude --headless \
  --project /path/to/repo \
  --prompt "Run all tests and generate coverage report" \
  --output /tmp/results.json
```

---

## Troubleshooting

### SSO Issues
1. Verify IdP metadata XML is correct
2. Check attribute mappings (email, firstName, lastName)
3. Confirm ACS URL in IdP matches Claude configuration
4. Test with single user before rollout

### Policy Not Enforcing
1. Check enterprise policy file exists at correct path
2. Verify JSON syntax is valid
3. Restart Claude Code to reload policies
4. Check configuration precedence (enterprise > user)

### High Costs
1. Review usage by workspace/user via Admin API
2. Check for inefficient model selection (Opus overuse)
3. Implement cost control hooks
4. Set user/org budget limits

### Audit Logs Missing
1. Verify Enterprise plan is active
2. Check audit log retention settings (30-day default)
3. Ensure SIEM integration is configured correctly
4. Test export endpoints

### Hook Not Triggering
1. Check hook script has execute permissions
2. Verify hook is in correct directory (`.claude/hooks/`)
3. Test hook manually with sample input
4. Check for syntax errors in hook script
5. Review hook timeout (60s default)

---

## Security Best Practices

1. **Least Privilege**: Grant minimum necessary roles
2. **MFA Everywhere**: Enforce MFA via SSO
3. **Allowlist First**: Use allowlist for MCP servers, tools, domains
4. **Audit Everything**: Enable comprehensive logging
5. **Rotate Keys**: Quarterly API key rotation
6. **Review Regularly**: Quarterly security audits
7. **Segregate Duties**: Enforce in financial workflows
8. **Monitor Real-Time**: Set alerts for violations
9. **Test Policies**: Verify enforcement before rollout
10. **Document Decisions**: Maintain audit trails

---

## Quick Links

- **Full Enterprise Guide**: [ENTERPRISE_SCALING_GUIDE.md](./ENTERPRISE_SCALING_GUIDE.md)
- **Claude Docs**: https://docs.claude.com/
- **Admin API**: https://docs.claude.com/en/api/administration-api
- **SSO Setup**: https://support.claude.com/en/articles/9797544-setting-up-single-sign-on-sso-on-the-enterprise-plan
- **Hooks Guide**: https://docs.claude.com/en/docs/claude-code/hooks

---

**Last Updated:** 2025-10-26
**Version:** 1.0
