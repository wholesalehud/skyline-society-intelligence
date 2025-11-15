# Enterprise Claude Code Implementation Checklist

**Step-by-step guide for deploying Claude Code at enterprise scale**

---

## Phase 1: Planning & Assessment (Week 1-2)

### Business Requirements
- [ ] Identify teams that will use Claude Code
- [ ] Define use cases for each team
- [ ] Estimate user count and growth projections
- [ ] Calculate budget (premium seats + usage)
- [ ] Identify regulatory compliance requirements
- [ ] Define success metrics and KPIs

### Technical Requirements
- [ ] Review current infrastructure (network, IdP, SIEM)
- [ ] Identify data classification levels
- [ ] Document security policies to enforce
- [ ] List required integrations (MCP servers)
- [ ] Define workspace structure
- [ ] Identify pilot team for initial rollout

### Stakeholder Alignment
- [ ] Get executive sponsorship
- [ ] Align with security team on policies
- [ ] Coordinate with compliance team on requirements
- [ ] Engage IT team for infrastructure support
- [ ] Brief legal team on data handling
- [ ] Inform finance team on budget

---

## Phase 2: Environment Setup (Week 2-3)

### Enterprise Account Setup
- [ ] Upgrade to Enterprise plan
- [ ] Configure organization settings
- [ ] Set up billing and payment method
- [ ] Obtain Admin API keys
- [ ] Configure organization profile

### SSO Integration
- [ ] Choose SSO protocol (SAML 2.0 or OIDC)
- [ ] Create application in IdP
- [ ] Configure entity ID and URLs
  - [ ] Entity ID: `https://claude.ai/saml/metadata`
  - [ ] ACS URL: `https://claude.ai/saml/acs`
  - [ ] SLO URL: `https://claude.ai/saml/slo`
- [ ] Map user attributes (email, firstName, lastName)
- [ ] Upload IdP metadata to Claude
- [ ] Configure attribute mappings in Claude
- [ ] Test SSO with test user
- [ ] Enable MFA enforcement in IdP

### User Provisioning
- [ ] Choose provisioning method (SCIM, JIT, or manual)
- [ ] Configure SCIM if selected
  - [ ] Generate SCIM API token
  - [ ] Configure SCIM endpoints in IdP
  - [ ] Set up group mappings
  - [ ] Test user sync
- [ ] Enable JIT provisioning if selected
  - [ ] Configure default role assignment
  - [ ] Set default workspace
- [ ] Enable domain capture (optional)
  - [ ] Verify domain ownership
  - [ ] Configure capture settings

### Workspace Creation
- [ ] Create workspaces for each team
  - [ ] Trading Desk
  - [ ] Risk Management
  - [ ] Research
  - [ ] Compliance
  - [ ] Engineering
- [ ] Assign workspace admins
- [ ] Configure workspace settings
- [ ] Set workspace budgets

---

## Phase 3: Security Configuration (Week 3-4)

### Enterprise Policy Deployment

#### Create `managed-settings.json`
```bash
# Linux/WSL
sudo mkdir -p /etc/claude-code
sudo nano /etc/claude-code/managed-settings.json

# macOS
sudo mkdir -p "/Library/Application Support/ClaudeCode"
sudo nano "/Library/Application Support/ClaudeCode/managed-settings.json"

# Windows (as Administrator)
mkdir "C:\ProgramData\ClaudeCode"
notepad "C:\ProgramData\ClaudeCode\managed-settings.json"
```

- [ ] Define tool permissions (bash, read, edit, webFetch)
- [ ] Configure excluded paths (secrets, credentials)
- [ ] Set bypass prevention (`disableBypassPermissionsMode: true`)
- [ ] Configure audit mode (`auditMode: "comprehensive"`)
- [ ] Enable session recording
- [ ] Validate JSON syntax
- [ ] Deploy to all managed endpoints
- [ ] Test policy enforcement

#### Create `managed-mcp.json`
- [ ] List approved MCP servers
- [ ] Configure server credentials (use env vars)
- [ ] Set workspace restrictions per server
- [ ] Deploy to all managed endpoints

### MCP Server Controls
- [ ] Enable `useEnterpriseMcpConfigOnly: true`
- [ ] Create allowlist of approved servers
- [ ] Define denylist of blocked servers
- [ ] Test MCP restrictions
- [ ] Document MCP governance process

### Network Security (if applicable)
- [ ] Set up VPC endpoints for AWS Bedrock
  - [ ] Create VPC endpoint
  - [ ] Configure security groups
  - [ ] Update DNS resolution
  - [ ] Test connectivity
- [ ] Set up PSC endpoints for Google Vertex AI
  - [ ] Create forwarding rule
  - [ ] Configure private connection
  - [ ] Update network routes
  - [ ] Test connectivity
- [ ] Configure firewall rules
  - [ ] Allowlist Claude API endpoints
  - [ ] Block personal claude.ai (if required)
- [ ] Test network access

### Data Protection
- [ ] Configure data residency (US or EU)
- [ ] Enable Zero Data Retention (if applicable)
  - [ ] Review contract terms
  - [ ] Submit ZDR request
  - [ ] Verify activation
- [ ] Configure encryption settings
  - [ ] TLS 1.3 for in-transit
  - [ ] AES-256 for at-rest
- [ ] Set up key management (AWS KMS or CMK)

### Access Controls
- [ ] Configure RBAC
  - [ ] Define roles for each workspace
  - [ ] Assign roles to users
  - [ ] Test role permissions
- [ ] Set session timeout policies
- [ ] Configure concurrent session limits
- [ ] Set up device trust requirements

---

## Phase 4: Governance & Compliance (Week 4-5)

### Hooks Implementation

#### Directory Structure
```bash
mkdir -p .claude/hooks/{pre-tool-use,post-tool-use,session-start,session-end}
```

#### Pre-Tool-Use Hooks
- [ ] Create security validation hook
  - [ ] Block dangerous commands
  - [ ] Detect risky operations
  - [ ] Require approval for sensitive actions
  - [ ] Test with various commands
- [ ] Create compliance checking hook
  - [ ] Verify role-based access
  - [ ] Detect PII patterns
  - [ ] Log compliance events
  - [ ] Test with financial data
- [ ] Create cost control hook
  - [ ] Check user budget
  - [ ] Warn at 80% threshold
  - [ ] Block at 100% limit
  - [ ] Test budget enforcement

#### Post-Tool-Use Hooks
- [ ] Create audit logging hook
  - [ ] Log all tool usage
  - [ ] Include session context
  - [ ] Forward to SIEM
  - [ ] Test log generation
- [ ] Create quality verification hook
  - [ ] Run linters on code changes
  - [ ] Execute tests
  - [ ] Check for TODOs in production
  - [ ] Test quality gates

#### Session Hooks
- [ ] Create session start hook
  - [ ] Load environment
  - [ ] Verify user permissions
  - [ ] Initialize logging
- [ ] Create session end hook
  - [ ] Generate session report
  - [ ] Archive transcript
  - [ ] Cleanup temporary files
  - [ ] Update usage metrics

#### Hook Testing
- [ ] Test all hooks individually
- [ ] Test hook combinations
- [ ] Verify timeout handling (60s)
- [ ] Test error scenarios
- [ ] Verify audit trail completeness

### Compliance Configuration

#### Audit Logging
- [ ] Enable comprehensive audit logging
- [ ] Configure 30-day retention
- [ ] Set up log exports
  - [ ] JSON format for APIs
  - [ ] CSV format for analysis
- [ ] Test log generation

#### SIEM Integration
- [ ] Choose SIEM platform (Splunk, Datadog, Elastic)
- [ ] Generate SIEM API tokens
- [ ] Configure log forwarding
  - [ ] Create forwarding script
  - [ ] Set up cron job (every 5-15 minutes)
  - [ ] Test event delivery
- [ ] Configure SIEM alerts
  - [ ] Policy violations
  - [ ] Security events
  - [ ] Unusual activity

#### Compliance API
- [ ] Generate Compliance API key
- [ ] Test API endpoints
  - [ ] Get usage data
  - [ ] Get content access logs
  - [ ] Test selective deletion
- [ ] Create compliance monitoring scripts
  - [ ] Flag suspicious access patterns
  - [ ] Verify authorized access
  - [ ] Generate compliance reports
- [ ] Set up automated reporting
  - [ ] Weekly usage reports
  - [ ] Monthly compliance reports
  - [ ] Quarterly security audits

### Data Retention Policies
- [ ] Define retention periods by data type
  - [ ] Financial records: 7 years (SOX)
  - [ ] Communications: 6 years (FINRA)
  - [ ] Audit logs: 7 years
  - [ ] Session transcripts: 90 days (or per policy)
- [ ] Configure automated archival
- [ ] Set up deletion workflows
- [ ] Test retention enforcement

---

## Phase 5: Monitoring & Observability (Week 5-6)

### Admin API Integration
- [ ] Create monitoring scripts
  - [ ] Usage report script
  - [ ] Cost report script
  - [ ] Claude Code analytics script
- [ ] Set up automated data collection
  - [ ] Hourly usage checks
  - [ ] Daily cost aggregation
  - [ ] Weekly analytics reports
- [ ] Test API calls

### Dashboard Setup

#### Grafana Dashboard (or similar)
- [ ] Set up data sources
  - [ ] Admin API data
  - [ ] Audit logs
  - [ ] Cost data
- [ ] Create panels
  - [ ] Active Sessions
  - [ ] Token Usage by Workspace
  - [ ] Cost per User (Top 10)
  - [ ] Security Alerts
  - [ ] Tool Usage Distribution
  - [ ] Session Success Rate
- [ ] Configure refresh intervals
- [ ] Set up dashboard permissions

#### Alerts Configuration
- [ ] High cost alert (> $1000/user/month)
- [ ] Policy violation alert (immediate)
- [ ] Unusual activity alert (> 100 req/min)
- [ ] Budget threshold alert (80%, 100%)
- [ ] Security event alert (immediate)
- [ ] Session failure alert (< 90% success rate)
- [ ] Test all alerts

### Performance Monitoring
- [ ] Track key metrics
  - [ ] Session success rate (target > 95%)
  - [ ] Average session duration (target 15-30 min)
  - [ ] Tool call success rate (target > 98%)
  - [ ] API response time p95 (target < 500ms)
  - [ ] Cost per session (target $0.50-$2.00)
- [ ] Set up metric collection
- [ ] Create performance reports

---

## Phase 6: Knowledge Management (Week 6)

### Memory Tool Setup
- [ ] Create organization memory templates
  ```bash
  .claude/templates/
  ├── financial-project-template.md
  ├── security-project-template.md
  └── default-project-template.md
  ```
- [ ] Define memory file standards
  - [ ] Maximum 500 lines for core files
  - [ ] Required sections
  - [ ] Update frequency
- [ ] Create memory audit procedures
- [ ] Document memory best practices

### Shared Memory Files
- [ ] Create organization-wide CLAUDE.md
  - [ ] Coding standards
  - [ ] Security policies
  - [ ] Common patterns
  - [ ] Project conventions
- [ ] Create workspace-specific memory files
  - [ ] Trading: Strategy parameters, risk limits
  - [ ] Risk: Risk models, regulatory constraints
  - [ ] Research: Methodologies, data sources
  - [ ] Compliance: Policies, procedures
- [ ] Version control memory files in Git

### Plugin Management
- [ ] Create enterprise plugin registry
  ```yaml
  # .claude/plugins/registry.yaml
  ```
- [ ] Deploy mandatory plugins
  - [ ] Security scanner
  - [ ] Code standards enforcer
  - [ ] Compliance checker
- [ ] Configure team-specific plugins
  - [ ] Financial validation toolkit (trading, risk)
  - [ ] Research aggregator (research team)
- [ ] Document plugin usage
- [ ] Set up plugin version control

---

## Phase 7: Pilot Rollout (Week 7-8)

### Pilot Team Selection
- [ ] Choose pilot team (5-10 users)
- [ ] Select diverse use cases
- [ ] Identify team champions
- [ ] Set pilot success criteria

### User Onboarding
- [ ] Create onboarding documentation
  - [ ] Enterprise Claude Code guide
  - [ ] Security policies
  - [ ] Hook examples
  - [ ] Troubleshooting guide
- [ ] Conduct training sessions
  - [ ] Admin training (workspace admins)
  - [ ] Developer training (pilot users)
  - [ ] Security training (all users)
  - [ ] Compliance training (financial teams)
- [ ] Set up support channel
  - [ ] Slack channel for questions
  - [ ] Email alias for issues
  - [ ] Escalation procedures

### Pilot Execution
- [ ] Provision pilot users
- [ ] Assign to pilot workspace
- [ ] Grant appropriate roles
- [ ] Distribute onboarding materials
- [ ] Conduct kickoff meeting

### Monitoring & Feedback
- [ ] Monitor pilot usage daily
  - [ ] Session counts
  - [ ] Tool usage patterns
  - [ ] Error rates
  - [ ] Cost tracking
- [ ] Collect user feedback
  - [ ] Weekly surveys
  - [ ] Office hours Q&A
  - [ ] Feedback form
- [ ] Track issues and blockers
- [ ] Measure against success criteria

### Iteration
- [ ] Review feedback weekly
- [ ] Adjust policies based on learnings
- [ ] Refine hooks and configurations
- [ ] Update documentation
- [ ] Communicate changes to pilot team

---

## Phase 8: Organization-Wide Rollout (Week 9-12)

### Pre-Rollout Validation
- [ ] Review pilot results
- [ ] Validate all policies working correctly
- [ ] Confirm infrastructure can scale
- [ ] Get stakeholder approval for full rollout
- [ ] Finalize budget allocations

### Staged Rollout

#### Wave 1: Early Adopters (Week 9)
- [ ] Identify early adopters (20-30 users)
- [ ] Provision users and assign workspaces
- [ ] Conduct training sessions
- [ ] Monitor closely for issues
- [ ] Collect feedback

#### Wave 2: Departmental Rollout (Week 10-11)
- [ ] Rollout to full departments
  - [ ] Trading Desk
  - [ ] Risk Management
  - [ ] Research
- [ ] Conduct department-specific training
- [ ] Monitor department usage
- [ ] Address department-specific issues

#### Wave 3: Organization-Wide (Week 12)
- [ ] Open to all eligible users
- [ ] Enable self-service onboarding
- [ ] Offer regular training sessions
- [ ] Monitor organization-wide metrics

### Communication
- [ ] Announce rollout to organization
- [ ] Share success stories from pilot
- [ ] Provide training schedule
- [ ] Distribute quick start guide
- [ ] Set expectations for support

### Support Infrastructure
- [ ] Establish dedicated support team
- [ ] Create FAQ documentation
- [ ] Set up ticketing system
- [ ] Define SLAs for issue resolution
- [ ] Schedule regular office hours

---

## Phase 9: Optimization (Ongoing)

### Usage Analysis
- [ ] Weekly usage reviews
  - [ ] Usage by workspace/user
  - [ ] Tool usage patterns
  - [ ] Cost trends
  - [ ] Success rates
- [ ] Monthly deep dives
  - [ ] Cost optimization opportunities
  - [ ] Model selection analysis
  - [ ] Policy effectiveness review
- [ ] Quarterly business reviews
  - [ ] ROI analysis
  - [ ] User satisfaction surveys
  - [ ] Strategic planning

### Cost Optimization
- [ ] Identify inefficient usage patterns
- [ ] Optimize model selection
  - [ ] Review Opus usage (is it necessary?)
  - [ ] Increase Haiku usage for simple tasks
- [ ] Implement caching strategies
- [ ] Set user/workspace budgets
- [ ] Renegotiate pricing with Anthropic (at scale)

### Policy Refinement
- [ ] Review policy violation logs
- [ ] Identify false positives
- [ ] Refine hook logic
- [ ] Update allowlists/denylists
- [ ] Communicate policy changes

### Security & Compliance
- [ ] Quarterly security audits
  - [ ] Review access logs
  - [ ] Verify policy enforcement
  - [ ] Test security controls
  - [ ] Penetration testing (if applicable)
- [ ] Quarterly compliance audits
  - [ ] Review audit trails
  - [ ] Verify data retention
  - [ ] Test disaster recovery
  - [ ] Generate compliance reports
- [ ] Annual policy review
  - [ ] Update for new regulations
  - [ ] Incorporate lessons learned
  - [ ] Align with changing business needs

### Continuous Improvement
- [ ] Collect user feedback continuously
- [ ] Track feature requests
- [ ] Monitor Anthropic product updates
- [ ] Evaluate new capabilities (sub-agents, plugins, etc.)
- [ ] Pilot new features with small groups
- [ ] Iterate on configurations

---

## Phase 10: Governance & Maturity (Ongoing)

### Governance Structure
- [ ] Establish Claude Code governance committee
  - [ ] Engineering leadership
  - [ ] Security representative
  - [ ] Compliance representative
  - [ ] Business stakeholders
- [ ] Define governance processes
  - [ ] Policy approval workflow
  - [ ] MCP server approval process
  - [ ] Plugin approval process
  - [ ] Budget allocation process
- [ ] Schedule regular governance meetings
  - [ ] Monthly tactical reviews
  - [ ] Quarterly strategic planning

### Documentation Maintenance
- [ ] Assign documentation owners
- [ ] Schedule documentation reviews (quarterly)
- [ ] Keep policies up to date
- [ ] Maintain runbooks for common tasks
- [ ] Update training materials

### Knowledge Sharing
- [ ] Create internal knowledge base
- [ ] Share best practices across teams
- [ ] Highlight success stories
- [ ] Foster community of practice
- [ ] Conduct lunch-and-learn sessions

### Vendor Relationship
- [ ] Establish regular cadence with Anthropic
- [ ] Provide feedback on enterprise features
- [ ] Participate in beta programs
- [ ] Attend Anthropic events/webinars
- [ ] Stay informed on roadmap

---

## Financial Services Specific Checklist

### Regulatory Compliance

#### SOX Compliance
- [ ] Implement audit trails for financial data access
- [ ] Configure change management controls
- [ ] Enforce segregation of duties
  - [ ] Trading vs. approval roles
  - [ ] Development vs. production access
- [ ] Set 7-year data retention for financial records
- [ ] Test SOX controls
- [ ] Document compliance procedures

#### FINRA Compliance
- [ ] Configure electronic communications archival
- [ ] Set 6-year retention for communications
- [ ] Implement supervision and review workflows
- [ ] Set up trading surveillance hooks
- [ ] Configure cybersecurity controls
- [ ] Test FINRA compliance

#### GDPR Compliance (if applicable)
- [ ] Implement PII detection hooks
- [ ] Configure right to erasure workflow
- [ ] Set up consent management
- [ ] Document data flows
- [ ] Test GDPR controls

### Risk Management Integration
- [ ] Integrate with portfolio management system
- [ ] Connect to risk calculation engines
- [ ] Set up real-time position monitoring
- [ ] Configure limit breach alerts
- [ ] Implement stress testing workflows

### Audit Trail for Investment Decisions
- [ ] Design decision audit trail schema
- [ ] Implement decision logging in sub-agents
- [ ] Create decision search API
- [ ] Build decision analysis tools
- [ ] Test audit trail completeness
- [ ] Document decision review process

---

## Success Criteria

### Pilot Success (Week 8)
- [ ] 80%+ pilot users actively using Claude Code
- [ ] < 5% policy violation rate
- [ ] 90%+ session success rate
- [ ] Positive feedback from 70%+ users
- [ ] Zero security incidents
- [ ] Within budget targets

### Rollout Success (Week 12)
- [ ] 60%+ eligible users onboarded
- [ ] < 3% policy violation rate
- [ ] 95%+ session success rate
- [ ] Positive feedback from 75%+ users
- [ ] Zero compliance violations
- [ ] Within 10% of budget forecast

### 6-Month Success
- [ ] 80%+ eligible users actively using Claude Code
- [ ] Measurable productivity gains (e.g., 30% faster development)
- [ ] Positive ROI (benefits > costs)
- [ ] 85%+ user satisfaction
- [ ] Zero major security incidents
- [ ] Zero regulatory compliance violations
- [ ] Established governance processes

---

## Rollback Plan

### Trigger Conditions
- [ ] > 10 security incidents in a week
- [ ] > 5 compliance violations
- [ ] > 50% user dissatisfaction
- [ ] Costs exceed budget by > 50%
- [ ] < 70% session success rate
- [ ] Major vendor incident/outage

### Rollback Procedure
1. [ ] Pause new user provisioning
2. [ ] Notify all users of rollback
3. [ ] Archive session transcripts and audit logs
4. [ ] Disable SSO integration
5. [ ] Remove enterprise policies
6. [ ] Conduct root cause analysis
7. [ ] Develop remediation plan
8. [ ] Get stakeholder approval to retry
9. [ ] Implement fixes
10. [ ] Re-pilot with small group

---

## Key Contacts

| Role | Name | Email | Responsibilities |
|------|------|-------|------------------|
| Program Sponsor | | | Executive approval, funding |
| Technical Lead | | | Architecture, implementation |
| Security Lead | | | Policy enforcement, audits |
| Compliance Lead | | | Regulatory requirements |
| Training Lead | | | Onboarding, documentation |
| Support Lead | | | User support, issue resolution |

---

## Resources & References

- **Enterprise Scaling Guide**: [ENTERPRISE_SCALING_GUIDE.md](./ENTERPRISE_SCALING_GUIDE.md)
- **Quick Reference**: [ENTERPRISE_QUICK_REFERENCE.md](./ENTERPRISE_QUICK_REFERENCE.md)
- **Claude Docs**: https://docs.claude.com/
- **Admin API Reference**: https://docs.claude.com/en/api/administration-api
- **SSO Setup Guide**: https://support.claude.com/en/articles/9797544-setting-up-single-sign-on-sso-on-the-enterprise-plan
- **Hooks Documentation**: https://docs.claude.com/en/docs/claude-code/hooks

---

**Last Updated:** 2025-10-26
**Version:** 1.0
**Estimated Timeline:** 12 weeks for full rollout
**Recommended Team Size:** 3-5 people (Technical Lead, Security Lead, Compliance Lead, Training Lead, Support Lead)
