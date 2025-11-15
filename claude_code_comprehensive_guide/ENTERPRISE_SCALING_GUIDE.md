# Claude Code Enterprise Scaling & Governance Guide

**Comprehensive Guide to Enterprise Deployment, Team Management, and Compliance for Claude Code**

---

## Table of Contents

1. [Enterprise Architecture Overview](#enterprise-architecture-overview)
2. [Hierarchical Configuration Management](#hierarchical-configuration-management)
3. [Team Management & User Provisioning](#team-management--user-provisioning)
4. [Security Framework](#security-framework)
5. [Governance & Compliance Automation](#governance--compliance-automation)
6. [MCP Server Enterprise Controls](#mcp-server-enterprise-controls)
7. [Scaling Patterns & Multi-Agent Architecture](#scaling-patterns--multi-agent-architecture)
8. [Knowledge Management & Memory Tools](#knowledge-management--memory-tools)
9. [Monitoring, Audit Trails & Observability](#monitoring-audit-trails--observability)
10. [Financial Services Implementation](#financial-services-implementation)
11. [Portfolio Validation Engine Enterprise Deployment](#portfolio-validation-engine-enterprise-deployment)

---

## Enterprise Architecture Overview

### 2025 Enterprise Capabilities

Claude Code's enterprise offerings (launched August 2025) provide centralized management through Team and Enterprise plans with "premium seats" for developer access.

**Key Enterprise Features:**
- **Single Sign-On (SSO)**: SAML 2.0 and OIDC integration with major IdPs (Okta, Azure AD, Ping Identity, Auth0)
- **SCIM Provisioning**: Automated user lifecycle management
- **Role-Based Access Control (RBAC)**: Fine-grained permissions at organization, workspace, and user levels
- **Compliance API**: Real-time programmatic access to usage data and customer content
- **Audit Logging**: SOC 2 Type II aligned logging with 30-day retention and SIEM integration
- **Domain Capture**: Automated workspace enrollment for organizational domains
- **Zero Data Retention (ZDR)**: Enterprise API customers can opt-in to prevent data storage

### Enterprise vs Team Plans

| Feature | Team Plan | Enterprise Plan |
|---------|-----------|-----------------|
| SSO Integration | ❌ | ✅ |
| SCIM Provisioning | ❌ | ✅ |
| Advanced RBAC | Limited | Full |
| Audit Logs | ❌ | ✅ (30 days) |
| Compliance API | ❌ | ✅ |
| Domain Capture | ❌ | ✅ |
| Usage Analytics | Basic | Advanced |
| Policy Management | Basic | Enterprise-managed |
| Cost Controls | Organization-level | Organization + User-level |

**Pricing Model:**
- Base cost per "premium seat" for Claude Code access
- Additional "extra usage" billed at standard API rates
- Flexible but potentially unpredictable costs requiring careful budget management

---

## Hierarchical Configuration Management

### Configuration Precedence

Claude Code implements a 5-tier configuration hierarchy (highest to lowest precedence):

1. **Enterprise Managed Policies** (`managed-settings.json`) - Highest priority, cannot be overridden
2. **Command Line Arguments** - Temporary session overrides
3. **Local Project Settings** (`.claude/settings.local.json`) - Personal preferences, gitignored
4. **Shared Project Settings** (`.claude/settings.json`) - Team standards, version controlled
5. **User Settings** (`~/.claude/settings.json`) - Global personal defaults, lowest priority

This architecture enables: "Enterprise security policies are always enforced while still allowing teams and individuals to customize their experience."

### Enterprise-Managed Policy Deployment

**Platform-Specific Paths:**

```bash
# macOS
/Library/Application Support/ClaudeCode/managed-settings.json

# Linux/WSL
/etc/claude-code/managed-settings.json

# Windows
C:\ProgramData\ClaudeCode\managed-settings.json
```

**Example Enterprise Policy Configuration:**

```json
{
  "useEnterpriseMcpConfigOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "sentry" },
    { "serverName": "company-internal-analytics" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" },
    { "serverName": "*-public" }
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
    "**/credentials/**",
    "**/keys/**"
  ],
  "auditMode": "comprehensive",
  "sessionRecording": true
}
```

### Administrative Controls

**Permission Management:**
- Granular tool access restrictions (Bash, Read, Edit, WebFetch, etc.)
- File/directory exclusion from Claude access
- Custom permission modes and bypass prevention
- Separate `managed-mcp.json` for centralized MCP server configuration

**Configuration Snapshots:**
- Hooks captured at startup to prevent runtime manipulation
- Policy-as-code approach for version-controlled governance
- Immutable enterprise policies enforced at session initialization

---

## Team Management & User Provisioning

### Organizational Structure & Roles

Five organization-level roles govern permissions:

| Role | Capabilities |
|------|--------------|
| **User** | Workbench access only |
| **Claude Code User** | Workbench + Claude Code access |
| **Developer** | Workbench + API key management |
| **Billing** | Workbench + billing oversight |
| **Admin** | All capabilities + user management + policy enforcement |

### Workspace Management

**Workspace Features:**
- Maximum 100 workspaces per organization
- Default Workspace (cannot be edited or removed, no ID)
- Workspace-specific roles: `workspace_admin`, `workspace_developer`, `workspace_user`
- Create, list, archive operations via Admin API
- Workspace-scoped memory for team collaboration

### User Provisioning Methods

#### 1. SCIM Provisioning (Automated)

```bash
# System for Cross-domain Identity Management
# Automates user lifecycle: create, update, deactivate, delete
# Integrates with IdP for synchronized access control
```

**SCIM Benefits:**
- Automated user provisioning tied to IdP authentication
- Advanced group mappings to determine user roles
- Consistent access control policies across systems
- Reduced manual administrative overhead

#### 2. Just-in-Time (JIT) Provisioning

```bash
# Users created automatically on first SSO login
# Profile attributes mapped from IdP claims
# Eliminates pre-provisioning requirements
```

**JIT Configuration:**
- Enable in SSO settings
- Map IdP attributes to Claude roles
- Configure default workspace assignment
- Set initial permission templates

#### 3. Manual Provisioning via Admin API

```bash
# Admin API endpoints for member management
POST /v1/organizations/{org_id}/invites
GET /v1/organizations/{org_id}/members
PATCH /v1/organizations/{org_id}/members/{member_id}
DELETE /v1/organizations/{org_id}/members/{member_id}
```

**Invitation Management:**
- Invites expire after 21 days (no modification after creation)
- Role assignment at invitation time
- Workspace assignment on acceptance
- No programmatic modification of pending invites

### SSO Integration

**Supported Protocols:**
- SAML 2.0
- OpenID Connect (OIDC)

**Supported Identity Providers:**
- Okta
- Azure AD (Microsoft Entra ID)
- Ping Identity
- Auth0
- Google Workspace
- OneLogin
- Any SAML 2.0 / OIDC compliant IdP

**SSO Configuration Steps:**

1. **Configure IdP Application:**
   ```yaml
   Application Type: SAML 2.0 or OIDC
   Entity ID: https://claude.ai/saml/metadata
   ACS URL: https://claude.ai/saml/acs
   Single Logout URL: https://claude.ai/saml/slo
   ```

2. **Map User Attributes:**
   ```yaml
   Required:
     - email (unique identifier)
     - firstName
     - lastName
   Optional:
     - department
     - title
     - manager
     - groups (for role mapping)
   ```

3. **Configure Claude Enterprise Settings:**
   - Upload IdP metadata XML
   - Configure attribute mappings
   - Enable JIT provisioning
   - Set default roles and workspaces
   - Enable domain capture (optional)

4. **Test SSO Flow:**
   ```bash
   # Test user authentication
   # Verify attribute mapping
   # Confirm role assignment
   # Validate workspace access
   ```

### Domain Capture

**Purpose:** Automatically enroll users from verified domains into organizational workspace

**Configuration:**
```json
{
  "domainCapture": {
    "enabled": true,
    "domains": ["company.com", "subsidiary.company.com"],
    "defaultWorkspace": "main-workspace",
    "defaultRole": "claude-code-user",
    "requireApproval": false
  }
}
```

**Behavior:**
- New signups with verified domain automatically join organization
- Existing users redirected to SSO on next login
- Optional admin approval workflow
- Prevents shadow IT usage outside organization

---

## Security Framework

### Authentication & Authorization

#### Multi-Factor Authentication (MFA)
- Enforced via SSO provider
- Support for TOTP, SMS, push notifications, hardware tokens
- Conditional access policies based on location, device, risk level

#### Session Management
- Configurable session timeout
- Idle timeout controls
- Concurrent session limits
- Device trust requirements

#### API Key Management

**Key Types:**
- Standard API Keys (`sk-ant-api-...`) - User or workspace scoped
- Admin API Keys (`sk-ant-admin-...`) - Organization admin access only

**Best Practices:**
```bash
# Rotate keys quarterly
# Use workspace-scoped keys when possible
# Monitor key usage via Admin API
# Revoke unused keys immediately
# Never commit keys to version control
```

**Admin API Key Operations:**
```bash
# List all API keys
GET /v1/organizations/{org_id}/api_keys

# Get specific key details
GET /v1/organizations/{org_id}/api_keys/{key_id}

# Update key (rotate, rename)
PATCH /v1/organizations/{org_id}/api_keys/{key_id}

# Note: New keys can only be created via Console for security
```

### Data Protection

#### Zero Data Retention (ZDR)
- Available for Enterprise API customers
- Anthropic doesn't store inputs/outputs
- Applies to API usage only (not Workbench or Claude Code)
- Requires explicit opt-in and contract terms

#### Data Residency
- Default: US data centers
- European data residency available for Enterprise
- Contractual data processing agreements
- GDPR compliance measures

#### Encryption
- In-transit: TLS 1.3
- At-rest: AES-256 encryption
- Key management via AWS KMS or customer-managed keys (CMK)

### Network Security

#### VPC Integration (AWS Bedrock)
```bash
# Private VPC endpoint for Bedrock-hosted Claude
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-12345678 \
  --service-name com.amazonaws.bedrock.runtime \
  --subnet-ids subnet-abc123 \
  --security-group-ids sg-xyz789
```

#### Private Service Connect (Google Vertex AI)
```bash
# PSC endpoints (GA April 2025)
gcloud compute forwarding-rules create claude-psc \
  --network=vpc-network \
  --address=internal-ip \
  --target-service-attachment=vertex-ai-claude
```

#### Firewall Rules
```bash
# Allowlist Claude API endpoints
*.anthropic.com
api.claude.ai
claude.ai

# Block personal Claude access (if using VPC/PSC)
# Configure DNS/firewall to route only to private endpoints
```

### File Access Controls

**Excluded Paths Configuration:**
```json
{
  "excludedPaths": [
    "**/secrets/**",
    "**/.env*",
    "**/credentials/**",
    "**/private_keys/**",
    "**/.aws/**",
    "**/.ssh/**",
    "**/passwords.txt",
    "**/token.json"
  ],
  "permissions": {
    "read": {
      "mode": "allowlist",
      "allowedPaths": [
        "**/src/**",
        "**/tests/**",
        "**/docs/**",
        "*.md",
        "*.json",
        "*.yaml"
      ]
    },
    "edit": {
      "mode": "ask",
      "autoApprovePatterns": [
        "**/tests/**/*.test.ts",
        "**/docs/**/*.md"
      ]
    }
  }
}
```

### Tool Permission Controls

**Granular Tool Access:**
```json
{
  "toolPermissions": {
    "bash": {
      "mode": "restricted",
      "allowedCommands": ["git", "npm", "pytest", "uv"],
      "deniedCommands": ["rm -rf", "dd", "mkfs", "curl", "wget"]
    },
    "read": {
      "mode": "allowlist",
      "excludePatterns": ["**/*.key", "**/*.pem", "**/.env*"]
    },
    "edit": {
      "mode": "ask",
      "requireReview": true
    },
    "webFetch": {
      "mode": "restricted",
      "allowedDomains": [
        "github.com",
        "docs.company.com",
        "stackoverflow.com"
      ]
    }
  },
  "disableBypassPermissionsMode": true
}
```

---

## Governance & Compliance Automation

### Hooks Framework

Claude Code hooks execute shell commands at critical workflow stages, enabling automated governance and compliance enforcement.

#### Hook Types & Event Lifecycle

**Available Hooks:**
- `PreToolUse` - Before any tool execution (validation, approval)
- `PostToolUse` - After tool execution (audit, quality checks)
- `SessionStart` - At session initialization (environment setup)
- `SessionEnd` - At session termination (cleanup, reporting)
- `PreCommit` - Before git commits (linting, security scans)
- `PostCommit` - After git commits (notifications, triggers)
- `PreTask` - Before task execution (planning, resource allocation)
- `PostTask` - After task completion (verification, documentation)
- `Notification` - For alerts and monitoring triggers

#### Hook Configuration

**Hooks Directory Structure:**
```bash
.claude/hooks/
├── pre-tool-use/
│   ├── security-scan.sh
│   ├── compliance-check.sh
│   └── resource-validator.sh
├── post-tool-use/
│   ├── audit-logger.sh
│   └── quality-verifier.sh
├── session-start/
│   ├── environment-setup.sh
│   └── policy-loader.sh
└── session-end/
    ├── session-reporter.sh
    └── cleanup.sh
```

**Hook Input Format (JSON):**
```json
{
  "event": "PreToolUse",
  "tool": "bash",
  "inputs": {
    "command": "rm sensitive_file.txt"
  },
  "session_id": "ses_abc123",
  "user_id": "usr_xyz789",
  "workspace_id": "ws_company",
  "timestamp": "2025-10-26T15:30:00Z",
  "transcript_path": "/var/log/claude/transcripts/ses_abc123.json"
}
```

**Hook Output (Decision Control):**
```bash
#!/bin/bash
# Exit codes control behavior:
# 0 = Allow/Approve
# 1 = Error (stops execution, shows to user)
# 2 = Block (stops execution, shows stderr to Claude)

# Example: Block dangerous commands
if echo "$INPUT" | jq -r '.inputs.command' | grep -qE 'rm -rf|dd|mkfs'; then
  echo "BLOCKED: Dangerous command detected" >&2
  exit 2
fi

# Example: Require approval for sensitive operations
if echo "$INPUT" | jq -r '.inputs.command' | grep -q 'production'; then
  echo '{"permissionDecision": "ask", "reason": "Production environment access requires approval"}'
  exit 0
fi

# Approve safe operations
exit 0
```

### Policy Enforcement Examples

#### 1. Compliance Checking Hook

```bash
#!/bin/bash
# .claude/hooks/pre-tool-use/compliance-check.sh

set -e

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool')
SESSION=$(echo "$INPUT" | jq -r '.session_id')

# Log all tool usage for audit trail
echo "$INPUT" >> "/var/log/claude/compliance/${SESSION}.log"

# Check if accessing financial data
if [ "$TOOL" = "read" ]; then
  FILE=$(echo "$INPUT" | jq -r '.inputs.file_path')

  if echo "$FILE" | grep -qE 'portfolio|trading|accounts'; then
    # Verify user has financial data access role
    USER_ROLES=$(get_user_roles.sh "$INPUT")

    if ! echo "$USER_ROLES" | grep -q 'financial_analyst'; then
      echo "COMPLIANCE VIOLATION: User lacks financial data access role" >&2
      echo "Required role: financial_analyst" >&2
      echo "Incident logged for security review" >&2

      # Alert compliance team
      send_alert.sh "compliance" "Unauthorized financial data access attempt"

      exit 2  # Block operation
    fi
  fi
fi

# Check for PII/sensitive data patterns
if [ "$TOOL" = "edit" ]; then
  CONTENT=$(echo "$INPUT" | jq -r '.inputs.new_string')

  # Scan for SSN, credit card numbers, etc.
  if echo "$CONTENT" | grep -qE '\b\d{3}-\d{2}-\d{4}\b|\b\d{16}\b'; then
    echo "COMPLIANCE WARNING: Potential PII detected in edit operation" >&2
    echo '{"permissionDecision": "ask", "reason": "Content contains potential PII - requires manual review"}'
    exit 0
  fi
fi

# Approve compliant operations
exit 0
```

#### 2. Security Validation Hook

```bash
#!/bin/bash
# .claude/hooks/pre-tool-use/security-scan.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool')

# Block risky bash commands
if [ "$TOOL" = "bash" ]; then
  COMMAND=$(echo "$INPUT" | jq -r '.inputs.command')

  # Check against denylist
  DENIED_PATTERNS=(
    'rm -rf /'
    'dd if='
    'mkfs'
    'curl.*|.*sh'
    'wget.*|.*sh'
    '> /dev/'
    'chmod 777'
    'chmod -R 777'
  )

  for pattern in "${DENIED_PATTERNS[@]}"; do
    if echo "$COMMAND" | grep -qE "$pattern"; then
      echo "SECURITY BLOCK: Command matches denied pattern: $pattern" >&2
      send_alert.sh "security" "Blocked dangerous command: $COMMAND"
      exit 2
    fi
  done

  # Warn on production access
  if echo "$COMMAND" | grep -qE 'prod|production'; then
    echo '{"permissionDecision": "ask", "reason": "Production system access requires approval"}'
    exit 0
  fi
fi

# Check file write operations
if [ "$TOOL" = "edit" ] || [ "$TOOL" = "write" ]; then
  FILE=$(echo "$INPUT" | jq -r '.inputs.file_path')

  # Block writes to system directories
  if echo "$FILE" | grep -qE '^/etc/|^/usr/|^/sys/|^/proc/'; then
    echo "SECURITY BLOCK: Cannot write to system directories" >&2
    exit 2
  fi

  # Require approval for config files
  if echo "$FILE" | grep -qE 'config\.yaml|settings\.json|\.env'; then
    echo '{"permissionDecision": "ask", "reason": "Configuration file modification requires approval"}'
    exit 0
  fi
fi

exit 0
```

#### 3. Quality Assurance Hook

```bash
#!/bin/bash
# .claude/hooks/post-tool-use/quality-verifier.sh

INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool')
SUCCESS=$(echo "$INPUT" | jq -r '.success')

# Only run QA on successful operations
if [ "$SUCCESS" != "true" ]; then
  exit 0
fi

# Verify code changes meet standards
if [ "$TOOL" = "edit" ]; then
  FILE=$(echo "$INPUT" | jq -r '.inputs.file_path')

  # Run linter on code files
  if echo "$FILE" | grep -qE '\.(py|js|ts|tsx)$'; then
    if ! run_linter.sh "$FILE"; then
      echo "QUALITY ISSUE: Code does not pass linting checks" >&2
      echo "Please fix linting errors before proceeding" >&2
      echo '{"decision": "block", "reason": "Linting failures detected"}'
      exit 2
    fi
  fi

  # Check for TODOs in production code
  if echo "$FILE" | grep -qE 'src/|lib/' && ! echo "$FILE" | grep -q 'test'; then
    if grep -q 'TODO\|FIXME\|HACK' "$FILE"; then
      echo "QUALITY WARNING: Production code contains TODO/FIXME comments" >&2
      echo "Consider addressing these before deployment" >&2
      # Don't block, just warn
    fi
  fi
fi

# Run tests after code changes
if [ "$TOOL" = "edit" ] && echo "$FILE" | grep -qE '\.(py|ts)$'; then
  # Check if tests exist
  TEST_FILE=$(get_test_file.sh "$FILE")
  if [ -f "$TEST_FILE" ]; then
    if ! run_tests.sh "$TEST_FILE"; then
      echo "QUALITY ISSUE: Tests failing for modified code" >&2
      echo '{"decision": "block", "reason": "Test failures detected"}'
      exit 2
    fi
  fi
fi

exit 0
```

#### 4. Audit Logging Hook

```bash
#!/bin/bash
# .claude/hooks/post-tool-use/audit-logger.sh

INPUT=$(cat)
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SESSION=$(echo "$INPUT" | jq -r '.session_id')
USER=$(echo "$INPUT" | jq -r '.user_id')
TOOL=$(echo "$INPUT" | jq -r '.tool')
SUCCESS=$(echo "$INPUT" | jq -r '.success')

# Structure audit log entry
AUDIT_ENTRY=$(jq -n \
  --arg ts "$TIMESTAMP" \
  --arg sess "$SESSION" \
  --arg usr "$USER" \
  --arg tl "$TOOL" \
  --arg succ "$SUCCESS" \
  --argjson inp "$INPUT" \
  '{
    timestamp: $ts,
    session_id: $sess,
    user_id: $usr,
    tool: $tl,
    success: $succ,
    details: $inp
  }')

# Write to audit log
echo "$AUDIT_ENTRY" >> "/var/log/claude/audit/${SESSION}.jsonl"

# Send high-value events to SIEM
if echo "$TOOL" | grep -qE 'bash|edit|write'; then
  send_to_siem.sh "$AUDIT_ENTRY"
fi

# Track usage metrics
update_usage_metrics.sh "$USER" "$TOOL" "$SUCCESS"

exit 0
```

#### 5. Cost Control Hook

```bash
#!/bin/bash
# .claude/hooks/pre-tool-use/cost-control.sh

INPUT=$(cat)
USER=$(echo "$INPUT" | jq -r '.user_id')
SESSION=$(echo "$INPUT" | jq -r '.session_id')

# Check user's usage against budget
USAGE=$(get_user_usage.sh "$USER")
BUDGET=$(get_user_budget.sh "$USER")

if [ "$USAGE" -ge "$BUDGET" ]; then
  echo "BUDGET EXCEEDED: User has reached spending limit" >&2
  echo "Current usage: $USAGE tokens" >&2
  echo "Budget: $BUDGET tokens" >&2
  send_alert.sh "billing" "User $USER exceeded budget"
  exit 2
fi

# Warn at 80% threshold
THRESHOLD=$(echo "$BUDGET * 0.8" | bc | cut -d. -f1)
if [ "$USAGE" -ge "$THRESHOLD" ]; then
  echo "WARNING: Approaching budget limit ($USAGE / $BUDGET tokens)" >&2
fi

exit 0
```

### Session Recording & Transcripts

**Automatic Session Logging:**
```bash
# Each session generates a transcript at:
/var/log/claude/transcripts/${SESSION_ID}.json

# Transcript contains:
{
  "session_id": "ses_abc123",
  "user_id": "usr_xyz789",
  "workspace_id": "ws_company",
  "start_time": "2025-10-26T15:00:00Z",
  "end_time": "2025-10-26T16:30:00Z",
  "tool_calls": [
    {
      "timestamp": "2025-10-26T15:05:23Z",
      "tool": "read",
      "inputs": {"file_path": "/src/app.py"},
      "outputs": {"content": "..."},
      "success": true
    }
  ],
  "messages": [...],
  "hooks_executed": [...]
}
```

**Transcript Analysis:**
```bash
# Extract all bash commands from session
jq '.tool_calls[] | select(.tool == "bash") | .inputs.command' \
  /var/log/claude/transcripts/${SESSION_ID}.json

# Find failed operations
jq '.tool_calls[] | select(.success == false)' \
  /var/log/claude/transcripts/${SESSION_ID}.json

# Calculate session cost
jq '[.tool_calls[] | .cost] | add' \
  /var/log/claude/transcripts/${SESSION_ID}.json
```

### Headless Mode for CI/CD

**Headless Execution:**
```bash
# Run Claude in non-interactive mode
claude --headless \
  --project /path/to/repo \
  --prompt "Run all tests and generate coverage report" \
  --output /tmp/claude-results.json

# Use in CI pipeline
# .github/workflows/claude-qa.yml
name: Claude QA
on: [pull_request]
jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Claude Code Review
        run: |
          claude --headless \
            --prompt "Review PR changes for security issues and code quality" \
            --output pr-review.json
      - name: Post Results
        run: gh pr comment --body-file pr-review.json
```

---

## MCP Server Enterprise Controls

### Model Context Protocol (MCP) Overview

MCP enables Claude to integrate with external tools, databases, and APIs. Enterprise controls ensure only approved servers are accessible.

### Enterprise MCP Configuration

**Deployment Path:**
```bash
# Same locations as managed-settings.json
/etc/claude-code/managed-mcp.json  # Linux/WSL
/Library/Application Support/ClaudeCode/managed-mcp.json  # macOS
C:\ProgramData\ClaudeCode\managed-mcp.json  # Windows
```

**Configuration Structure:**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "company-analytics": {
      "command": "/opt/company/mcp-servers/analytics-server",
      "env": {
        "API_ENDPOINT": "https://analytics.internal.company.com",
        "AUTH_TOKEN": "${ANALYTICS_TOKEN}"
      },
      "allowedWorkspaces": ["finance", "analytics"]
    },
    "sentry": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sentry"],
      "env": {
        "SENTRY_ORG": "company",
        "SENTRY_TOKEN": "${SENTRY_TOKEN}"
      }
    }
  }
}
```

### Allowlist vs Denylist (2025 Update)

**IMPORTANT:** Blocklist feature deprecated October 31, 2025, replaced with allowlist-first approach.

**Deny-by-Default Model (Recommended):**
```json
{
  "useEnterpriseMcpConfigOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverName": "company-analytics" },
    { "serverName": "sentry" },
    { "serverName": "company-internal-*" }
  ],
  "deniedMcpServers": [
    { "serverName": "filesystem" },
    { "serverName": "*-public" },
    { "serverName": "experimental-*" }
  ]
}
```

**Configuration Precedence:**
1. `deniedMcpServers` takes absolute precedence (if in both lists, blocked)
2. `allowedMcpServers` permits explicitly listed servers
3. `useEnterpriseMcpConfigOnly: true` blocks all non-managed servers
4. Enterprise MCP config has highest precedence, cannot be overridden

**Master Disable Switch:**
```json
{
  "mcpEnabled": false  // Disables ALL MCP functionality organization-wide
}
```

### MCP Security Best Practices

1. **Start with narrow allowlist:** Only approve proven, necessary servers
2. **Use denylist on top of allowlist:** Layer defenses
3. **Enable `useEnterpriseMcpConfigOnly`:** Prevent shadow servers
4. **Workspace-scope servers:** Limit server access to specific teams
5. **Rotate credentials regularly:** Use environment variables, rotate tokens quarterly
6. **Monitor server usage:** Track via audit logs and analytics
7. **Review server code:** Audit open-source servers before deployment
8. **Implement network controls:** Restrict server network access via firewall rules

### MCP Server Governance Pattern

```bash
# Enterprise MCP Server Approval Workflow

1. Developer Request
   ├─ Submit request via governance portal
   └─ Provide: server name, purpose, workspace, risk assessment

2. Security Review
   ├─ Code audit (if custom server)
   ├─ Dependency scan
   ├─ Network access review
   └─ Data access scope evaluation

3. Compliance Review
   ├─ Data classification check
   ├─ Regulatory requirement verification
   └─ Audit trail requirements

4. Approval & Deployment
   ├─ Add to managed-mcp.json
   ├─ Update allowlist
   ├─ Deploy to target workspaces
   └─ Document in server registry

5. Ongoing Monitoring
   ├─ Track usage via audit logs
   ├─ Review quarterly for continued need
   ├─ Update on security advisories
   └─ Rotate credentials on schedule
```

---

## Scaling Patterns & Multi-Agent Architecture

### Hierarchical Multi-Agent Systems

Claude Code's subagent architecture (launched July 2025) enables sophisticated multi-agent orchestration for complex tasks.

#### Three-Tier Scaling Pattern

```
Strategic Orchestrator (Opus 4)
├─ Maintains big picture
├─ Sets objectives
├─ Allocates resources
└─ Coordinates coordinators

Middle-Tier Coordinators (Sonnet 4)
├─ Research Coordinator
├─ Analysis Coordinator
├─ Content Coordinator
└─ Implementation Coordinator

Ground-Tier Specialists (Sonnet 4 / Haiku)
├─ Data Fetcher
├─ Code Analyzer
├─ Test Runner
├─ Documentation Generator
└─ Quality Checker
```

**Benefits:**
- Handle hundreds of simultaneous tasks without overwhelming single agent
- Reduce costs by 40-60% (use smaller models for specific tasks, Opus for orchestration)
- Scale elegantly: 2-3 agents for simple queries, 20-30 for comprehensive research
- Dynamic adaptation: spawn agents as needed, consolidate results as subtasks complete

### Orchestrator-Worker Pattern

**Architecture:**
```python
# Pseudo-code for orchestrator pattern

class Orchestrator:
    """Lead agent (Opus 4) coordinates specialized subagents"""

    def __init__(self):
        self.workers = {}
        self.state = {}

    def delegate_task(self, task):
        # Analyze task complexity
        subtasks = self.break_down_task(task)

        # Spawn specialized workers (Sonnet 4)
        for subtask in subtasks:
            worker_type = self.determine_worker_type(subtask)
            worker = self.spawn_worker(worker_type)
            self.workers[worker.id] = worker
            worker.execute(subtask)

        # Coordinate and consolidate results
        results = self.wait_for_completion()
        return self.synthesize_results(results)

    def spawn_worker(self, worker_type):
        """Create specialized subagent with narrow scope"""
        return SubAgent(
            model="claude-sonnet-4",
            role=worker_type,
            tools=self.get_tools_for_role(worker_type),
            permissions=self.get_permissions_for_role(worker_type)
        )
```

### Production-Ready Subagent Patterns

**Golden Rule:** One job per subagent, orchestrator coordinates

#### 1. Sequential Pipeline Pattern

```bash
# Deterministic workflow for predictable tasks
Analyst → Architect → Implementer → Tester → Security Auditor

Example: Feature implementation
1. Analyst: Understand requirements, identify dependencies
2. Architect: Design solution, create technical spec
3. Implementer: Write code, implement design
4. Tester: Create and run tests, verify functionality
5. Security Auditor: Scan for vulnerabilities, verify compliance
```

**Use when:**
- Tasks have clear dependencies
- Each step must complete before next
- Predictable workflow with defined stages

#### 2. Parallel Specialization Pattern

```bash
# Independent specialists work simultaneously
UI Specialist ─┐
API Specialist ├─→ Integrator → QA
DB Specialist  ─┘

Example: Full-stack feature
- UI Specialist: Build React components
- API Specialist: Implement REST endpoints
- DB Specialist: Design schema, write migrations
- Integrator: Connect layers, resolve conflicts
- QA: End-to-end testing
```

**Use when:**
- Low dependencies between subtasks
- Work can be parallelized
- Integration step needed at end

#### 3. Research Swarm Pattern

```bash
# Multiple researchers gather data, analyst synthesizes
Researcher A ─┐
Researcher B ├─→ Analyst → Reporter
Researcher C ─┘

Example: Market research
- Researcher A: Competitor analysis
- Researcher B: Customer sentiment
- Researcher C: Technical benchmarks
- Analyst: Synthesize findings, identify patterns
- Reporter: Generate executive summary
```

**Use when:**
- Information gathering from multiple sources
- Diverse perspectives needed
- Synthesis required

#### 4. Review Pipeline Pattern

```bash
# Iterative review and refinement
Generator → Reviewer → Refiner → Validator → Approver

Example: Document creation
1. Generator: Create initial draft
2. Reviewer: Identify issues, provide feedback
3. Refiner: Address feedback, improve quality
4. Validator: Check against requirements
5. Approver: Final review, approve for publication
```

**Use when:**
- Quality standards are critical
- Iterative improvement needed
- Multiple review stages required

### Resource Optimization Strategies

#### Token Efficiency

```python
# Orchestrator manages context efficiently
class Orchestrator:
    def optimize_context(self):
        # Use smaller models for routine tasks
        if task.complexity == "low":
            model = "claude-haiku-4"  # Fast, cheap
        elif task.complexity == "medium":
            model = "claude-sonnet-4"  # Balanced
        else:
            model = "claude-opus-4"  # Maximum capability

        # Compress context for subagents
        subagent_context = self.extract_relevant_context(task)
        # Don't pass full conversation history to workers

        return model, subagent_context
```

**Cost Savings:**
- Reserve Opus 4 for orchestration only
- Use Sonnet 4 for specialized tasks (60% cheaper)
- Use Haiku for simple operations (90% cheaper)
- Typical savings: 40-60% compared to using Opus for everything

#### Background Task Management

```bash
# Prevent resource conflicts
# Task orchestration with resource isolation

Task Scheduler
├─ Task-specific resource limits
├─ Memory constraints
├─ CPU throttling
└─ Priority queuing

Error Handling
├─ Circuit breaker patterns
├─ Exponential backoff
└─ Automatic retry mechanisms
```

### Multi-Tenant Deployment Patterns

#### Workspace Isolation

```yaml
# Enterprise multi-tenant architecture
Organization
├─ Trading Desk Workspace
│   ├─ Subagent pool: Market analyzers, order managers
│   ├─ MCP servers: Market data, broker APIs
│   └─ Resources: Dedicated compute, priority queue
├─ Risk Management Workspace
│   ├─ Subagent pool: Risk calculators, compliance checkers
│   ├─ MCP servers: Position data, regulatory feeds
│   └─ Resources: Shared compute, standard queue
└─ Research Workspace
    ├─ Subagent pool: Research aggregators, report generators
    ├─ MCP servers: News feeds, financial databases
    └─ Resources: Burstable compute, low priority
```

**Isolation Guarantees:**
- Memory boundaries between workspaces
- Separate MCP server configurations
- Independent audit logs
- Workspace-scoped API keys
- Resource quotas per workspace

#### Scaling by Team Size

| Team Size | Workspaces | Subagents | Orchestrators | Cost/Month (est.) |
|-----------|-----------|-----------|---------------|-------------------|
| 1-10 | 1-2 | 5-10 | 1 | $500-2,000 |
| 10-50 | 3-10 | 20-50 | 2-5 | $2,000-10,000 |
| 50-200 | 10-30 | 50-200 | 5-20 | $10,000-50,000 |
| 200+ | 30-100 | 200-1000+ | 20-100 | $50,000+ |

---

## Knowledge Management & Memory Tools

### Claude Memory System (2025)

Persistent context across conversations enabling continuous learning and team collaboration.

#### Memory Hierarchy

**Three-Level Memory Architecture:**

1. **Local Project Memory** (`.claude/CLAUDE.local.md`)
   - Personal workspace notes
   - Gitignored - not shared with team
   - Session-specific context
   - Temporary reminders and preferences

2. **Shared Project Memory** (`.claude/CLAUDE.md`)
   - Team documentation
   - Version controlled, committed to repo
   - Project architecture and standards
   - Living documentation for humans AND AI

3. **User Global Memory** (`~/.claude/CLAUDE.md`)
   - Personal preferences across all projects
   - Global coding standards
   - Frequently used patterns
   - Cross-project conventions

#### Memory File Best Practices

**Effective Memory Structure:**

```markdown
# .claude/CLAUDE.md - Shared Team Memory

## Project Overview
- Portfolio validation engine for M1 strategy
- Multi-agent architecture with specialized validators
- Python 3.11+, uv for dependency management

## Architecture Principles
1. Separation of concerns: Each agent handles one validation domain
2. Event-driven communication via message bus
3. Immutable validation results
4. Comprehensive audit logging

## Critical Standards
- ALL financial calculations must have unit tests
- NO hardcoded API keys (use environment variables)
- Validate ALL external data before processing
- Log ALL validation decisions with rationale

## Common Patterns

### Agent Implementation
Each validation agent follows this structure:
- Inherits from BaseValidator
- Implements validate() method
- Returns ValidationResult object
- Logs all decisions to audit trail

### Error Handling
- Catch specific exceptions, not bare except
- Log errors with full context
- Return ValidationResult with error details
- Never fail silently

## Project-Specific Commands
- `uv run pytest` - Run full test suite
- `uv run python -m auth_service.run` - Start auth service
- `make validate` - Run all validation checks

## Recent Decisions
- 2025-10-26: Consolidated auth service for Schwab & Webull
- 2025-10-25: Added browser automation for Webull auth
- 2025-10-24: Implemented retry logic with exponential backoff

## Dependencies to Watch
- webull: Unofficial SDK, may break
- schwab-py: Official but limited capabilities
- playwright: Heavy dependency, needed for browser auth
```

**Personal Memory Example:**

```markdown
# ~/.claude/CLAUDE.md - Personal Global Preferences

## My Coding Style
- Prefer type hints in Python
- Use descriptive variable names, avoid abbreviations
- Add docstrings to all public functions
- Comment WHY, not WHAT

## My Project Conventions
- tests/ directory mirrors src/ structure
- Use pytest fixtures for test setup
- Mock external services in unit tests
- Integration tests use Docker containers

## My Frequent Tasks
- When adding API client: Always include retry logic
- When writing validators: Include both happy and error paths
- When modifying schemas: Update both Pydantic model and docs
```

#### Memory Performance Impact

**Benchmark Results (100-turn evaluation):**
- Memory tool + context editing: **39% improvement** over baseline
- Context editing alone: 29% improvement
- Token consumption reduction: **84% fewer tokens** vs. no context management
- Enables workflows that would fail due to context exhaustion

**Memory Budget Guidelines:**
- Core memory files: Keep under 500 lines
- Use imports for detailed specifications
- Be ruthless about removing obsolete information
- Regular audits against actual codebase

#### Memory Maintenance Workflow

```bash
# Checkpoint Pattern: Update memory before major changes

# 1. Before refactoring, capture current state
claude --prompt "Update CLAUDE.md with current architecture decisions"

# 2. Perform refactoring work
# ... multiple sessions ...

# 3. After refactoring, update with new state
claude --prompt "Update CLAUDE.md with refactoring outcomes and new patterns"

# This creates knowledge checkpoints that persist across sessions
```

**Memory Audit Script:**

```bash
#!/bin/bash
# audit-memory.sh - Check memory file relevance

MEMORY_FILE=".claude/CLAUDE.md"

# Check for outdated dependency versions
grep -n "python 3.9" "$MEMORY_FILE" && echo "WARNING: Python version outdated"

# Find references to deleted files
grep -o "'[^']*\.py'" "$MEMORY_FILE" | while read -r file; do
  file=$(echo "$file" | tr -d "'")
  if [ ! -f "$file" ]; then
    echo "WARNING: Memory references deleted file: $file"
  fi
done

# Check memory file size
LINES=$(wc -l < "$MEMORY_FILE")
if [ "$LINES" -gt 500 ]; then
  echo "WARNING: Memory file exceeds recommended 500 lines ($LINES lines)"
fi
```

### Team Knowledge Management Patterns

#### 1. Documentation as Memory

**Treat memory files as living documentation:**
- Human-readable AND AI-readable
- Updated alongside code changes
- Reviewed in pull requests
- Versioned with codebase

#### 2. Shared Plugin Marketplace

**Enterprise Plugin Registry:**
```yaml
# .claude/plugins/registry.yaml
plugins:
  - name: company-code-standards
    version: 2.1.0
    source: internal-registry.company.com
    workspaces: [all]

  - name: financial-validation-toolkit
    version: 1.5.2
    source: internal-registry.company.com
    workspaces: [trading, risk, compliance]

  - name: security-scanner
    version: 3.0.0
    source: internal-registry.company.com
    mandatory: true
    workspaces: [all]
```

**Benefits:**
- Standardized capabilities across teams
- Centralized version management
- Mandatory security plugins
- Team-specific plugin access

#### 3. Sub-Agent Configuration Standardization

**Enterprise Sub-Agent Templates:**
```python
# .claude/subagents/templates/financial-analyst.yaml
name: financial-analyst
model: claude-sonnet-4
role: Analyze financial data and generate insights
tools:
  - read
  - calculator
  - financial-data-mcp
permissions:
  read:
    allowedPaths: ["**/data/**", "**/reports/**"]
  bash:
    mode: deny
memory:
  - .claude/CLAUDE.md
  - .claude/financial-standards.md
outputFormat: structured-json
maxTokens: 8000
```

**Standardization Benefits:**
- Consistent sub-agent behavior across projects
- Reusable configurations
- Easier onboarding
- Reduced configuration errors

#### 4. Knowledge Handoff Protocols

**Session Handoff Checklist:**
```markdown
# Session Handoff Template
# Update memory files before ending session

## What was accomplished:
- [ ] List completed tasks
- [ ] Document new patterns/decisions
- [ ] Update architecture diagrams (if changed)

## Context for next session:
- [ ] Describe current state
- [ ] List remaining work
- [ ] Note any blockers or issues

## Memory updates made:
- [ ] Updated .claude/CLAUDE.md with new patterns
- [ ] Added recent decisions section
- [ ] Updated dependency notes if changed
- [ ] Removed obsolete information
```

### Memory Tool Enterprise Features

**Claude Max, Team, and Enterprise Plans:**

| Feature | Max | Team | Enterprise |
|---------|-----|------|------------|
| Personal Memory | ✅ | ✅ | ✅ |
| Shared Project Memory | ✅ | ✅ | ✅ |
| On-demand Recall | ✅ | ✅ | ✅ |
| Project-scoped Memory | ❌ | ✅ | ✅ |
| Admin Memory Controls | ❌ | ❌ | ✅ |
| Memory Audit Logs | ❌ | ❌ | ✅ |
| Organization Memory Templates | ❌ | ❌ | ✅ |

**Enterprise Memory Controls:**
```json
{
  "memory": {
    "enabled": true,
    "allowPersonalMemory": true,
    "allowProjectMemory": true,
    "requireMemoryReview": true,
    "memoryRetentionDays": 90,
    "auditMemoryAccess": true,
    "memoryTemplates": [
      "financial-project-template",
      "security-project-template"
    ]
  }
}
```

---

## Monitoring, Audit Trails & Observability

### Usage & Cost Monitoring

#### Admin API Analytics Endpoints

**Organization-Level Metrics:**
```bash
# Get usage report
GET /v1/organizations/{org_id}/usage
?start_date=2025-10-01
&end_date=2025-10-31
&group_by=workspace,user,model

# Response structure
{
  "period": "2025-10-01 to 2025-10-31",
  "total_requests": 15234,
  "total_tokens": 45678901,
  "total_cost_usd": 1234.56,
  "breakdown": [
    {
      "workspace": "trading",
      "user": "usr_abc123",
      "model": "claude-opus-4",
      "requests": 234,
      "tokens": 1234567,
      "cost_usd": 123.45
    }
  ]
}
```

**Cost Report API:**
```bash
# Get detailed cost breakdown
GET /v1/organizations/{org_id}/cost
?start_date=2025-10-01
&end_date=2025-10-31
&currency=USD

# Response
{
  "total_cost": 1234.56,
  "by_workspace": {
    "trading": 567.89,
    "risk": 234.56,
    "research": 123.45
  },
  "by_model": {
    "claude-opus-4": 890.12,
    "claude-sonnet-4": 234.56,
    "claude-haiku-4": 45.67
  },
  "by_user": {
    "top_users": [
      {"user_id": "usr_abc", "cost": 234.56},
      {"user_id": "usr_xyz", "cost": 123.45}
    ]
  },
  "trend": "increasing",
  "forecast_next_month": 1500.00
}
```

**Claude Code Analytics:**
```bash
# Get developer productivity metrics
GET /v1/organizations/{org_id}/claude-code-usage
?start_date=2025-10-01
&end_date=2025-10-31

# Response
{
  "total_sessions": 456,
  "total_duration_minutes": 12345,
  "code_changes": {
    "lines_added": 5678,
    "lines_removed": 2345,
    "files_modified": 234,
    "commits": 123
  },
  "tool_usage": {
    "read": 1234,
    "edit": 567,
    "bash": 234,
    "webFetch": 123
  },
  "by_user": [
    {
      "user_id": "usr_abc",
      "sessions": 45,
      "acceptance_rate": 0.78,
      "productivity_score": 8.5
    }
  ],
  "metrics": {
    "average_session_duration": 27.04,
    "suggestion_acceptance_rate": 0.72,
    "commits_per_session": 0.27
  }
}
```

#### Programmatic Monitoring

**Usage Monitoring Script:**
```python
#!/usr/bin/env python3
# monitor-usage.py

import anthropic
import os
from datetime import datetime, timedelta

# Initialize Admin API client
client = anthropic.AdminAPI(api_key=os.environ['CLAUDE_ADMIN_API_KEY'])

# Get last 7 days usage
end_date = datetime.now()
start_date = end_date - timedelta(days=7)

usage = client.organizations.usage(
    organization_id="org-123",
    start_date=start_date.isoformat(),
    end_date=end_date.isoformat(),
    group_by=["workspace", "user"]
)

# Alert on anomalies
for entry in usage.breakdown:
    if entry.cost_usd > 500:  # Alert if user exceeds $500/week
        send_alert(
            f"High usage alert: {entry.user} spent ${entry.cost_usd} "
            f"in {entry.workspace} workspace"
        )

    # Check for unusual activity
    if entry.requests > 1000:  # More than 1000 requests/week
        send_alert(
            f"High request volume: {entry.user} made {entry.requests} requests"
        )

# Generate weekly report
generate_report(usage, recipients=["finance@company.com", "eng-leads@company.com"])
```

### Audit Trail Implementation

#### Audit Log Structure

**Enterprise Audit Logs (30-day retention):**
```json
{
  "event_id": "evt_abc123",
  "timestamp": "2025-10-26T15:30:45.123Z",
  "event_type": "tool_execution",
  "severity": "info",
  "actor": {
    "user_id": "usr_xyz789",
    "email": "analyst@company.com",
    "role": "claude-code-user",
    "ip_address": "10.0.1.50",
    "user_agent": "ClaudeCode/1.5.0"
  },
  "resource": {
    "type": "file",
    "path": "/home/user/project/src/portfolio_validator.py",
    "workspace_id": "ws_trading",
    "project": "portfolio-validation-engine"
  },
  "action": {
    "tool": "edit",
    "operation": "modify_file",
    "details": {
      "lines_changed": 23,
      "functions_modified": ["validate_positions", "calculate_risk"]
    }
  },
  "context": {
    "session_id": "ses_abc123",
    "prompt": "Add position size validation",
    "conversation_turn": 15
  },
  "security": {
    "policy_evaluated": "financial-data-access",
    "policy_result": "allow",
    "mfa_verified": true,
    "hooks_triggered": ["pre-tool-use/security-scan", "post-tool-use/audit-logger"]
  },
  "compliance": {
    "data_classification": "confidential",
    "regulatory_tags": ["SOX", "FINRA"],
    "retention_period_days": 2555
  }
}
```

**Audit Event Types:**
- `user_login` / `user_logout` / `sso_auth`
- `session_start` / `session_end`
- `tool_execution` (read, edit, bash, etc.)
- `file_access` / `file_modification`
- `api_key_created` / `api_key_rotated` / `api_key_revoked`
- `permission_change` / `role_assignment`
- `policy_violation` / `security_alert`
- `mcp_server_connection` / `mcp_server_call`
- `workspace_created` / `workspace_archived`
- `member_invited` / `member_removed`

#### SIEM Integration

**Export Audit Logs to SIEM:**
```python
#!/usr/bin/env python3
# export-to-siem.py

import anthropic
from datetime import datetime, timedelta
import json

client = anthropic.AdminAPI(api_key=os.environ['CLAUDE_ADMIN_API_KEY'])

# Fetch last hour of audit logs
end_time = datetime.now()
start_time = end_time - timedelta(hours=1)

audit_logs = client.organizations.audit_logs(
    organization_id="org-123",
    start_time=start_time.isoformat(),
    end_time=end_time.isoformat(),
    event_types=["tool_execution", "security_alert", "policy_violation"]
)

# Forward to SIEM (Splunk example)
import requests

SPLUNK_HEC_URL = "https://splunk.company.com:8088/services/collector/event"
SPLUNK_TOKEN = os.environ['SPLUNK_HEC_TOKEN']

for log in audit_logs:
    event = {
        "time": log.timestamp,
        "source": "claude-code",
        "sourcetype": "claude:audit",
        "event": log
    }

    requests.post(
        SPLUNK_HEC_URL,
        headers={
            "Authorization": f"Splunk {SPLUNK_TOKEN}",
            "Content-Type": "application/json"
        },
        data=json.dumps(event)
    )
```

**Datadog Integration:**
```python
from datadog import initialize, api
import os

options = {
    'api_key': os.environ['DATADOG_API_KEY'],
    'app_key': os.environ['DATADOG_APP_KEY']
}
initialize(**options)

# Send audit events to Datadog
for log in audit_logs:
    api.Event.create(
        title=f"Claude Code: {log.event_type}",
        text=f"{log.actor.email} performed {log.action.operation}",
        tags=[
            f"user:{log.actor.user_id}",
            f"workspace:{log.resource.workspace_id}",
            f"severity:{log.severity}"
        ],
        alert_type=log.severity
    )
```

### Compliance API

**Programmatic Compliance Monitoring:**
```python
#!/usr/bin/env python3
# compliance-monitor.py

import anthropic
from datetime import datetime, timedelta

client = anthropic.ComplianceAPI(api_key=os.environ['CLAUDE_COMPLIANCE_API_KEY'])

# Get usage data for compliance reporting
usage_data = client.get_usage(
    organization_id="org-123",
    start_date=(datetime.now() - timedelta(days=30)).isoformat(),
    include_content=False,  # Don't export actual content for privacy
    include_metadata=True
)

# Get customer content access logs (for data governance)
content_access = client.get_content_access_logs(
    organization_id="org-123",
    start_date=(datetime.now() - timedelta(days=7)).isoformat(),
    filter={
        "data_classification": ["confidential", "restricted"],
        "workspaces": ["trading", "compliance"]
    }
)

# Automated policy enforcement
for access_log in content_access:
    # Flag suspicious access patterns
    if access_log.access_count > 100 and access_log.time_range_hours < 1:
        flag_for_review(
            user=access_log.user_id,
            reason="Unusual access volume",
            details=access_log
        )

    # Verify authorized access
    if not verify_user_authorization(access_log.user_id, access_log.resource):
        create_incident(
            severity="high",
            type="unauthorized_access",
            details=access_log
        )

# Selective deletion for data retention policies
expired_data = client.find_expired_content(
    organization_id="org-123",
    retention_policy="financial-records-7-years"
)

for item in expired_data:
    client.delete_content(content_id=item.content_id)
    log_deletion(item, reason="retention_policy_expired")
```

### Real-Time Monitoring Dashboards

**Grafana Dashboard Configuration:**
```yaml
# claude-code-monitoring.yaml
dashboard:
  title: Claude Code Enterprise Monitoring
  refresh: 30s

  panels:
    - title: Active Sessions
      type: stat
      query: |
        SELECT COUNT(DISTINCT session_id)
        FROM claude_sessions
        WHERE status = 'active'
        AND timestamp > NOW() - INTERVAL '5 minutes'

    - title: Token Usage by Workspace
      type: timeseries
      query: |
        SELECT
          timestamp,
          workspace_id,
          SUM(tokens) as total_tokens
        FROM claude_usage
        WHERE timestamp > NOW() - INTERVAL '24 hours'
        GROUP BY timestamp, workspace_id

    - title: Cost per User (Top 10)
      type: bar
      query: |
        SELECT
          user_id,
          SUM(cost_usd) as total_cost
        FROM claude_usage
        WHERE timestamp > NOW() - INTERVAL '30 days'
        GROUP BY user_id
        ORDER BY total_cost DESC
        LIMIT 10

    - title: Security Alerts
      type: table
      query: |
        SELECT
          timestamp,
          event_type,
          user_id,
          details
        FROM claude_audit_logs
        WHERE severity IN ('high', 'critical')
        AND timestamp > NOW() - INTERVAL '24 hours'
        ORDER BY timestamp DESC

    - title: Tool Usage Distribution
      type: pie
      query: |
        SELECT
          tool_name,
          COUNT(*) as usage_count
        FROM claude_tool_usage
        WHERE timestamp > NOW() - INTERVAL '7 days'
        GROUP BY tool_name

    - title: Session Success Rate
      type: gauge
      query: |
        SELECT
          COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 /
          COUNT(*) as success_rate
        FROM claude_sessions
        WHERE timestamp > NOW() - INTERVAL '24 hours'

  alerts:
    - name: High Cost Alert
      condition: total_cost_usd > 1000
      interval: 1h
      notifications: [email, slack]

    - name: Policy Violation
      condition: policy_violations > 0
      interval: 5m
      notifications: [email, pagerduty]

    - name: Unusual Activity
      condition: requests_per_minute > 100
      interval: 5m
      notifications: [slack]
```

### Performance Monitoring

**Key Metrics to Track:**

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Session Success Rate | > 95% | < 90% |
| Average Session Duration | 15-30 min | > 60 min |
| Tool Call Success Rate | > 98% | < 95% |
| API Response Time (p95) | < 500ms | > 2000ms |
| Token Efficiency | > 80% relevant | < 60% relevant |
| Cost per Session | $0.50-$2.00 | > $5.00 |
| Security Violations | 0 | > 0 |
| Hook Execution Time | < 5s | > 30s |

---

## Financial Services Implementation

### Regulatory Compliance Requirements

#### SOX (Sarbanes-Oxley) Compliance

**Key Requirements:**
- Audit trails for all financial data access
- Change management controls
- Segregation of duties
- Access controls and authentication
- Data retention (7 years for financial records)

**Claude Code Implementation:**
```bash
# SOX-Compliant Hooks Configuration

# .claude/hooks/pre-tool-use/sox-compliance.sh
#!/bin/bash
INPUT=$(cat)
TOOL=$(echo "$INPUT" | jq -r '.tool')
USER=$(echo "$INPUT" | jq -r '.user_id')

# Enforce segregation of duties
if [ "$TOOL" = "edit" ]; then
  FILE=$(echo "$INPUT" | jq -r '.inputs.file_path')

  # Trading code can't be modified by same person who approves
  if echo "$FILE" | grep -q 'trading/'; then
    USER_ROLES=$(get_user_roles.sh "$USER")

    if echo "$USER_ROLES" | grep -q 'approver'; then
      echo "SOX VIOLATION: Approvers cannot modify trading code" >&2
      log_sox_violation "$USER" "segregation_of_duties" "$FILE"
      exit 2
    fi
  fi
fi

# Log all financial data access
if echo "$INPUT" | jq -r '.inputs' | grep -qE 'portfolio|trading|account'; then
  log_financial_access "$USER" "$TOOL" "$INPUT" "sox-audit.log"
fi

exit 0
```

**Data Retention Policy:**
```json
{
  "dataRetention": {
    "financialRecords": {
      "retentionPeriodDays": 2555,
      "categories": ["portfolio_data", "trading_records", "account_statements"],
      "archiveAfterDays": 365,
      "archiveLocation": "s3://company-compliance/sox-archives/"
    },
    "auditLogs": {
      "retentionPeriodDays": 2555,
      "immutable": true,
      "encryption": "AES-256"
    }
  }
}
```

#### FINRA Compliance

**Key Requirements:**
- Electronic communications archival
- Supervision and review
- Trading surveillance
- Recordkeeping (3-6 years)
- Cybersecurity controls

**Claude Code Implementation:**
```python
# FINRA Communications Archival Hook
# .claude/hooks/session-end/finra-archival.py

import json
import boto3
from datetime import datetime

def archive_session(session_data):
    """Archive session transcript for FINRA compliance"""
    s3 = boto3.client('s3')

    # Load session transcript
    with open(session_data['transcript_path']) as f:
        transcript = json.load(f)

    # Add FINRA metadata
    finra_record = {
        "recordType": "AI_ASSISTED_COMMUNICATION",
        "timestamp": datetime.now().isoformat(),
        "userId": session_data['user_id'],
        "workspaceId": session_data['workspace_id'],
        "duration": session_data['duration'],
        "transcript": transcript,
        "classification": "BUSINESS_COMMUNICATION",
        "retentionYears": 6,
        "tags": ["claude-code", "ai-assisted", "trading-desk"]
    }

    # Upload to WORM (Write Once Read Many) compliant storage
    s3.put_object(
        Bucket='company-finra-archives',
        Key=f"claude-sessions/{datetime.now().year}/{session_data['session_id']}.json",
        Body=json.dumps(finra_record),
        ObjectLockMode='COMPLIANCE',
        ObjectLockRetainUntilDate=datetime.now() + timedelta(days=365*6),
        ServerSideEncryption='AES256',
        Metadata={
            'compliance-type': 'FINRA',
            'record-type': 'AI-COMMUNICATION',
            'user-id': session_data['user_id']
        }
    )

# Execute archival
if __name__ == "__main__":
    session_data = json.loads(input())
    archive_session(session_data)
```

#### GDPR & Data Privacy

**Key Requirements:**
- Data minimization
- Right to erasure
- Data portability
- Consent management
- Data protection by design

**Claude Code Implementation:**
```json
{
  "dataPrivacy": {
    "piiDetection": {
      "enabled": true,
      "scanTools": ["read", "edit", "webFetch"],
      "patterns": [
        "SSN: \\b\\d{3}-\\d{2}-\\d{4}\\b",
        "Email: \\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b",
        "Phone: \\b\\d{3}[-.]?\\d{3}[-.]?\\d{4}\\b",
        "Credit Card: \\b\\d{4}[- ]?\\d{4}[- ]?\\d{4}[- ]?\\d{4}\\b"
      ],
      "action": "block",
      "notifyUser": true
    },
    "rightToErasure": {
      "enabled": true,
      "automatedDeletion": true,
      "deletionRequestWorkflow": "compliance-portal"
    },
    "consentManagement": {
      "required": true,
      "consentTypes": ["data_processing", "ai_assistance", "analytics"],
      "renewalPeriodDays": 365
    }
  }
}
```

### Financial Services Use Cases

#### 1. Due Diligence & Research

**Multi-Agent Research Pipeline:**
```python
# Due diligence orchestrator
orchestrator = ClaudeOrchestrator(model="opus-4")

# Spawn specialized research agents
agents = [
    orchestrator.spawn_agent("financial-analyst", task="Analyze 10-K filings"),
    orchestrator.spawn_agent("market-researcher", task="Gather competitor data"),
    orchestrator.spawn_agent("sentiment-analyzer", task="Analyze news sentiment"),
    orchestrator.spawn_agent("technical-analyst", task="Chart pattern analysis"),
    orchestrator.spawn_agent("risk-assessor", task="Identify risk factors")
]

# Execute in parallel
results = orchestrator.execute_parallel(agents)

# Synthesize findings
report = orchestrator.synthesize(
    results,
    template="investment-memo",
    output="reports/TICKER_due_diligence.pdf"
)

# Audit trail
log_research_activity(
    session_id=orchestrator.session_id,
    agents_used=agents,
    data_sources=report.sources,
    analyst=current_user,
    compliance_tags=["SOX", "FINRA"]
)
```

#### 2. Portfolio Deep Dives

**Portfolio Validation Workflow:**
```python
# Portfolio validation engine with Claude Code
validator = PortfolioValidator()

# Validate positions against strategy criteria
validation_agents = {
    "alpha-calculator": validator.spawn("Calculate alpha vs benchmarks"),
    "risk-assessor": validator.spawn("Assess concentration & tail risk"),
    "technical-analyzer": validator.spawn("Evaluate technical signals"),
    "sentiment-analyzer": validator.spawn("Gauge market sentiment"),
    "market-data-validator": validator.spawn("Verify data accuracy")
}

# Execute validations in parallel
validations = await validator.run_parallel(validation_agents)

# Generate master trade ticket
trade_ticket = validator.synthesize(
    validations,
    decision_framework="M1_strategy",
    output="trade_tickets/YYYYMMDD_positions.json"
)

# Compliance checks
compliance_checks = [
    check_position_limits(trade_ticket),
    verify_regulatory_constraints(trade_ticket),
    validate_risk_parameters(trade_ticket)
]

if all(compliance_checks):
    trade_ticket.approve(approver=risk_manager)
    log_trade_decision(trade_ticket, audit_trail="SOX")
```

#### 3. Financial Modeling

**Monte Carlo Simulation with Audit Trails:**
```python
# Financial modeling with Claude Code
model = FinancialModel(
    scenario="portfolio_stress_test",
    model_type="monte_carlo",
    simulations=10000
)

# Claude generates and runs simulation code
result = claude.execute(
    prompt="""
    Create Monte Carlo simulation for portfolio stress testing:
    - 10,000 simulations
    - Market crash scenario (-30% to -50%)
    - Interest rate shock (+200 to +500 bps)
    - Credit spread widening (+300 to +800 bps)
    - Calculate VaR (95%, 99%), CVaR, max drawdown
    - Generate distribution charts
    """,
    tools=["edit", "bash"],
    audit_mode="comprehensive"
)

# Full audit trail captured
audit_trail = {
    "model_code": result.code_generated,
    "assumptions": result.assumptions,
    "data_sources": result.data_sources,
    "simulation_parameters": result.parameters,
    "results": result.outputs,
    "analyst": current_user,
    "reviewer": risk_manager,
    "approval_timestamp": datetime.now(),
    "compliance_tags": ["SOX", "model_risk"]
}

# Archive for regulatory inspection
archive_model(audit_trail, retention_years=7)
```

#### 4. Trading System Modernization

**Automated Trading System Development:**
```python
# Modernize legacy trading systems with Claude Code
modernization_team = [
    SubAgent("code-analyzer", "Analyze legacy COBOL/Fortran code"),
    SubAgent("architect", "Design modern microservices architecture"),
    SubAgent("implementer", "Write Python/Go services"),
    SubAgent("tester", "Create comprehensive test suite"),
    SubAgent("security-auditor", "Security scan and vulnerability assessment")
]

# Incremental migration strategy
for module in legacy_system.modules:
    # Analyze legacy code
    analysis = modernization_team[0].analyze(module)

    # Design replacement
    design = modernization_team[1].design(analysis)

    # Implement new service
    new_service = modernization_team[2].implement(design)

    # Test equivalence
    test_results = modernization_team[3].test(
        legacy_module=module,
        new_service=new_service,
        test_cases=module.test_cases
    )

    # Security review
    security_report = modernization_team[4].audit(new_service)

    if test_results.passed and security_report.no_critical_issues:
        deploy(new_service, environment="staging")
        log_migration(module, audit_trail=True)
```

### Risk Management Integration

**Portfolio Risk Dashboard Generation:**
```python
# Automated risk reporting with Claude Code
risk_dashboard = RiskDashboard()

# Parallel risk calculations
risk_metrics = await asyncio.gather(
    calculate_var(portfolio, confidence=0.95),
    calculate_cvar(portfolio, confidence=0.95),
    calculate_stress_scenarios(portfolio),
    calculate_concentration_risk(portfolio),
    calculate_liquidity_risk(portfolio),
    calculate_correlation_risk(portfolio)
)

# Claude generates executive summary
summary = claude.generate(
    prompt=f"""
    Generate executive risk summary from metrics:
    {json.dumps(risk_metrics, indent=2)}

    Include:
    - Key risk indicators with trend vs last period
    - Limit breaches and near-breaches
    - Recommended actions for risk mitigation
    - Portfolio adjustments to improve risk profile
    """,
    output_format="markdown",
    audience="executive"
)

# Audit trail for risk report
risk_report = {
    "report_date": datetime.now(),
    "portfolio_snapshot": portfolio.snapshot(),
    "risk_metrics": risk_metrics,
    "executive_summary": summary,
    "generated_by": "claude-code",
    "reviewed_by": risk_manager,
    "approval_status": "approved",
    "compliance_tags": ["SOX", "risk_management"]
}

# Distribute to stakeholders
distribute_report(risk_report, recipients=[cio, risk_committee])
archive_report(risk_report, retention_years=7)
```

---

## Portfolio Validation Engine Enterprise Deployment

### Architecture for Enterprise Scale

**Multi-Team Deployment Structure:**
```yaml
Organization: Portfolio Validation Engine Enterprise
├─ Trading Desk Workspace
│   ├─ Teams: Portfolio Managers, Traders, Analysts
│   ├─ Claude Code Users: 15
│   ├─ Sub-Agents:
│   │   ├─ alpha-calculator (Sonnet 4)
│   │   ├─ technical-analyzer (Sonnet 4)
│   │   ├─ market-data-validator (Haiku)
│   │   └─ trade-ticket-generator (Opus 4)
│   ├─ MCP Servers:
│   │   ├─ market-data-feed (Bloomberg, Reuters)
│   │   ├─ portfolio-management-system (internal)
│   │   └─ execution-management-system (internal)
│   ├─ Memory:
│   │   ├─ Trading strategy parameters
│   │   ├─ Position sizing rules
│   │   └─ Risk limits and constraints
│   └─ Budget: $10,000/month
│
├─ Risk Management Workspace
│   ├─ Teams: Risk Analysts, Quants, Compliance
│   ├─ Claude Code Users: 10
│   ├─ Sub-Agents:
│   │   ├─ risk-assessor (Sonnet 4)
│   │   ├─ stress-tester (Opus 4)
│   │   ├─ limit-monitor (Haiku)
│   │   └─ correlation-analyzer (Sonnet 4)
│   ├─ MCP Servers:
│   │   ├─ risk-system (internal)
│   │   ├─ market-data-feed (read-only)
│   │   └─ regulatory-reporting (internal)
│   ├─ Memory:
│   │   ├─ Risk models and parameters
│   │   ├─ Stress test scenarios
│   │   └─ Regulatory constraints
│   └─ Budget: $7,000/month
│
├─ Research Workspace
│   ├─ Teams: Research Analysts, Data Scientists
│   ├─ Claude Code Users: 8
│   ├─ Sub-Agents:
│   │   ├─ sentiment-analyzer (Sonnet 4)
│   │   ├─ research-aggregator (Sonnet 4)
│   │   ├─ report-generator (Opus 4)
│   │   └─ data-miner (Haiku)
│   ├─ MCP Servers:
│   │   ├─ news-feeds (Bloomberg, Reuters, internal)
│   │   ├─ research-databases (FactSet, S&P Capital IQ)
│   │   └─ social-sentiment (Twitter, Reddit)
│   ├─ Memory:
│   │   ├─ Research methodologies
│   │   ├─ Company/sector insights
│   │   └─ Analyst models
│   └─ Budget: $5,000/month
│
└─ Compliance Workspace
    ├─ Teams: Compliance Officers, Auditors, Legal
    ├─ Claude Code Users: 5
    ├─ Sub-Agents:
    │   ├─ compliance-checker (Opus 4)
    │   ├─ audit-trail-analyzer (Sonnet 4)
    │   ├─ policy-enforcer (Sonnet 4)
    │   └─ report-generator (Sonnet 4)
    ├─ MCP Servers:
    │   ├─ compliance-database (internal)
    │   ├─ regulatory-feeds (SEC, FINRA)
    │   └─ audit-log-aggregator (internal)
    ├─ Memory:
    │   ├─ Regulatory requirements
    │   ├─ Compliance policies
    │   └─ Audit procedures
    └─ Budget: $3,000/month

Total Enterprise Budget: $25,000/month
Total Claude Code Users: 38
Total Workspaces: 4
```

### Governance Controls for Financial Workflows

**Enterprise Policy Configuration:**
```json
{
  "organization": "portfolio-validation-engine",
  "policies": {
    "financialDataAccess": {
      "classification": "confidential",
      "accessControl": {
        "mode": "role-based",
        "requiredRoles": ["financial_analyst", "risk_manager", "trader"],
        "mfaRequired": true,
        "approvalRequired": {
          "actions": ["edit", "delete"],
          "approvers": ["workspace_admin", "compliance_officer"]
        }
      },
      "dataCategories": [
        "**/portfolio/**",
        "**/trading/**",
        "**/positions/**",
        "**/accounts/**"
      ]
    },
    "tradingOperations": {
      "segregationOfDuties": {
        "enabled": true,
        "rules": [
          {
            "role": "trader",
            "cannotHaveRole": "risk_approver",
            "reason": "SOX compliance: segregation of duties"
          },
          {
            "role": "developer",
            "cannotModify": "**/production/trading/**",
            "reason": "Production trading code requires separate approver"
          }
        ]
      },
      "fourEyesPrinciple": {
        "enabled": true,
        "requiredForActions": ["deploy_trading_code", "modify_risk_limits"],
        "minApprovers": 2,
        "approverRoles": ["risk_manager", "head_of_trading"]
      }
    },
    "auditAndCompliance": {
      "comprehensiveLogging": true,
      "retentionPeriodDays": 2555,
      "immutableLogs": true,
      "logCategories": [
        "all_financial_data_access",
        "trading_decisions",
        "risk_calculations",
        "position_changes",
        "model_executions"
      ],
      "realTimeMonitoring": {
        "enabled": true,
        "alertOn": ["policy_violation", "unusual_activity", "limit_breach"],
        "alertChannels": ["email", "slack", "pagerduty"]
      }
    },
    "toolRestrictions": {
      "bash": {
        "mode": "restricted",
        "allowedCommands": ["git", "pytest", "uv", "python"],
        "deniedPatterns": ["rm -rf", "dd", "curl.*production"]
      },
      "webFetch": {
        "mode": "allowlist",
        "allowedDomains": [
          "bloomberg.com",
          "reuters.com",
          "sec.gov",
          "finra.org",
          "*.company.com"
        ]
      },
      "edit": {
        "mode": "ask",
        "autoApprove": ["**/tests/**", "**/docs/**"],
        "requireReview": ["**/src/validators/**", "**/config/**"]
      }
    },
    "mcpServers": {
      "useEnterpriseMcpConfigOnly": true,
      "allowedServers": [
        "market-data-feed",
        "portfolio-management-system",
        "risk-system",
        "compliance-database",
        "github"
      ],
      "deniedServers": [
        "filesystem",
        "*-public",
        "experimental-*"
      ]
    }
  }
}
```

### Audit Trail for Investment Decisions

**Decision Audit Trail Schema:**
```json
{
  "decisionId": "dec_abc123",
  "timestamp": "2025-10-26T15:30:00Z",
  "decisionType": "POSITION_VALIDATION",
  "portfolio": "M1_STRATEGY",
  "ticker": "AAPL",
  "decision": "HOLD",
  "rationale": {
    "alphaVsBenchmark": 0.0234,
    "technicalSignals": "neutral",
    "sentimentScore": 0.65,
    "riskAssessment": "within_limits",
    "validation_results": {
      "alpha-calculator": "PASS",
      "risk-assessor": "PASS",
      "technical-analyzer": "NEUTRAL",
      "sentiment-analyzer": "PASS",
      "market-data-validator": "PASS"
    }
  },
  "validationProcess": {
    "sessionId": "ses_xyz789",
    "orchestrator": "trade-ticket-generator",
    "subagentsUsed": [
      {
        "agent": "alpha-calculator",
        "model": "claude-sonnet-4",
        "inputs": {"ticker": "AAPL", "benchmark": "SPY"},
        "outputs": {"alpha": 0.0234, "significance": 0.03},
        "duration_seconds": 8.5
      },
      {
        "agent": "risk-assessor",
        "model": "claude-sonnet-4",
        "inputs": {"ticker": "AAPL", "portfolio": "M1_STRATEGY"},
        "outputs": {"concentration": 0.15, "var_contribution": 0.08},
        "duration_seconds": 12.3
      }
    ],
    "totalDuration_seconds": 45.7,
    "totalCost_usd": 0.23
  },
  "analyst": {
    "userId": "usr_analyst_123",
    "email": "analyst@company.com",
    "role": "portfolio_manager",
    "mfaVerified": true
  },
  "approvals": [
    {
      "approver": "usr_risk_mgr_456",
      "role": "risk_manager",
      "approved": true,
      "timestamp": "2025-10-26T15:35:00Z",
      "comments": "Risk parameters acceptable"
    }
  ],
  "complianceTags": ["SOX", "FINRA", "internal_policy"],
  "dataClassification": "confidential",
  "retentionPeriodDays": 2555
}
```

**Query Decision Audit Trail:**
```python
# Search investment decisions
from claude_compliance import ComplianceAPI

compliance = ComplianceAPI(api_key=os.environ['COMPLIANCE_API_KEY'])

# Find all decisions for specific ticker
decisions = compliance.search_decisions(
    organization="portfolio-validation-engine",
    filters={
        "ticker": "AAPL",
        "date_range": ("2025-10-01", "2025-10-31"),
        "decision_type": "POSITION_VALIDATION"
    }
)

# Analyze decision patterns
for decision in decisions:
    print(f"{decision.timestamp}: {decision.decision} - {decision.rationale}")

# Generate compliance report
report = compliance.generate_report(
    decisions=decisions,
    format="PDF",
    template="regulatory_inspection",
    include_full_audit_trail=True
)

# Export for regulatory inspection
report.export("reports/AAPL_decision_history_Q4_2025.pdf")
```

### Security Patterns for Financial Data

**Data Classification & Access Control:**
```python
# .claude/hooks/pre-tool-use/financial-data-security.py

import json
import re

DATA_CLASSIFICATIONS = {
    "public": {
        "patterns": ["**/docs/**", "**/README.md"],
        "roles": ["all"]
    },
    "internal": {
        "patterns": ["**/src/**", "**/tests/**"],
        "roles": ["developer", "analyst", "trader"]
    },
    "confidential": {
        "patterns": [
            "**/portfolio/**",
            "**/positions/**",
            "**/trading/**"
        ],
        "roles": ["analyst", "trader", "portfolio_manager"],
        "mfa_required": True
    },
    "restricted": {
        "patterns": [
            "**/accounts/**",
            "**/credentials/**",
            "**/keys/**"
        ],
        "roles": ["admin", "security_officer"],
        "mfa_required": True,
        "approval_required": True
    }
}

def classify_resource(resource_path):
    """Determine data classification of resource"""
    for classification, config in DATA_CLASSIFICATIONS.items():
        for pattern in config['patterns']:
            if re.match(pattern.replace('**', '.*').replace('*', '[^/]*'), resource_path):
                return classification, config
    return "internal", DATA_CLASSIFICATIONS["internal"]

def check_access(user, classification, config):
    """Verify user has required access"""
    user_roles = get_user_roles(user)

    # Check role requirement
    if config['roles'] != ['all'] and not any(role in config['roles'] for role in user_roles):
        return False, f"Requires one of roles: {', '.join(config['roles'])}"

    # Check MFA requirement
    if config.get('mfa_required') and not is_mfa_verified(user):
        return False, "MFA verification required for this data classification"

    # Check approval requirement
    if config.get('approval_required') and not has_approval(user):
        return False, "Manager approval required for this data classification"

    return True, "Access granted"

# Main hook logic
input_data = json.loads(input())
tool = input_data['tool']
user = input_data['user_id']

# Check file access
if tool in ['read', 'edit', 'write']:
    file_path = input_data['inputs'].get('file_path', '')
    classification, config = classify_resource(file_path)

    access_allowed, reason = check_access(user, classification, config)

    if not access_allowed:
        print(f"ACCESS DENIED: {reason}", file=sys.stderr)
        print(f"Resource: {file_path}", file=sys.stderr)
        print(f"Classification: {classification}", file=sys.stderr)
        log_security_event(user, "access_denied", file_path, reason)
        sys.exit(2)

    # Log access to confidential/restricted data
    if classification in ['confidential', 'restricted']:
        log_data_access(user, classification, file_path, tool)

sys.exit(0)
```

### Scaling for Large Portfolio Management

**Performance Optimization:**
```python
# Optimize for large-scale portfolio validation

from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

class PortfolioValidator:
    def __init__(self, max_workers=10):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cache = {}

    async def validate_portfolio(self, positions):
        """Validate entire portfolio in parallel"""

        # Group positions by validation complexity
        simple_positions = [p for p in positions if p.value < 100000]
        complex_positions = [p for p in positions if p.value >= 100000]

        # Use Haiku for simple positions (fast, cheap)
        simple_futures = [
            self.executor.submit(
                self.validate_position,
                position,
                model="haiku",
                validators=["market-data-validator"]
            )
            for position in simple_positions
        ]

        # Use Sonnet for complex positions (thorough)
        complex_futures = [
            self.executor.submit(
                self.validate_position,
                position,
                model="sonnet",
                validators=["alpha-calculator", "risk-assessor",
                           "technical-analyzer", "sentiment-analyzer"]
            )
            for position in complex_positions
        ]

        # Collect results
        all_futures = simple_futures + complex_futures
        results = []

        for future in as_completed(all_futures):
            result = future.result()
            results.append(result)

            # Real-time monitoring
            if result.status == "FAIL":
                send_alert(f"Position validation failed: {result.ticker}")

        return results

    def validate_position(self, position, model, validators):
        """Validate single position"""

        # Check cache first
        cache_key = f"{position.ticker}_{position.date}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Run validators in parallel
        validation_results = {}
        for validator in validators:
            agent = self.spawn_agent(validator, model=model)
            validation_results[validator] = agent.validate(position)

        # Aggregate results
        final_result = self.aggregate_results(validation_results)

        # Cache result
        self.cache[cache_key] = final_result

        return final_result
```

**Cost Optimization:**
```python
# Cost-aware orchestration

class CostAwareOrchestrator:
    COSTS = {
        "opus-4": 0.015,    # per 1K input tokens
        "sonnet-4": 0.003,  # per 1K input tokens
        "haiku-4": 0.00025  # per 1K input tokens
    }

    def select_model(self, task_complexity, budget_remaining):
        """Choose most cost-effective model for task"""

        if budget_remaining < 1.00:
            # Low budget: use Haiku for everything
            return "haiku-4"

        if task_complexity == "high":
            # Complex task: worth using Opus
            return "opus-4"
        elif task_complexity == "medium":
            # Balanced: Sonnet is sweet spot
            return "sonnet-4"
        else:
            # Simple task: Haiku is sufficient
            return "haiku-4"

    def estimate_cost(self, task, model):
        """Estimate task cost before execution"""
        estimated_tokens = self.estimate_tokens(task)
        cost_per_1k = self.COSTS[model]
        return (estimated_tokens / 1000) * cost_per_1k

    async def execute_with_budget(self, tasks, budget_usd):
        """Execute tasks within budget constraint"""

        # Sort tasks by priority
        tasks = sorted(tasks, key=lambda t: t.priority, reverse=True)

        results = []
        spent = 0

        for task in tasks:
            # Select cost-effective model
            model = self.select_model(task.complexity, budget_usd - spent)

            # Estimate cost
            estimated_cost = self.estimate_cost(task, model)

            if spent + estimated_cost > budget_usd:
                # Out of budget: downgrade model or skip
                if model != "haiku-4":
                    model = "haiku-4"
                    estimated_cost = self.estimate_cost(task, model)

                if spent + estimated_cost > budget_usd:
                    # Still over budget: skip task
                    log_warning(f"Skipping task {task.id} due to budget constraint")
                    continue

            # Execute task
            result = await self.execute_task(task, model)
            results.append(result)

            # Update spend
            actual_cost = result.cost_usd
            spent += actual_cost

            log_usage(task.id, model, actual_cost, spent, budget_usd)

        return results, spent
```

---

## Enterprise Deployment Checklist

### Pre-Deployment

- [ ] **SSO Integration**
  - [ ] Configure IdP application (SAML/OIDC)
  - [ ] Map user attributes
  - [ ] Test SSO authentication flow
  - [ ] Enable MFA enforcement

- [ ] **User Provisioning**
  - [ ] Configure SCIM provisioning (if applicable)
  - [ ] Set up JIT provisioning
  - [ ] Define default roles and workspaces
  - [ ] Enable domain capture (if applicable)

- [ ] **Organization Structure**
  - [ ] Create workspaces for each team
  - [ ] Assign workspace admins
  - [ ] Define role hierarchy
  - [ ] Set up approval workflows

- [ ] **Policy Configuration**
  - [ ] Deploy enterprise managed policies
  - [ ] Configure tool permissions
  - [ ] Set up file access controls
  - [ ] Define MCP server allowlist

### Security Configuration

- [ ] **Network Security**
  - [ ] Configure VPC endpoints (if using Bedrock)
  - [ ] Set up PSC endpoints (if using Vertex AI)
  - [ ] Define firewall rules
  - [ ] Block personal Claude access (if required)

- [ ] **Data Protection**
  - [ ] Enable Zero Data Retention (if applicable)
  - [ ] Configure data residency
  - [ ] Set up encryption (TLS, AES-256)
  - [ ] Implement key management

- [ ] **Access Controls**
  - [ ] Configure RBAC
  - [ ] Set up MFA requirements
  - [ ] Define session timeout policies
  - [ ] Implement API key rotation schedule

### Governance Setup

- [ ] **Hooks Implementation**
  - [ ] Deploy pre-tool-use hooks
  - [ ] Deploy post-tool-use hooks
  - [ ] Configure session start/end hooks
  - [ ] Test hook execution

- [ ] **Compliance Configuration**
  - [ ] Enable comprehensive audit logging
  - [ ] Set retention periods
  - [ ] Configure SIEM integration
  - [ ] Set up Compliance API access

- [ ] **Policy Enforcement**
  - [ ] Deploy compliance checking hooks
  - [ ] Configure security validation
  - [ ] Set up quality assurance checks
  - [ ] Implement cost controls

### Monitoring & Observability

- [ ] **Dashboards**
  - [ ] Set up Grafana/Datadog dashboards
  - [ ] Configure real-time alerts
  - [ ] Create usage reports
  - [ ] Implement cost tracking

- [ ] **Audit & Compliance**
  - [ ] Configure audit log exports
  - [ ] Set up SIEM forwarding
  - [ ] Create compliance reports
  - [ ] Test data retention policies

- [ ] **Usage Analytics**
  - [ ] Enable Claude Code analytics
  - [ ] Track token usage by workspace/user
  - [ ] Monitor cost trends
  - [ ] Set budget alerts

### Knowledge Management

- [ ] **Memory Setup**
  - [ ] Create organization memory templates
  - [ ] Define project memory standards
  - [ ] Set up memory audit procedures
  - [ ] Train teams on memory best practices

- [ ] **Plugin Management**
  - [ ] Deploy enterprise plugin registry
  - [ ] Configure mandatory plugins
  - [ ] Set up plugin version control
  - [ ] Document plugin usage

### Team Onboarding

- [ ] **Documentation**
  - [ ] Create enterprise Claude Code guide
  - [ ] Document security policies
  - [ ] Provide hook examples
  - [ ] Create troubleshooting guides

- [ ] **Training**
  - [ ] Conduct admin training
  - [ ] Train developers on best practices
  - [ ] Security awareness training
  - [ ] Compliance training

- [ ] **Support**
  - [ ] Set up internal support channel
  - [ ] Define escalation procedures
  - [ ] Create FAQ documentation
  - [ ] Establish regular review meetings

### Financial Services Specific

- [ ] **Regulatory Compliance**
  - [ ] Implement SOX controls
  - [ ] Configure FINRA archival
  - [ ] Set up GDPR compliance measures
  - [ ] Define data retention policies (7 years)

- [ ] **Segregation of Duties**
  - [ ] Configure role-based restrictions
  - [ ] Implement four-eyes principle
  - [ ] Set up approval workflows
  - [ ] Test segregation enforcement

- [ ] **Audit Trails**
  - [ ] Enable comprehensive logging for financial data
  - [ ] Configure immutable log storage
  - [ ] Set up decision audit trail
  - [ ] Test audit trail completeness

### Post-Deployment

- [ ] **Testing**
  - [ ] Test SSO authentication
  - [ ] Verify policy enforcement
  - [ ] Test audit logging
  - [ ] Validate cost controls

- [ ] **Monitoring**
  - [ ] Monitor initial usage patterns
  - [ ] Review security alerts
  - [ ] Check compliance violations
  - [ ] Track costs vs budget

- [ ] **Optimization**
  - [ ] Analyze usage data
  - [ ] Optimize model selection
  - [ ] Refine policies based on feedback
  - [ ] Adjust budgets as needed

- [ ] **Review**
  - [ ] Quarterly security review
  - [ ] Quarterly compliance audit
  - [ ] Quarterly cost optimization review
  - [ ] Annual policy review

---

## Conclusion

This comprehensive guide provides enterprise-ready patterns for deploying Claude Code at scale with robust team management, security, governance, and compliance capabilities. Key takeaways:

1. **Hierarchical Configuration**: Five-tier settings precedence ensures enterprise policies are always enforced while allowing individual customization.

2. **Strong Authentication**: SSO integration with SCIM/JIT provisioning, MFA enforcement, and RBAC provide enterprise-grade access control.

3. **Governance Automation**: Hooks framework enables policy-as-code, automated compliance checking, and comprehensive audit trails.

4. **MCP Server Controls**: Allowlist-first approach (October 2025 update) provides zero-trust model for external integrations.

5. **Multi-Agent Scaling**: Hierarchical orchestration patterns enable managing hundreds of tasks with 40-60% cost savings.

6. **Knowledge Management**: Memory tools create persistent context across sessions, improving performance by 39% while reducing token usage by 84%.

7. **Comprehensive Monitoring**: Admin API, Compliance API, and SIEM integration provide real-time observability and audit capabilities.

8. **Financial Services Ready**: SOX, FINRA, GDPR compliance patterns with full audit trails for investment decisions and regulatory inspection.

9. **Portfolio Validation Engine**: Multi-workspace deployment with specialized sub-agents, governance controls, and decision audit trails transforms the engine into enterprise-ready system.

10. **Cost Optimization**: Model selection strategies, caching, and budget-aware orchestration control costs while maintaining quality.

**Next Steps:**
1. Review enterprise deployment checklist
2. Adapt configurations to your organization's specific requirements
3. Pilot with small team before organization-wide rollout
4. Establish regular review cycles for policies and usage patterns
5. Continuously optimize based on usage analytics and feedback

**Additional Resources:**
- [Claude Enterprise Documentation](https://docs.claude.com/en/docs/admin)
- [Claude Code Settings Reference](https://docs.claude.com/en/docs/claude-code/settings)
- [Admin API Reference](https://docs.claude.com/en/api/administration-api)
- [Compliance API Documentation](https://docs.claude.com/en/api/compliance)
- [MCP Security Best Practices](https://docs.claude.com/en/docs/claude-code/mcp#security)

---

**Document Version:** 1.0
**Last Updated:** 2025-10-26
**Target Audience:** Enterprise Architects, Security Teams, Compliance Officers, Engineering Leaders
**Maintained By:** Portfolio Validation Engine Team
