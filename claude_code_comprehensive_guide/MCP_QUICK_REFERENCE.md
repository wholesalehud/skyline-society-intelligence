# MCP Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### Install MCP SDK

```bash
# Using uv (recommended)
uv add "mcp[cli]"

# Using pip
pip install "mcp[cli]"
```

### Minimal MCP Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool()
def hello(name: str = "World") -> str:
    """Say hello."""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

### Test with Inspector

```bash
npx @modelcontextprotocol/inspector server.py
```

### Install in Claude Desktop

```bash
uv run mcp install server.py
```

---

## 📋 Core Concepts

| Concept | Purpose | When to Use |
|---------|---------|-------------|
| **Tools** | Actions with side effects | POST-like operations (execute trade, update portfolio) |
| **Resources** | Read-only data access | GET-like operations (fetch quotes, view holdings) |
| **Prompts** | Reusable templates | Common analysis workflows |
| **Lifespan** | Startup/shutdown | Initialize DB connections, HTTP clients |
| **Context** | Request capabilities | Access logging, progress, app resources |

---

## 🛠️ Essential Patterns

### Tool with Type Safety

```python
from pydantic import BaseModel

class RiskMetrics(BaseModel):
    volatility: float
    sharpe_ratio: float
    max_drawdown: float

@mcp.tool()
def calculate_risk(returns: list[float]) -> RiskMetrics:
    """Calculate risk metrics."""
    # Calculation logic
    return RiskMetrics(...)
```

### Lifespan Management

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan(server: FastMCP):
    # Startup
    db = await Database.connect()
    try:
        yield {"db": db}
    finally:
        # Shutdown
        await db.disconnect()

mcp = FastMCP("MyServer", lifespan=app_lifespan)
```

### Context Injection

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def my_tool(symbol: str, ctx: Context) -> dict:
    """Tool with context."""
    await ctx.info(f"Processing {symbol}")
    await ctx.report_progress(0.5, 1.0)

    # Access lifespan resources
    db = ctx.app_context["db"]

    return {"status": "complete"}
```

### Resource (Read-Only Data)

```python
@mcp.resource("portfolio://holdings/{portfolio_id}")
async def get_holdings(portfolio_id: str) -> str:
    """Fetch portfolio holdings."""
    holdings = await fetch_from_db(portfolio_id)
    return json.dumps(holdings, indent=2)
```

---

## 🔐 Security Essentials

### Input Validation

```python
from pydantic import Field, validator

class TradeRequest(BaseModel):
    symbol: str = Field(regex=r"^[A-Z]{1,5}$")
    quantity: int = Field(gt=0, le=10000)

    @validator('symbol')
    def validate_symbol(cls, v):
        if v in BLOCKED_SYMBOLS:
            raise ValueError("Invalid symbol")
        return v
```

### Rate Limiting

```python
from collections import defaultdict
from datetime import datetime

class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.rpm = requests_per_minute
        self.buckets = defaultdict(lambda: {
            "tokens": requests_per_minute,
            "last_update": datetime.now()
        })

    async def check(self, client_id: str) -> bool:
        # Token bucket implementation
        # ... (see full guide for complete code)
        pass
```

### API Key Management

```python
import os

API_KEYS = {
    "market_data": os.getenv("MARKET_DATA_API_KEY"),
    "database": os.getenv("DATABASE_API_KEY")
}

# Never hardcode keys!
```

---

## ⚡ Performance Patterns

### Caching

```python
from datetime import timedelta
import redis

cache = redis.Redis(host='localhost', port=6379)

@mcp.tool()
async def cached_tool(symbol: str) -> dict:
    cache_key = f"data:{symbol}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return json.loads(cached)

    # Fetch fresh data
    data = await fetch_data(symbol)

    # Cache for 5 minutes
    cache.setex(cache_key, timedelta(minutes=5), json.dumps(data))

    return data
```

### Retry with Backoff

```python
import asyncio
import random

async def retry_with_backoff(operation, max_attempts=3):
    for attempt in range(max_attempts):
        try:
            return await operation()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise

            delay = 2 ** attempt + random.random()  # Jitter
            await asyncio.sleep(delay)
```

### Connection Pooling

```python
import httpx

# HTTP client with connection pooling
http_client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=100,
        max_keepalive_connections=20
    ),
    timeout=30.0
)
```

---

## 🧪 Testing Patterns

### Unit Test

```python
import pytest
from mcp.server.fastmcp import Client

@pytest.fixture
def client():
    return Client(mcp_server)

@pytest.mark.asyncio
async def test_tool(client):
    async with client as c:
        result = await c.call_tool("my_tool", {"arg": "value"})
        assert result.data["status"] == "success"
```

### Integration Test

```python
@pytest.mark.asyncio
async def test_workflow():
    async with Client(mcp_server) as client:
        # Step 1
        data = await client.call_tool("fetch_data", {...})

        # Step 2
        metrics = await client.call_tool("calculate_metrics", {
            "data": data.data
        })

        # Assertions
        assert metrics.data["sharpe_ratio"] > 1.0
```

### MCP Inspector (Visual Testing)

```bash
# Launch inspector
npx @modelcontextprotocol/inspector server.py

# With environment variables
npx @modelcontextprotocol/inspector \
  -e API_KEY=test_key \
  server.py
```

---

## 📦 Configuration

### Claude Desktop Config

```json
{
  "mcpServers": {
    "my-server": {
      "command": "/path/to/.venv/bin/python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "your-key",
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### Project-Level Config (.mcp.json)

```json
{
  "mcpServers": {
    "market-data": {
      "command": "uv",
      "args": ["run", "python", "mcp_servers/market_data/server.py"],
      "env": {
        "API_KEY": "${MARKET_DATA_API_KEY}"
      }
    }
  }
}
```

---

## 🏦 Financial Application Patterns

### Alpha Calculation

```python
import numpy as np

@mcp.tool()
def calculate_alpha(
    portfolio_returns: list[float],
    benchmark_returns: list[float],
    risk_free_rate: float = 0.02
) -> dict:
    """Jensen's Alpha: α = Rp - (Rf + β × (Rm - Rf))"""

    # Calculate beta
    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance

    # Calculate alpha
    avg_portfolio = np.mean(portfolio_returns)
    avg_benchmark = np.mean(benchmark_returns)
    expected_return = risk_free_rate + beta * (avg_benchmark - risk_free_rate)
    alpha = avg_portfolio - expected_return

    return {
        "alpha": alpha,
        "beta": beta,
        "interpretation": "outperforming" if alpha > 0 else "underperforming"
    }
```

### Value at Risk (VaR)

```python
@mcp.tool()
def calculate_var(
    returns: list[float],
    confidence: float = 0.95
) -> dict:
    """Calculate Value at Risk."""
    returns_array = np.array(returns)

    # Historical VaR
    var_95 = np.percentile(returns_array, 5)
    var_99 = np.percentile(returns_array, 1)

    # Conditional VaR (Expected Shortfall)
    cvar_95 = returns_array[returns_array <= var_95].mean()

    return {
        "var_95": var_95,
        "var_99": var_99,
        "cvar_95": cvar_95
    }
```

### Sharpe Ratio

```python
@mcp.tool()
def calculate_sharpe(
    returns: list[float],
    risk_free_rate: float = 0.02
) -> float:
    """Sharpe Ratio = (Return - RiskFreeRate) / StdDev"""
    returns_array = np.array(returns)
    excess_returns = returns_array - (risk_free_rate / 252)
    sharpe = np.mean(excess_returns) / np.std(returns_array) * np.sqrt(252)
    return sharpe
```

---

## 🚨 Common Errors & Solutions

### Error: "Tool not found"

**Solution:** Ensure tool is registered with `@mcp.tool()` decorator

```python
@mcp.tool()  # Don't forget this!
def my_tool():
    pass
```

### Error: "Invalid schema"

**Solution:** Use proper type hints

```python
# Bad
@mcp.tool()
def my_tool(data):  # Missing type hint
    pass

# Good
@mcp.tool()
def my_tool(data: dict[str, float]) -> dict:
    pass
```

### Error: "Context not available"

**Solution:** Add Context parameter with type hint

```python
# Bad
@mcp.tool()
async def my_tool(ctx):  # Missing type hint
    await ctx.info("test")

# Good
from mcp.server.fastmcp import Context

@mcp.tool()
async def my_tool(ctx: Context):
    await ctx.info("test")
```

### Error: "Rate limit exceeded"

**Solution:** Implement exponential backoff

```python
async def with_retry(operation):
    for attempt in range(3):
        try:
            return await operation()
        except RateLimitError:
            await asyncio.sleep(2 ** attempt)
    raise
```

---

## 📚 Production Checklist

### Before Deployment

- [ ] Input validation with Pydantic
- [ ] Rate limiting implemented
- [ ] Caching configured
- [ ] Error handling and retries
- [ ] Logging and monitoring
- [ ] Unit and integration tests
- [ ] Security review (no hardcoded keys)
- [ ] Load testing completed
- [ ] Documentation updated

### Monitoring

- [ ] Structured JSON logging
- [ ] Request/response tracking
- [ ] Error rate monitoring
- [ ] Latency metrics (p50, p95, p99)
- [ ] Cache hit rate
- [ ] Rate limit violations
- [ ] Resource utilization (CPU, memory)

### Security

- [ ] OAuth 2.1 or API key authentication
- [ ] RBAC implemented
- [ ] mTLS for production
- [ ] Network segmentation
- [ ] Input sanitization
- [ ] Audit logging
- [ ] Secrets management (environment variables)

---

## 🔗 Quick Links

### Official Resources

- **MCP Specification**: https://modelcontextprotocol.io/specification
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector
- **Server Examples**: https://github.com/modelcontextprotocol/servers

### Financial MCP Servers

- **Financial Datasets**: https://github.com/financial-datasets/mcp-server
- **Financial Modeling Prep**: https://github.com/imbenrabi/Financial-Modeling-Prep-MCP-Server
- **Twelve Data**: https://github.com/twelvedata/mcp

### Guides & Tutorials

- **FastMCP Docs**: https://gofastmcp.com/
- **Security Best Practices**: https://collabnix.com/mcp-security-best-practices-2025/
- **Production Best Practices**: https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/

---

## 💡 Pro Tips

1. **Start Simple** - Begin with basic tools, add complexity gradually
2. **Use FastMCP** - High-level framework handles protocol details
3. **Type Everything** - Pydantic models provide validation and documentation
4. **Test with Inspector** - Visual testing accelerates development
5. **Cache Aggressively** - Multi-layer caching (in-memory + Redis)
6. **Monitor Everything** - Structured logging is essential for production
7. **Fail Gracefully** - Circuit breakers prevent cascading failures
8. **Scale Horizontally** - Stateless design enables easy scaling

---

*For detailed implementation examples, see [MCP_COMPREHENSIVE_RESEARCH.md](./MCP_COMPREHENSIVE_RESEARCH.md)*
