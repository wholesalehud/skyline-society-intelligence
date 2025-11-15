# Model Context Protocol (MCP) - Comprehensive Research & Implementation Guide

## Executive Summary

The Model Context Protocol (MCP) is an open protocol developed by Anthropic that standardizes how AI applications connect to external tools and data sources. Think of MCP as a "universal USB-C port for AI applications" - it provides a unified way to extend Claude Code and other AI systems with custom capabilities, from database access to financial data APIs.

**Key Insights for Portfolio Validation Engine:**
- MCP enables building custom tools for market data integration, risk calculations, and compliance checks
- Financial data providers (Financial Datasets, EODHD, Twelve Data, etc.) already offer production-ready MCP servers
- FastMCP framework makes Python MCP server development straightforward with lifespan management and context injection
- Production deployments require robust error handling, rate limiting, caching, and security patterns

---

## Table of Contents

1. [MCP Architecture & Core Concepts](#mcp-architecture--core-concepts)
2. [Python SDK Implementation Patterns](#python-sdk-implementation-patterns)
3. [Financial Data Integration Examples](#financial-data-integration-examples)
4. [Production Deployment & Security](#production-deployment--security)
5. [Performance & Scalability](#performance--scalability)
6. [Testing & Quality Assurance](#testing--quality-assurance)
7. [Portfolio Validation Engine Integration](#portfolio-validation-engine-integration)
8. [Code Examples & Templates](#code-examples--templates)

---

## MCP Architecture & Core Concepts

### Protocol Overview

MCP is a client-server protocol with three core primitives:

1. **Resources** - Read-only data sources (like GET requests)
2. **Tools** - Actions with side effects (like POST requests)
3. **Prompts** - Reusable interaction templates

**Key Architectural Patterns:**

```
Client (Claude Code/Agent) <-> MCP Protocol <-> Server (Your Custom Tools)
                              JSON-RPC 2.0
                         Transport: stdio/HTTP/SSE
```

### Transport Mechanisms

**Stdio (Standard Input/Output)**
- Default for local CLI tools
- Lightweight and simple
- Process-based isolation

**Streamable HTTP**
- Replaces deprecated SSE as of 2025
- Designed for web services and remote servers
- Supports session management and authentication

**HTTP/SSE (Server-Sent Events)**
- Legacy transport (still supported for backward compatibility)
- Being phased out in favor of Streamable HTTP

### Protocol Version Management

MCP follows semantic versioning with backward compatibility guarantees:
- Protocol version negotiation between client and server
- Incremental updates don't increment version if backward compatible
- Fallback mechanisms to latest supported version

**Current Specification:** 2025-06-18 (added structured data support)

---

## Python SDK Implementation Patterns

### Installation & Setup

Using `uv` (recommended):
```bash
uv init mcp-server-portfolio
cd mcp-server-portfolio
uv add "mcp[cli]"
```

Alternative with pip:
```bash
pip install "mcp[cli]"
```

### FastMCP Server Basics

FastMCP provides a high-level interface handling protocol compliance and message routing:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("PortfolioValidator")

@mcp.tool()
def calculate_portfolio_alpha(
    portfolio_returns: list[float],
    benchmark_returns: list[float],
    risk_free_rate: float = 0.02
) -> dict:
    """
    Calculate Jensen's Alpha for portfolio performance.

    Alpha = Rp - (Rf + β * (Rm - Rf))
    """
    import numpy as np

    # Calculate beta
    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance

    # Calculate expected return (CAPM)
    avg_portfolio = np.mean(portfolio_returns)
    avg_benchmark = np.mean(benchmark_returns)
    expected_return = risk_free_rate + beta * (avg_benchmark - risk_free_rate)

    # Alpha is actual return - expected return
    alpha = avg_portfolio - expected_return

    return {
        "alpha": alpha,
        "beta": beta,
        "avg_portfolio_return": avg_portfolio,
        "avg_benchmark_return": avg_benchmark,
        "interpretation": "outperforming" if alpha > 0 else "underperforming"
    }
```

### Lifespan Management

Manage application startup/shutdown with typed context:

```python
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
import aiohttp

@dataclass
class AppContext:
    """Application context with typed dependencies."""
    http_session: aiohttp.ClientSession
    db_connection: Database
    api_keys: dict[str, str]

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context."""
    # Initialize resources on startup
    http_session = aiohttp.ClientSession()
    db = await Database.connect()
    api_keys = load_api_keys_from_env()

    try:
        yield AppContext(
            http_session=http_session,
            db_connection=db,
            api_keys=api_keys
        )
    finally:
        # Cleanup on shutdown
        await http_session.close()
        await db.disconnect()

mcp = FastMCP("PortfolioValidator", lifespan=app_lifespan)
```

### Context Injection

Access server capabilities through context injection:

```python
from mcp.server.fastmcp import Context

@mcp.tool()
async def validate_portfolio_positions(
    portfolio_id: str,
    ctx: Context[AppContext]
) -> dict:
    """
    Validate portfolio positions with progress reporting.
    """
    await ctx.info(f"Starting validation for portfolio {portfolio_id}")

    # Access lifespan resources
    app_ctx = ctx.app_context

    # Report progress
    await ctx.report_progress(progress=0.2, total=1.0)

    # Fetch positions
    positions = await fetch_positions(
        portfolio_id,
        app_ctx.http_session,
        app_ctx.api_keys
    )

    await ctx.report_progress(progress=0.5, total=1.0)

    # Validate each position
    validations = []
    for i, position in enumerate(positions):
        validation = await validate_position(position, app_ctx.db_connection)
        validations.append(validation)

        progress = 0.5 + (0.5 * (i + 1) / len(positions))
        await ctx.report_progress(progress=progress, total=1.0)

    await ctx.info("Validation complete")

    return {
        "portfolio_id": portfolio_id,
        "total_positions": len(positions),
        "validations": validations,
        "status": "complete"
    }
```

### Structured Output with Pydantic

FastMCP automatically supports structured returns:

```python
from pydantic import BaseModel, Field
from typing import Literal

class RiskMetrics(BaseModel):
    """Portfolio risk assessment metrics."""
    volatility: float = Field(description="Annualized volatility (standard deviation)")
    sharpe_ratio: float = Field(description="Risk-adjusted return metric")
    max_drawdown: float = Field(description="Maximum peak-to-trough decline")
    var_95: float = Field(description="Value at Risk at 95% confidence")
    risk_rating: Literal["low", "medium", "high", "extreme"]

@mcp.tool()
def assess_portfolio_risk(
    returns: list[float],
    risk_free_rate: float = 0.02
) -> RiskMetrics:
    """
    Comprehensive portfolio risk assessment.
    """
    import numpy as np

    returns_array = np.array(returns)

    # Calculate metrics
    volatility = np.std(returns_array) * np.sqrt(252)  # Annualized
    sharpe = (np.mean(returns_array) - risk_free_rate) / np.std(returns_array)

    # Max drawdown
    cumulative = (1 + returns_array).cumprod()
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    # VaR at 95%
    var_95 = np.percentile(returns_array, 5)

    # Risk rating
    if volatility < 0.15:
        risk_rating = "low"
    elif volatility < 0.25:
        risk_rating = "medium"
    elif volatility < 0.40:
        risk_rating = "high"
    else:
        risk_rating = "extreme"

    return RiskMetrics(
        volatility=volatility,
        sharpe_ratio=sharpe,
        max_drawdown=max_drawdown,
        var_95=var_95,
        risk_rating=risk_rating
    )
```

### Resource Management

Resources expose read-only data using URI patterns:

```python
@mcp.resource("portfolio://holdings/{portfolio_id}")
async def get_portfolio_holdings(portfolio_id: str) -> str:
    """
    Retrieve current holdings for a portfolio.
    """
    holdings = await fetch_holdings(portfolio_id)
    return json.dumps(holdings, indent=2)

@mcp.resource("market-data://quote/{symbol}")
async def get_market_quote(symbol: str) -> str:
    """
    Fetch current market quote for a symbol.
    """
    quote = await fetch_quote(symbol)
    return json.dumps(quote, indent=2)

@mcp.resource("config://risk-parameters")
def get_risk_parameters() -> str:
    """
    Retrieve risk assessment configuration.
    """
    config = {
        "volatility_thresholds": {
            "low": 0.15,
            "medium": 0.25,
            "high": 0.40
        },
        "var_confidence": 0.95,
        "max_drawdown_alert": -0.20,
        "min_sharpe_ratio": 1.0
    }
    return json.dumps(config, indent=2)
```

### Prompts (Reusable Templates)

Define interaction templates:

```python
@mcp.prompt()
def portfolio_analysis_prompt(
    portfolio_id: str,
    analysis_type: str = "comprehensive"
) -> str:
    """
    Generate a portfolio analysis prompt.
    """
    templates = {
        "comprehensive": f"""
Perform a comprehensive analysis of portfolio {portfolio_id}:
1. Fetch current holdings using portfolio://holdings/{portfolio_id}
2. Calculate risk metrics (volatility, Sharpe ratio, VaR, max drawdown)
3. Assess alpha vs benchmark (SPY)
4. Identify concentration risks
5. Provide actionable recommendations
        """,
        "risk-focused": f"""
Conduct a risk-focused analysis of portfolio {portfolio_id}:
1. Assess portfolio volatility and standard deviation
2. Calculate Value at Risk (VaR) at 95% and 99% confidence
3. Evaluate maximum drawdown and recovery time
4. Identify tail risk exposures
5. Recommend risk mitigation strategies
        """,
        "performance": f"""
Evaluate performance of portfolio {portfolio_id}:
1. Calculate absolute and risk-adjusted returns
2. Compute alpha vs relevant benchmarks
3. Analyze Sharpe and Sortino ratios
4. Compare sector and factor exposures
5. Identify sources of outperformance/underperformance
        """
    }

    return templates.get(analysis_type, templates["comprehensive"])
```

### Running Your MCP Server

**Development with Inspector:**
```bash
uv run mcp dev server.py
```

**Install in Claude Desktop:**
```bash
uv run mcp install server.py
```

**Manual Configuration (Claude Desktop):**
```json
{
  "mcpServers": {
    "portfolio-validator": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "MARKET_DATA_API_KEY": "your-key",
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

---

## Financial Data Integration Examples

### Available Financial MCP Servers

Several production-ready financial MCP servers exist:

| Provider | Capabilities | Authentication |
|----------|-------------|----------------|
| **Financial Datasets** | Income statements, balance sheets, cash flow, stock prices, news | OAuth 2.1 / API Key |
| **EODHD** | Real-time & historical data, fundamentals, technical indicators | API Key |
| **Twelve Data** | Time series, real-time quotes, forex, crypto, 100+ indicators | API Key + OpenAI (for u-tool) |
| **Financial Modeling Prep** | 253+ tools across 24 categories, SEC filings, analyst ratings | API Key |
| **Alpha Vantage** | Stock quotes, technical indicators, fundamentals | API Key |

### Financial Datasets MCP Server

**Features:**
- 10 primary tools for equities and crypto
- OAuth 2.1 authentication flow
- Income statements, balance sheets, cash flow statements
- Current and historical stock/crypto prices
- Market news integration

**Configuration Example:**
```json
{
  "mcpServers": {
    "financial-datasets": {
      "command": "uvx",
      "args": ["financial-datasets-mcp"],
      "env": {
        "FINANCIAL_DATASETS_API_KEY": "your-api-key"
      }
    }
  }
}
```

**Usage Examples:**
- "What are Apple's recent income statements?"
- "Show me Tesla's current stock price"
- "Get historical prices for MSFT from 2024-01-01 to 2024-12-31"

### Financial Modeling Prep MCP Server

**Architecture Highlights:**
- Stateful session-based architecture using Smithery SDK
- Client-level caching keyed by clientId
- 253+ tools organized into 24 categories
- Dynamic tool discovery mode available

**Tool Categories:**
```python
TOOLSETS = [
    "search",           # Symbol lookup, company directories
    "company",          # Company profiles, key metrics
    "quotes",           # Live prices, market data
    "statements",       # Financial statements and ratios
    "calendar",         # Earnings calendar, IPO calendar
    "charts",           # Intraday, historical charts
    "news",             # Market news, press releases
    "analyst",          # Price targets, ratings, estimates
    "market-performance", # Sector performance, gainers/losers
    "insider-trades",   # Insider transaction tracking
    "institutional",    # Institutional holdings
    "indexes",          # Index composition and performance
    "economics",        # Economic indicators, treasury rates
    "crypto",           # Digital assets and blockchain
    "forex",            # Currency pairs
    "commodities",      # Commodities pricing
    "etf-funds",        # ETF and mutual fund data
    "esg",              # ESG ratings and scores
    "technical-indicators", # RSI, MACD, SMA, EMA, etc.
    "senate",           # Senate trading disclosures
    "sec-filings",      # 10-K, 10-Q, 8-K documents
    "earnings",         # Earnings history and surprises
    "dcf",              # Discounted cash flow models
    "bulk"              # Bulk data endpoints
]
```

**Dynamic Mode (Recommended):**
```bash
# Start with 3 meta-tools, load toolsets on-demand
DYNAMIC_TOOL_DISCOVERY=true FMP_ACCESS_TOKEN=token npm start
```

**Meta-tools:**
- `enable_toolset` - Load a toolset dynamically
- `disable_toolset` - Unload a toolset
- `get_toolset_status` - Check which toolsets are active

### Twelve Data MCP Server

**Real-time Data Streaming:**
- WebSocket integration for live data
- Historical time series retrieval
- Instrument metadata for stocks, forex, crypto
- 100+ technical indicators

**u-tool Feature:**
- AI-powered universal router
- Natural language to API endpoint mapping
- Powered by GPT-4o for parameter generation
- Requires both Twelve Data and OpenAI API keys

**Configuration:**
```json
{
  "mcpServers": {
    "twelvedata": {
      "command": "uvx",
      "args": [
        "mcp-server-twelve-data@latest",
        "-k", "TWELVE_DATA_KEY",
        "-u", "OPENAI_KEY"
      ]
    }
  }
}
```

### Building a Custom Financial MCP Server

Example structure for a portfolio validation server:

```python
from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel
import httpx
import numpy as np

mcp = FastMCP("PortfolioValidation")

# Tool 1: Fetch market data
@mcp.tool()
async def fetch_market_data(
    symbols: list[str],
    start_date: str,
    end_date: str,
    ctx: Context
) -> dict:
    """Fetch historical market data for symbols."""
    await ctx.info(f"Fetching data for {len(symbols)} symbols")

    async with httpx.AsyncClient() as client:
        data = {}
        for symbol in symbols:
            response = await client.get(
                f"https://api.example.com/v1/historical",
                params={
                    "symbol": symbol,
                    "from": start_date,
                    "to": end_date
                },
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            data[symbol] = response.json()

    return data

# Tool 2: Calculate portfolio metrics
@mcp.tool()
def calculate_portfolio_metrics(
    positions: dict[str, float],  # symbol -> weight
    returns_data: dict[str, list[float]]
) -> dict:
    """Calculate comprehensive portfolio metrics."""

    # Portfolio returns (weighted)
    symbols = list(positions.keys())
    weights = np.array([positions[s] for s in symbols])
    returns_matrix = np.array([returns_data[s] for s in symbols])

    portfolio_returns = returns_matrix.T @ weights

    # Metrics
    avg_return = np.mean(portfolio_returns)
    volatility = np.std(portfolio_returns) * np.sqrt(252)
    sharpe = avg_return / np.std(portfolio_returns)

    # Drawdown
    cumulative = (1 + portfolio_returns).cumprod()
    running_max = np.maximum.accumulate(cumulative)
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    return {
        "avg_annual_return": avg_return * 252,
        "volatility": volatility,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_drawdown,
        "current_drawdown": drawdown[-1]
    }

# Tool 3: Validate against benchmarks
@mcp.tool()
async def validate_vs_benchmark(
    portfolio_returns: list[float],
    benchmark_symbol: str = "SPY"
) -> dict:
    """Compare portfolio performance to benchmark."""

    # Fetch benchmark data
    benchmark_returns = await fetch_benchmark_returns(benchmark_symbol)

    # Calculate beta
    covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance

    # Calculate alpha (Jensen's)
    rf_rate = 0.02  # Risk-free rate
    avg_portfolio = np.mean(portfolio_returns)
    avg_benchmark = np.mean(benchmark_returns)
    expected_return = rf_rate + beta * (avg_benchmark - rf_rate)
    alpha = avg_portfolio - expected_return

    return {
        "benchmark": benchmark_symbol,
        "beta": beta,
        "alpha": alpha,
        "correlation": np.corrcoef(portfolio_returns, benchmark_returns)[0][1],
        "tracking_error": np.std(np.array(portfolio_returns) - np.array(benchmark_returns)),
        "information_ratio": alpha / np.std(np.array(portfolio_returns) - np.array(benchmark_returns))
    }

# Resource: Configuration
@mcp.resource("config://validation-parameters")
def get_validation_config() -> str:
    """Retrieve validation configuration."""
    config = {
        "risk_thresholds": {
            "max_volatility": 0.30,
            "min_sharpe": 1.0,
            "max_drawdown": -0.25
        },
        "benchmarks": ["SPY", "QQQ", "IWM"],
        "rebalance_threshold": 0.05,
        "concentration_limit": 0.20  # Max 20% in single position
    }
    return json.dumps(config, indent=2)

if __name__ == "__main__":
    mcp.run()
```

---

## Production Deployment & Security

### Authentication & Authorization

**OAuth 2.1 Implementation:**
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate and decode JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/mcp")
async def mcp_endpoint(
    request: dict,
    user_id: str = Depends(get_current_user)
):
    """MCP endpoint with authentication."""
    # Process MCP request with user context
    pass
```

**API Key Management:**
```python
import os
from typing import Optional

class APIKeyManager:
    """Secure API key management."""

    def __init__(self):
        self._keys = {}
        self._load_keys_from_env()

    def _load_keys_from_env(self):
        """Load API keys from environment variables."""
        key_prefixes = ["MARKET_DATA_", "DATABASE_", "AUTH_"]
        for key, value in os.environ.items():
            if any(key.startswith(prefix) for prefix in key_prefixes):
                self._keys[key] = value

    def get_key(self, service: str) -> Optional[str]:
        """Retrieve API key for service."""
        key_name = f"{service.upper()}_API_KEY"
        return self._keys.get(key_name)

    def rotate_key(self, service: str, new_key: str):
        """Rotate API key for service."""
        key_name = f"{service.upper()}_API_KEY"
        old_key = self._keys.get(key_name)
        self._keys[key_name] = new_key
        # Log rotation event
        logger.info(f"Rotated API key for {service}")
        return old_key
```

### Role-Based Access Control (RBAC)

```python
from enum import Enum
from typing import Set

class Role(Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    TRADER = "trader"
    ADMIN = "admin"

class Permission(Enum):
    READ_PORTFOLIO = "read:portfolio"
    WRITE_PORTFOLIO = "write:portfolio"
    EXECUTE_TRADE = "execute:trade"
    READ_MARKET_DATA = "read:market_data"
    ADMIN_ACCESS = "admin:all"

ROLE_PERMISSIONS: dict[Role, Set[Permission]] = {
    Role.VIEWER: {Permission.READ_PORTFOLIO, Permission.READ_MARKET_DATA},
    Role.ANALYST: {
        Permission.READ_PORTFOLIO,
        Permission.WRITE_PORTFOLIO,
        Permission.READ_MARKET_DATA
    },
    Role.TRADER: {
        Permission.READ_PORTFOLIO,
        Permission.WRITE_PORTFOLIO,
        Permission.EXECUTE_TRADE,
        Permission.READ_MARKET_DATA
    },
    Role.ADMIN: {
        Permission.READ_PORTFOLIO,
        Permission.WRITE_PORTFOLIO,
        Permission.EXECUTE_TRADE,
        Permission.READ_MARKET_DATA,
        Permission.ADMIN_ACCESS
    }
}

def check_permission(user_role: Role, required_permission: Permission) -> bool:
    """Check if user role has required permission."""
    return required_permission in ROLE_PERMISSIONS.get(user_role, set())

# Decorator for tool permission checking
def require_permission(permission: Permission):
    """Decorator to enforce permission checks on MCP tools."""
    def decorator(func):
        async def wrapper(*args, ctx: Context, **kwargs):
            user_role = ctx.request_context.get("user_role")
            if not check_permission(user_role, permission):
                raise PermissionError(f"Insufficient permissions: {permission.value}")
            return await func(*args, ctx=ctx, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@require_permission(Permission.EXECUTE_TRADE)
async def execute_trade(
    symbol: str,
    quantity: int,
    side: str,
    ctx: Context
) -> dict:
    """Execute trade with permission checking."""
    # Only traders and admins can execute
    pass
```

### Network Security

**mTLS (Mutual TLS) Configuration:**
```python
import ssl
from fastapi import FastAPI

def create_ssl_context():
    """Create SSL context with client certificate verification."""
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(
        certfile="/path/to/server.crt",
        keyfile="/path/to/server.key"
    )
    context.load_verify_locations(cafile="/path/to/ca.crt")
    context.verify_mode = ssl.CERT_REQUIRED
    return context

# Run with mTLS
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8443,
        ssl_context=create_ssl_context()
    )
```

**Firewall Rules & Network Segmentation:**
```yaml
# Example AWS Security Group rules
ingress_rules:
  - description: "MCP Server from Claude Code"
    protocol: tcp
    from_port: 8443
    to_port: 8443
    cidr_blocks: ["10.0.1.0/24"]  # Claude Code subnet

  - description: "Health check from ALB"
    protocol: tcp
    from_port: 8080
    to_port: 8080
    cidr_blocks: ["10.0.0.0/16"]  # Internal VPC

egress_rules:
  - description: "Market data API"
    protocol: tcp
    from_port: 443
    to_port: 443
    cidr_blocks: ["0.0.0.0/0"]
```

### Input Validation & Sanitization

```python
from pydantic import BaseModel, validator, Field
from typing import Literal

class TradeRequest(BaseModel):
    """Validated trade request."""
    symbol: str = Field(regex=r"^[A-Z]{1,5}$", description="Stock ticker (1-5 uppercase letters)")
    quantity: int = Field(gt=0, le=10000, description="Quantity (1-10,000)")
    side: Literal["buy", "sell"]
    order_type: Literal["market", "limit", "stop"]
    limit_price: Optional[float] = Field(None, gt=0)

    @validator('symbol')
    def validate_symbol(cls, v):
        """Additional symbol validation."""
        if v in ["XXX", "TEST"]:  # Blocked symbols
            raise ValueError("Invalid symbol")
        return v

    @validator('limit_price')
    def validate_limit_price(cls, v, values):
        """Validate limit price is provided for limit orders."""
        if values.get('order_type') == 'limit' and v is None:
            raise ValueError("Limit price required for limit orders")
        return v

@mcp.tool()
async def submit_trade(trade: TradeRequest) -> dict:
    """
    Submit trade with automatic validation.
    Pydantic handles all validation automatically.
    """
    # Trade is guaranteed to be valid
    pass
```

### Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta
import asyncio

class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.buckets = defaultdict(lambda: {
            "tokens": requests_per_minute,
            "last_update": datetime.now()
        })

    async def check_rate_limit(self, client_id: str) -> bool:
        """Check if request is within rate limit."""
        bucket = self.buckets[client_id]
        now = datetime.now()

        # Refill tokens
        time_passed = (now - bucket["last_update"]).total_seconds()
        tokens_to_add = (time_passed / 60.0) * self.requests_per_minute
        bucket["tokens"] = min(
            self.requests_per_minute,
            bucket["tokens"] + tokens_to_add
        )
        bucket["last_update"] = now

        # Check if tokens available
        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            return False

    async def wait_for_token(self, client_id: str):
        """Wait until token is available."""
        while not await self.check_rate_limit(client_id):
            await asyncio.sleep(0.1)

# Global rate limiter
rate_limiter = RateLimiter(requests_per_minute=30)

@mcp.tool()
async def rate_limited_tool(symbol: str, ctx: Context) -> dict:
    """Tool with rate limiting."""
    client_id = ctx.request_context.get("client_id")

    if not await rate_limiter.check_rate_limit(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Try again later.",
            headers={"Retry-After": "2"}
        )

    # Process request
    pass
```

### Monitoring & Logging

```python
import logging
import json
from datetime import datetime
from typing import Any

class StructuredLogger:
    """Structured JSON logging for MCP servers."""

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(message)s')
        )
        self.logger.addHandler(handler)

    def log_event(
        self,
        event_type: str,
        client_id: str,
        tool_name: str,
        input_params: dict,
        output: Any,
        execution_time_ms: float,
        error: Optional[str] = None
    ):
        """Log structured event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "client_id": client_id,
            "tool_name": tool_name,
            "input_params": input_params,
            "output_summary": str(output)[:100],  # Truncate
            "execution_time_ms": execution_time_ms,
            "error": error,
            "success": error is None
        }

        self.logger.info(json.dumps(event))

# Usage in tools
logger = StructuredLogger("portfolio-validation-mcp")

@mcp.tool()
async def monitored_tool(symbol: str, ctx: Context) -> dict:
    """Tool with monitoring."""
    client_id = ctx.request_context.get("client_id")
    start_time = time.time()

    try:
        result = await perform_analysis(symbol)

        execution_time = (time.time() - start_time) * 1000
        logger.log_event(
            event_type="tool_execution",
            client_id=client_id,
            tool_name="monitored_tool",
            input_params={"symbol": symbol},
            output=result,
            execution_time_ms=execution_time
        )

        return result

    except Exception as e:
        execution_time = (time.time() - start_time) * 1000
        logger.log_event(
            event_type="tool_error",
            client_id=client_id,
            tool_name="monitored_tool",
            input_params={"symbol": symbol},
            output=None,
            execution_time_ms=execution_time,
            error=str(e)
        )
        raise
```

---

## Performance & Scalability

### Multi-Layered Caching

```python
from typing import Optional, Any
import redis
import pickle
from datetime import timedelta

class CacheManager:
    """Multi-layered cache implementation."""

    def __init__(self):
        # L1: In-memory cache (fastest)
        self.l1_cache = {}
        self.l1_max_size = 1000

        # L2: Redis distributed cache
        self.l2_cache = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=False
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache (L1 -> L2 -> None)."""
        # Check L1
        if key in self.l1_cache:
            return self.l1_cache[key]

        # Check L2
        l2_value = self.l2_cache.get(key)
        if l2_value:
            value = pickle.loads(l2_value)
            # Promote to L1
            self._set_l1(key, value)
            return value

        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: int = 300
    ):
        """Set value in both cache layers."""
        # Set L1
        self._set_l1(key, value)

        # Set L2 with TTL
        self.l2_cache.setex(
            key,
            timedelta(seconds=ttl_seconds),
            pickle.dumps(value)
        )

    def _set_l1(self, key: str, value: Any):
        """Set L1 cache with size limit."""
        if len(self.l1_cache) >= self.l1_max_size:
            # Evict oldest entry (simplified LRU)
            self.l1_cache.pop(next(iter(self.l1_cache)))

        self.l1_cache[key] = value

    async def invalidate(self, key: str):
        """Invalidate cache entry."""
        self.l1_cache.pop(key, None)
        self.l2_cache.delete(key)

# Global cache manager
cache = CacheManager()

@mcp.tool()
async def cached_market_data(symbol: str) -> dict:
    """Fetch market data with caching."""
    cache_key = f"market_data:{symbol}"

    # Check cache
    cached = await cache.get(cache_key)
    if cached:
        return cached

    # Fetch fresh data
    data = await fetch_from_api(symbol)

    # Cache for 5 minutes
    await cache.set(cache_key, data, ttl_seconds=300)

    return data
```

### Connection Pooling

```python
from contextlib import asynccontextmanager
import asyncpg
from typing import AsyncIterator

class DatabasePool:
    """Connection pool for database."""

    def __init__(self, database_url: str, pool_size: int = 20):
        self.database_url = database_url
        self.pool_size = pool_size
        self.pool = None

    async def initialize(self):
        """Initialize connection pool."""
        self.pool = await asyncpg.create_pool(
            self.database_url,
            min_size=5,
            max_size=self.pool_size,
            command_timeout=60
        )

    async def close(self):
        """Close connection pool."""
        if self.pool:
            await self.pool.close()

    @asynccontextmanager
    async def acquire(self) -> AsyncIterator[asyncpg.Connection]:
        """Acquire connection from pool."""
        async with self.pool.acquire() as connection:
            yield connection

# HTTP connection pooling
import httpx

class HTTPClientPool:
    """HTTP client with connection pooling."""

    def __init__(self, max_connections: int = 100):
        self.client = httpx.AsyncClient(
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=20
            ),
            timeout=httpx.Timeout(30.0)
        )

    async def close(self):
        await self.client.aclose()

# Lifespan with pools
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Initialize connection pools."""
    db_pool = DatabasePool(DATABASE_URL)
    http_pool = HTTPClientPool()

    await db_pool.initialize()

    try:
        yield AppContext(db=db_pool, http=http_pool)
    finally:
        await db_pool.close()
        await http_pool.close()
```

### Error Handling & Retry Patterns

```python
import asyncio
import random
from typing import Callable, Any

async def retry_with_backoff(
    operation: Callable,
    max_attempts: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 30.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> Any:
    """
    Retry operation with exponential backoff and jitter.
    """
    for attempt in range(max_attempts):
        try:
            return await operation()

        except Exception as e:
            if attempt == max_attempts - 1:
                # Last attempt failed
                raise

            # Calculate delay
            delay = min(
                initial_delay * (exponential_base ** attempt),
                max_delay
            )

            # Add jitter to prevent thundering herd
            if jitter:
                delay = delay * (0.5 + random.random())

            logger.warning(
                f"Attempt {attempt + 1} failed: {e}. "
                f"Retrying in {delay:.2f}s..."
            )

            await asyncio.sleep(delay)

# Circuit breaker pattern
from enum import Enum
from datetime import datetime, timedelta

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """Circuit breaker for external service calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        timeout_seconds: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.timeout = timedelta(seconds=timeout_seconds)
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0

    async def call(self, operation: Callable) -> Any:
        """Execute operation with circuit breaker protection."""

        # Check if circuit should transition from OPEN to HALF_OPEN
        if self.state == CircuitState.OPEN:
            if datetime.now() - self.last_failure_time > self.timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
            else:
                raise CircuitBreakerError("Circuit breaker is OPEN")

        # Reject if HALF_OPEN and too many calls
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                raise CircuitBreakerError("Circuit breaker is HALF_OPEN with max calls")
            self.half_open_calls += 1

        try:
            result = await operation()

            # Success - reset if needed
            if self.state == CircuitState.HALF_OPEN:
                self.state = CircuitState.CLOSED
                self.failure_count = 0

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = datetime.now()

            # Open circuit if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

            raise

# Usage example
circuit_breaker = CircuitBreaker()

@mcp.tool()
async def resilient_api_call(symbol: str) -> dict:
    """API call with retry and circuit breaker."""

    async def operation():
        return await fetch_market_data(symbol)

    # Apply circuit breaker
    async def protected_operation():
        return await circuit_breaker.call(operation)

    # Apply retry with backoff
    return await retry_with_backoff(protected_operation)
```

### Horizontal Scaling

**Stateless Server Design:**
```python
# Store session data in Redis, not in-memory
class SessionManager:
    """Distributed session management."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Retrieve session from Redis."""
        data = self.redis.get(f"session:{session_id}")
        return json.loads(data) if data else None

    async def set_session(self, session_id: str, data: dict, ttl: int = 3600):
        """Store session in Redis with TTL."""
        self.redis.setex(
            f"session:{session_id}",
            ttl,
            json.dumps(data)
        )
```

**Load Balancer Configuration (AWS ALB):**
```yaml
# Application Load Balancer configuration
load_balancer:
  health_check:
    path: /health
    interval: 30
    timeout: 5
    healthy_threshold: 2
    unhealthy_threshold: 3

  target_group:
    protocol: HTTPS
    port: 8443
    deregistration_delay: 30

  stickiness:
    enabled: false  # Stateless design doesn't need sticky sessions
```

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portfolio-mcp-server
spec:
  replicas: 3  # Horizontal scaling
  selector:
    matchLabels:
      app: portfolio-mcp
  template:
    metadata:
      labels:
        app: portfolio-mcp
    spec:
      containers:
      - name: mcp-server
        image: portfolio-mcp:latest
        ports:
        - containerPort: 8443
        env:
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8443
          initialDelaySeconds: 5
          periodSeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: portfolio-mcp-service
spec:
  type: LoadBalancer
  selector:
    app: portfolio-mcp
  ports:
  - protocol: TCP
    port: 443
    targetPort: 8443
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: portfolio-mcp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: portfolio-mcp-server
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## Testing & Quality Assurance

### Unit Testing with Pytest

```python
import pytest
from mcp.server.fastmcp import FastMCP, Client

@pytest.fixture
def mcp_server():
    """Create test MCP server."""
    server = FastMCP("TestServer")

    @server.tool()
    def calculate_alpha(
        portfolio_return: float,
        benchmark_return: float,
        beta: float,
        risk_free_rate: float = 0.02
    ) -> float:
        """Calculate Jensen's Alpha."""
        expected_return = risk_free_rate + beta * (benchmark_return - risk_free_rate)
        return portfolio_return - expected_return

    return server

@pytest.mark.asyncio
async def test_calculate_alpha(mcp_server):
    """Test alpha calculation tool."""
    async with Client(mcp_server) as client:
        result = await client.call_tool(
            "calculate_alpha",
            {
                "portfolio_return": 0.15,
                "benchmark_return": 0.10,
                "beta": 1.5,
                "risk_free_rate": 0.02
            }
        )

        # Expected: 0.15 - (0.02 + 1.5 * (0.10 - 0.02)) = 0.01
        assert abs(result.data - 0.01) < 0.0001

@pytest.mark.asyncio
async def test_invalid_input(mcp_server):
    """Test error handling for invalid input."""
    async with Client(mcp_server) as client:
        with pytest.raises(Exception):
            await client.call_tool(
                "calculate_alpha",
                {
                    "portfolio_return": "invalid",  # Should be float
                    "benchmark_return": 0.10,
                    "beta": 1.5
                }
            )
```

### Integration Testing

```python
import pytest
import httpx
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_market_data_integration():
    """Test integration with market data API."""

    # Mock external API
    mock_response = {
        "symbol": "AAPL",
        "price": 150.25,
        "volume": 50000000
    }

    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value.json = lambda: mock_response

        # Test tool
        result = await fetch_market_data("AAPL")

        assert result["symbol"] == "AAPL"
        assert result["price"] == 150.25

@pytest.mark.asyncio
async def test_end_to_end_portfolio_validation():
    """End-to-end test of portfolio validation workflow."""

    # Setup test portfolio
    portfolio = {
        "positions": {
            "AAPL": 0.40,
            "GOOGL": 0.30,
            "MSFT": 0.30
        }
    }

    # Execute validation workflow
    async with Client(mcp_server) as client:
        # Step 1: Fetch market data
        market_data = await client.call_tool(
            "fetch_market_data",
            {"symbols": list(portfolio["positions"].keys())}
        )

        # Step 2: Calculate metrics
        metrics = await client.call_tool(
            "calculate_portfolio_metrics",
            {
                "positions": portfolio["positions"],
                "returns_data": market_data.data["returns"]
            }
        )

        # Step 3: Validate against benchmark
        validation = await client.call_tool(
            "validate_vs_benchmark",
            {
                "portfolio_returns": metrics.data["returns"],
                "benchmark_symbol": "SPY"
            }
        )

        # Assertions
        assert "alpha" in validation.data
        assert "beta" in validation.data
        assert validation.data["benchmark"] == "SPY"
```

### Validation Testing

```python
import pytest
from pydantic import ValidationError

@pytest.mark.parametrize("symbol,valid", [
    ("AAPL", True),
    ("GOOGL", True),
    ("A", True),
    ("ABCDE", True),
    ("ABC123", False),  # Contains numbers
    ("abc", False),     # Lowercase
    ("ABCDEF", False),  # Too long
    ("", False),        # Empty
])
def test_symbol_validation(symbol, valid):
    """Test symbol validation logic."""
    try:
        request = TradeRequest(
            symbol=symbol,
            quantity=100,
            side="buy",
            order_type="market"
        )
        assert valid, f"Expected {symbol} to be invalid"
    except ValidationError:
        assert not valid, f"Expected {symbol} to be valid"

@pytest.mark.parametrize("quantity,valid", [
    (1, True),
    (100, True),
    (10000, True),
    (0, False),         # Zero not allowed
    (-100, False),      # Negative not allowed
    (10001, False),     # Exceeds maximum
])
def test_quantity_validation(quantity, valid):
    """Test quantity validation logic."""
    try:
        request = TradeRequest(
            symbol="AAPL",
            quantity=quantity,
            side="buy",
            order_type="market"
        )
        assert valid, f"Expected {quantity} to be invalid"
    except ValidationError:
        assert not valid, f"Expected {quantity} to be valid"
```

### Performance Testing

```python
import pytest
import time
import asyncio

@pytest.mark.asyncio
async def test_tool_performance():
    """Test tool execution performance."""

    start_time = time.time()

    async with Client(mcp_server) as client:
        result = await client.call_tool(
            "calculate_portfolio_metrics",
            test_data
        )

    execution_time = time.time() - start_time

    # Assert performance requirements
    assert execution_time < 0.5, f"Tool took {execution_time}s, expected < 0.5s"

@pytest.mark.asyncio
async def test_concurrent_requests():
    """Test handling of concurrent requests."""

    async with Client(mcp_server) as client:
        # Execute 100 concurrent requests
        tasks = [
            client.call_tool("fetch_market_data", {"symbol": f"SYM{i}"})
            for i in range(100)
        ]

        start_time = time.time()
        results = await asyncio.gather(*tasks)
        execution_time = time.time() - start_time

        # All should succeed
        assert len(results) == 100

        # Should handle concurrency efficiently
        assert execution_time < 5.0, f"Took {execution_time}s for 100 requests"
```

### MCP Inspector Testing

**Visual Testing:**
```bash
# Launch MCP Inspector
npx @modelcontextprotocol/inspector /path/to/server.py

# Or with environment variables
npx @modelcontextprotocol/inspector \
  -e MARKET_DATA_API_KEY=test_key \
  /path/to/server.py
```

**CLI Testing:**
```bash
# List available tools
npx @modelcontextprotocol/inspector --cli /path/to/server.py \
  --method tools/list

# Call specific tool
npx @modelcontextprotocol/inspector --cli /path/to/server.py \
  --method tools/call \
  --tool-name calculate_alpha \
  --tool-args '{"portfolio_return": 0.15, "benchmark_return": 0.10, "beta": 1.5}'
```

### Continuous Integration

```yaml
# .github/workflows/mcp-server-test.yml
name: MCP Server Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:7
        ports:
          - 6379:6379

      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh

    - name: Install dependencies
      run: |
        uv sync
        uv pip install pytest pytest-asyncio pytest-cov

    - name: Run unit tests
      run: |
        uv run pytest tests/unit/ \
          --cov=src \
          --cov-report=xml \
          --cov-report=term
      env:
        DATABASE_URL: postgresql://postgres:test@localhost:5432/test
        REDIS_URL: redis://localhost:6379

    - name: Run integration tests
      run: |
        uv run pytest tests/integration/ -v
      env:
        MARKET_DATA_API_KEY: ${{ secrets.TEST_API_KEY }}

    - name: Test MCP Inspector
      run: |
        npx @modelcontextprotocol/inspector --cli server.py \
          --method tools/list > tools_list.json
        cat tools_list.json

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

---

## Portfolio Validation Engine Integration

### Custom MCP Server Architecture

```
portfolio_validation_engine/
├── mcp_servers/
│   ├── market_data_server/
│   │   ├── server.py              # Market data integration
│   │   ├── providers/
│   │   │   ├── alpha_vantage.py
│   │   │   ├── yahoo_finance.py
│   │   │   └── financial_datasets.py
│   │   └── tests/
│   │
│   ├── risk_calculator_server/
│   │   ├── server.py              # Risk metrics calculation
│   │   ├── calculators/
│   │   │   ├── alpha.py
│   │   │   ├── var.py
│   │   │   ├── sharpe.py
│   │   │   └── drawdown.py
│   │   └── tests/
│   │
│   ├── portfolio_manager_server/
│   │   ├── server.py              # Portfolio CRUD operations
│   │   ├── models.py
│   │   ├── database.py
│   │   └── tests/
│   │
│   └── compliance_server/
│       ├── server.py              # Compliance checks
│       ├── rules/
│       │   ├── concentration.py
│       │   ├── diversification.py
│       │   └── regulatory.py
│       └── tests/
│
├── .mcp.json                      # MCP server configuration
└── mcp_config_templates/
    ├── claude_desktop.json
    └── agent_sdk.json
```

### Market Data MCP Server

```python
# mcp_servers/market_data_server/server.py

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from typing import AsyncIterator
from dataclasses import dataclass
import httpx

@dataclass
class MarketDataContext:
    http_client: httpx.AsyncClient
    api_keys: dict[str, str]
    cache: CacheManager

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[MarketDataContext]:
    """Initialize market data server resources."""
    http_client = httpx.AsyncClient(timeout=30.0)
    api_keys = {
        "alpha_vantage": os.getenv("ALPHA_VANTAGE_API_KEY"),
        "financial_datasets": os.getenv("FINANCIAL_DATASETS_API_KEY")
    }
    cache = CacheManager()

    try:
        yield MarketDataContext(
            http_client=http_client,
            api_keys=api_keys,
            cache=cache
        )
    finally:
        await http_client.aclose()

mcp = FastMCP("MarketData", lifespan=lifespan)

@mcp.tool()
async def get_historical_prices(
    symbol: str,
    start_date: str,
    end_date: str,
    provider: str = "alpha_vantage",
    ctx: Context[MarketDataContext] = None
) -> dict:
    """
    Fetch historical price data for a symbol.

    Args:
        symbol: Stock ticker (e.g., 'AAPL')
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        provider: Data provider ('alpha_vantage', 'financial_datasets', 'yahoo')

    Returns:
        Dictionary with dates and OHLCV data
    """
    cache_key = f"historical:{symbol}:{start_date}:{end_date}:{provider}"

    # Check cache
    cached = await ctx.app_context.cache.get(cache_key)
    if cached:
        await ctx.info(f"Cache hit for {symbol}")
        return cached

    await ctx.info(f"Fetching {symbol} from {provider}")

    # Fetch from provider
    if provider == "alpha_vantage":
        data = await fetch_alpha_vantage(
            symbol, start_date, end_date,
            ctx.app_context.http_client,
            ctx.app_context.api_keys["alpha_vantage"]
        )
    elif provider == "financial_datasets":
        data = await fetch_financial_datasets(
            symbol, start_date, end_date,
            ctx.app_context.http_client,
            ctx.app_context.api_keys["financial_datasets"]
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")

    # Cache for 1 hour
    await ctx.app_context.cache.set(cache_key, data, ttl_seconds=3600)

    return data

@mcp.tool()
async def get_realtime_quote(
    symbol: str,
    ctx: Context[MarketDataContext] = None
) -> dict:
    """
    Get real-time quote for a symbol.

    Returns:
        Current price, bid/ask, volume, etc.
    """
    cache_key = f"quote:{symbol}"

    # Short cache (30 seconds for real-time data)
    cached = await ctx.app_context.cache.get(cache_key)
    if cached:
        return cached

    # Fetch fresh quote
    quote = await fetch_quote(
        symbol,
        ctx.app_context.http_client,
        ctx.app_context.api_keys["alpha_vantage"]
    )

    await ctx.app_context.cache.set(cache_key, quote, ttl_seconds=30)

    return quote

@mcp.resource("market-data://quote/{symbol}")
async def quote_resource(symbol: str) -> str:
    """Resource for accessing quotes."""
    quote = await get_realtime_quote(symbol)
    return json.dumps(quote, indent=2)

if __name__ == "__main__":
    mcp.run()
```

### Risk Calculator MCP Server

```python
# mcp_servers/risk_calculator_server/server.py

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from typing import Literal
import numpy as np

mcp = FastMCP("RiskCalculator")

class AlphaResult(BaseModel):
    """Jensen's Alpha calculation result."""
    alpha: float
    beta: float
    avg_portfolio_return: float
    avg_benchmark_return: float
    expected_return: float
    outperformance: Literal["outperforming", "underperforming", "neutral"]

@mcp.tool()
def calculate_jensens_alpha(
    portfolio_returns: list[float],
    benchmark_returns: list[float],
    risk_free_rate: float = 0.02
) -> AlphaResult:
    """
    Calculate Jensen's Alpha for portfolio performance.

    Formula: α = Rp - (Rf + β × (Rm - Rf))

    Args:
        portfolio_returns: List of portfolio returns
        benchmark_returns: List of benchmark returns
        risk_free_rate: Risk-free rate (default 2%)

    Returns:
        AlphaResult with alpha, beta, and interpretation
    """
    port_array = np.array(portfolio_returns)
    bench_array = np.array(benchmark_returns)

    # Calculate beta (covariance / variance)
    covariance = np.cov(port_array, bench_array)[0][1]
    benchmark_variance = np.var(bench_array)
    beta = covariance / benchmark_variance

    # Calculate average returns
    avg_portfolio = np.mean(port_array)
    avg_benchmark = np.mean(bench_array)

    # Calculate expected return using CAPM
    expected_return = risk_free_rate + beta * (avg_benchmark - risk_free_rate)

    # Alpha = Actual - Expected
    alpha = avg_portfolio - expected_return

    # Interpretation
    if alpha > 0.01:
        outperformance = "outperforming"
    elif alpha < -0.01:
        outperformance = "underperforming"
    else:
        outperformance = "neutral"

    return AlphaResult(
        alpha=alpha,
        beta=beta,
        avg_portfolio_return=avg_portfolio,
        avg_benchmark_return=avg_benchmark,
        expected_return=expected_return,
        outperformance=outperformance
    )

class VaRResult(BaseModel):
    """Value at Risk calculation result."""
    var_95: float
    var_99: float
    cvar_95: float  # Conditional VaR (Expected Shortfall)
    interpretation: str

@mcp.tool()
def calculate_value_at_risk(
    returns: list[float],
    confidence_level: float = 0.95,
    portfolio_value: float = 1000000.0
) -> VaRResult:
    """
    Calculate Value at Risk (VaR) and Conditional VaR.

    Args:
        returns: Historical returns
        confidence_level: Confidence level (0.95 or 0.99)
        portfolio_value: Portfolio value in dollars

    Returns:
        VaR and CVaR at 95% and 99% confidence
    """
    returns_array = np.array(returns)

    # Historical VaR
    var_95 = np.percentile(returns_array, 5)
    var_99 = np.percentile(returns_array, 1)

    # Conditional VaR (Expected Shortfall)
    # Average of returns below VaR threshold
    cvar_95 = returns_array[returns_array <= var_95].mean()

    # Dollar terms
    var_95_dollars = var_95 * portfolio_value
    var_99_dollars = var_99 * portfolio_value
    cvar_95_dollars = cvar_95 * portfolio_value

    interpretation = (
        f"At 95% confidence, maximum expected loss is "
        f"${abs(var_95_dollars):,.2f} (${abs(var_95)*100:.2f}%). "
        f"In worst-case scenarios (beyond 95% threshold), "
        f"average loss is ${abs(cvar_95_dollars):,.2f}."
    )

    return VaRResult(
        var_95=var_95,
        var_99=var_99,
        cvar_95=cvar_95,
        interpretation=interpretation
    )

class DrawdownResult(BaseModel):
    """Maximum drawdown analysis result."""
    max_drawdown: float
    max_drawdown_duration_days: int
    current_drawdown: float
    recovery_time_days: Optional[int]
    peak_date: str
    trough_date: str

@mcp.tool()
def calculate_maximum_drawdown(
    prices: list[float],
    dates: list[str]
) -> DrawdownResult:
    """
    Calculate maximum drawdown and recovery time.

    Args:
        prices: Historical prices
        dates: Corresponding dates

    Returns:
        Maximum drawdown metrics and analysis
    """
    prices_array = np.array(prices)

    # Calculate running maximum
    running_max = np.maximum.accumulate(prices_array)

    # Calculate drawdown series
    drawdown = (prices_array - running_max) / running_max

    # Maximum drawdown
    max_dd_idx = np.argmin(drawdown)
    max_drawdown = drawdown[max_dd_idx]

    # Find peak before max drawdown
    peak_idx = np.argmax(prices_array[:max_dd_idx + 1])

    # Drawdown duration
    duration = max_dd_idx - peak_idx

    # Recovery time (if recovered)
    recovery_idx = None
    peak_price = prices_array[peak_idx]
    for i in range(max_dd_idx, len(prices_array)):
        if prices_array[i] >= peak_price:
            recovery_idx = i
            break

    recovery_time = recovery_idx - max_dd_idx if recovery_idx else None

    # Current drawdown
    current_drawdown = drawdown[-1]

    return DrawdownResult(
        max_drawdown=max_drawdown,
        max_drawdown_duration_days=duration,
        current_drawdown=current_drawdown,
        recovery_time_days=recovery_time,
        peak_date=dates[peak_idx],
        trough_date=dates[max_dd_idx]
    )

class SharpeResult(BaseModel):
    """Sharpe ratio calculation result."""
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    rating: Literal["excellent", "good", "acceptable", "poor"]

@mcp.tool()
def calculate_risk_adjusted_returns(
    returns: list[float],
    risk_free_rate: float = 0.02,
    max_drawdown: float = None
) -> SharpeResult:
    """
    Calculate risk-adjusted return metrics.

    Args:
        returns: Historical returns
        risk_free_rate: Risk-free rate (annualized)
        max_drawdown: Maximum drawdown (if known)

    Returns:
        Sharpe, Sortino, and Calmar ratios
    """
    returns_array = np.array(returns)

    # Sharpe Ratio
    excess_returns = returns_array - (risk_free_rate / 252)  # Daily rf rate
    sharpe = np.mean(excess_returns) / np.std(returns_array) * np.sqrt(252)

    # Sortino Ratio (only downside deviation)
    downside_returns = returns_array[returns_array < 0]
    downside_std = np.std(downside_returns) if len(downside_returns) > 0 else np.std(returns_array)
    sortino = np.mean(excess_returns) / downside_std * np.sqrt(252)

    # Calmar Ratio (return / max drawdown)
    if max_drawdown is None:
        cumulative = (1 + returns_array).cumprod()
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(drawdown.min())

    annual_return = np.mean(returns_array) * 252
    calmar = annual_return / max_drawdown if max_drawdown != 0 else 0

    # Rating
    if sharpe > 2.0:
        rating = "excellent"
    elif sharpe > 1.0:
        rating = "good"
    elif sharpe > 0.5:
        rating = "acceptable"
    else:
        rating = "poor"

    return SharpeResult(
        sharpe_ratio=sharpe,
        sortino_ratio=sortino,
        calmar_ratio=calmar,
        rating=rating
    )

if __name__ == "__main__":
    mcp.run()
```

### MCP Configuration for Portfolio Validation

```json
// .mcp.json (in project root)
{
  "mcpServers": {
    "market-data": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp_servers/market_data_server",
        "python",
        "server.py"
      ],
      "env": {
        "ALPHA_VANTAGE_API_KEY": "${ALPHA_VANTAGE_API_KEY}",
        "FINANCIAL_DATASETS_API_KEY": "${FINANCIAL_DATASETS_API_KEY}"
      }
    },

    "risk-calculator": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp_servers/risk_calculator_server",
        "python",
        "server.py"
      ]
    },

    "portfolio-manager": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp_servers/portfolio_manager_server",
        "python",
        "server.py"
      ],
      "env": {
        "DATABASE_URL": "${DATABASE_URL}",
        "REDIS_URL": "${REDIS_URL}"
      }
    },

    "compliance": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/mcp_servers/compliance_server",
        "python",
        "server.py"
      ]
    }
  }
}
```

### Usage Example: Complete Portfolio Validation Workflow

```python
# Example workflow using all MCP servers

"""
Workflow: Validate a portfolio and generate recommendations

1. Fetch current portfolio holdings (portfolio-manager)
2. Get market data for all positions (market-data)
3. Calculate risk metrics (risk-calculator)
4. Calculate alpha vs benchmark (risk-calculator)
5. Run compliance checks (compliance)
6. Generate recommendations based on results
"""

# This would be executed by Claude Code Agent with access to all MCP servers

portfolio_validation_prompt = """
Please perform a comprehensive validation of portfolio 'TECH_GROWTH_001':

1. Use portfolio-manager server to fetch current holdings
2. Use market-data server to get historical prices (past 252 trading days)
3. Use risk-calculator server to calculate:
   - Jensen's Alpha vs SPY
   - Value at Risk (95% and 99%)
   - Maximum Drawdown
   - Sharpe, Sortino, and Calmar ratios
4. Use compliance server to check:
   - Concentration risk (no position > 20%)
   - Sector diversification requirements
   - Regulatory constraints
5. Provide actionable recommendations:
   - Risk assessment (low/medium/high/extreme)
   - Rebalancing suggestions if needed
   - Compliance issues to address
   - Performance improvement opportunities

Format the output as a structured report with:
- Executive Summary
- Risk Metrics Table
- Alpha Analysis
- Compliance Status
- Recommendations (prioritized)
"""
```

---

## Code Examples & Templates

### Complete MCP Server Template

```python
#!/usr/bin/env python3
"""
MCP Server Template for Financial Applications

This template provides a production-ready structure for building
MCP servers with proper error handling, caching, monitoring, and security.
"""

from mcp.server.fastmcp import FastMCP, Context
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Optional, Any
from pydantic import BaseModel, Field
import httpx
import logging
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mcp_server.log')
    ]
)
logger = logging.getLogger(__name__)

# ========== Configuration ==========

@dataclass
class AppConfig:
    """Application configuration."""
    api_key: str
    database_url: str
    redis_url: str
    cache_ttl_seconds: int = 300
    rate_limit_per_minute: int = 30
    timeout_seconds: int = 30

def load_config() -> AppConfig:
    """Load configuration from environment."""
    return AppConfig(
        api_key=os.getenv("API_KEY", ""),
        database_url=os.getenv("DATABASE_URL", ""),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
        cache_ttl_seconds=int(os.getenv("CACHE_TTL", "300")),
        rate_limit_per_minute=int(os.getenv("RATE_LIMIT", "30")),
        timeout_seconds=int(os.getenv("TIMEOUT", "30"))
    )

# ========== Application Context ==========

@dataclass
class AppContext:
    """Application context with shared resources."""
    config: AppConfig
    http_client: httpx.AsyncClient
    cache: CacheManager
    rate_limiter: RateLimiter
    db_pool: DatabasePool

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle."""
    logger.info("Starting MCP server...")

    # Load configuration
    config = load_config()

    # Initialize resources
    http_client = httpx.AsyncClient(
        timeout=config.timeout_seconds,
        limits=httpx.Limits(max_connections=100)
    )
    cache = CacheManager(redis_url=config.redis_url)
    rate_limiter = RateLimiter(requests_per_minute=config.rate_limit_per_minute)
    db_pool = DatabasePool(config.database_url)

    await db_pool.initialize()

    logger.info("MCP server started successfully")

    try:
        yield AppContext(
            config=config,
            http_client=http_client,
            cache=cache,
            rate_limiter=rate_limiter,
            db_pool=db_pool
        )
    finally:
        logger.info("Shutting down MCP server...")
        await http_client.aclose()
        await db_pool.close()
        logger.info("Shutdown complete")

# ========== Initialize MCP Server ==========

mcp = FastMCP(
    name="FinancialDataServer",
    version="1.0.0",
    lifespan=app_lifespan
)

# ========== Pydantic Models ==========

class FinancialData(BaseModel):
    """Financial data response model."""
    symbol: str = Field(description="Stock ticker symbol")
    price: float = Field(description="Current price")
    volume: int = Field(description="Trading volume")
    timestamp: str = Field(description="Data timestamp")

# ========== Tools ==========

@mcp.tool()
async def fetch_financial_data(
    symbol: str,
    ctx: Context[AppContext] = None
) -> FinancialData:
    """
    Fetch financial data for a symbol with caching and rate limiting.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        FinancialData with current price, volume, and timestamp
    """
    # Rate limiting
    client_id = ctx.request_context.get("client_id", "default")
    if not await ctx.app_context.rate_limiter.check_rate_limit(client_id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    # Check cache
    cache_key = f"financial_data:{symbol}"
    cached = await ctx.app_context.cache.get(cache_key)
    if cached:
        await ctx.info(f"Cache hit for {symbol}")
        return FinancialData(**cached)

    # Fetch from API
    await ctx.info(f"Fetching {symbol} from API")

    try:
        response = await ctx.app_context.http_client.get(
            f"https://api.example.com/quote/{symbol}",
            headers={"Authorization": f"Bearer {ctx.app_context.config.api_key}"}
        )
        response.raise_for_status()
        data = response.json()

        # Parse into model
        financial_data = FinancialData(
            symbol=data["symbol"],
            price=data["price"],
            volume=data["volume"],
            timestamp=data["timestamp"]
        )

        # Cache result
        await ctx.app_context.cache.set(
            cache_key,
            financial_data.dict(),
            ttl_seconds=ctx.app_context.config.cache_ttl_seconds
        )

        return financial_data

    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {symbol}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

# ========== Resources ==========

@mcp.resource("config://settings")
def get_configuration() -> str:
    """Retrieve server configuration."""
    config = {
        "cache_ttl_seconds": 300,
        "rate_limit_per_minute": 30,
        "timeout_seconds": 30
    }
    return json.dumps(config, indent=2)

# ========== Prompts ==========

@mcp.prompt()
def analysis_prompt(symbol: str, analysis_type: str = "comprehensive") -> str:
    """Generate an analysis prompt."""
    return f"""
Analyze {symbol} with a {analysis_type} approach:
1. Fetch current financial data
2. Calculate relevant metrics
3. Provide actionable insights
"""

# ========== Run Server ==========

if __name__ == "__main__":
    logger.info("Launching MCP server...")
    mcp.run()
```

### Testing Template

```python
# tests/test_mcp_server.py

import pytest
from mcp.server.fastmcp import Client
from server import mcp

@pytest.fixture
def mcp_client():
    """Create MCP client for testing."""
    return Client(mcp)

@pytest.mark.asyncio
async def test_fetch_financial_data(mcp_client):
    """Test financial data fetching."""
    async with mcp_client as client:
        result = await client.call_tool(
            "fetch_financial_data",
            {"symbol": "AAPL"}
        )

        assert result.data["symbol"] == "AAPL"
        assert "price" in result.data
        assert "volume" in result.data

@pytest.mark.asyncio
async def test_rate_limiting(mcp_client):
    """Test rate limiting enforcement."""
    async with mcp_client as client:
        # Make requests up to limit
        for _ in range(30):
            await client.call_tool("fetch_financial_data", {"symbol": "AAPL"})

        # Next request should fail
        with pytest.raises(Exception) as exc_info:
            await client.call_tool("fetch_financial_data", {"symbol": "AAPL"})

        assert "rate limit" in str(exc_info.value).lower()
```

---

## Best Practices Summary

### Development

1. **Use FastMCP** - High-level framework handles protocol compliance
2. **Lifespan Management** - Initialize resources on startup, cleanup on shutdown
3. **Context Injection** - Access server capabilities through Context parameter
4. **Structured Output** - Use Pydantic models for type safety and validation
5. **Proper Logging** - Structured JSON logs for production monitoring

### Security

1. **OAuth 2.1 or API Keys** - Never hardcode credentials
2. **RBAC** - Implement role-based access control
3. **Input Validation** - Use Pydantic for automatic validation
4. **Rate Limiting** - Protect against abuse
5. **mTLS** - Mutual TLS for production deployments

### Performance

1. **Multi-Layer Caching** - L1 (in-memory) + L2 (Redis) caching
2. **Connection Pooling** - Reuse database and HTTP connections
3. **Retry with Backoff** - Handle transient failures gracefully
4. **Circuit Breaker** - Prevent cascading failures
5. **Horizontal Scaling** - Stateless design for easy scaling

### Testing

1. **Unit Tests** - Test individual tools with pytest
2. **Integration Tests** - Test end-to-end workflows
3. **MCP Inspector** - Visual testing during development
4. **Performance Tests** - Validate latency requirements
5. **CI/CD** - Automated testing in GitHub Actions

---

## Additional Resources

### Official Documentation

- **MCP Specification**: https://modelcontextprotocol.io/specification
- **Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
- **MCP Inspector**: https://github.com/modelcontextprotocol/inspector
- **Server Examples**: https://github.com/modelcontextprotocol/servers

### Financial MCP Servers

- **Financial Datasets**: https://github.com/financial-datasets/mcp-server
- **Financial Modeling Prep**: https://github.com/imbenrabi/Financial-Modeling-Prep-MCP-Server
- **Twelve Data**: https://github.com/twelvedata/mcp
- **EODHD**: https://eodhd.com/financial-apis/mcp-server-for-financial-data-by-eodhd

### Community Resources

- **MCP Registry**: https://github.com/modelcontextprotocol/mcp-registry
- **MCP Servers Collection**: https://glama.ai/mcp/servers
- **LobeHub MCP Servers**: https://lobehub.com/mcp

### Tutorials & Guides

- **Building Your First MCP Server** (Rohit Paul): https://blog.rohitpaul.com/posts/2025-04-01-building-python-mcp-server/
- **Microsoft MCP for Beginners**: https://github.com/microsoft/mcp-for-beginners
- **FastMCP Documentation**: https://gofastmcp.com/

### Security & Best Practices

- **MCP Security Best Practices 2025**: https://collabnix.com/mcp-security-best-practices-2025/
- **MCP Server Security** (TrueFoundry): https://www.truefoundry.com/blog/mcp-server-security-best-practices
- **15 Best Practices for Production**: https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/

---

## Conclusion

The Model Context Protocol (MCP) represents a paradigm shift in how AI systems interact with external tools and data sources. For the Portfolio Validation Engine, MCP enables:

1. **Modular Architecture** - Separate concerns (market data, risk calculation, compliance) into discrete servers
2. **Rapid Development** - FastMCP framework makes Python server development straightforward
3. **Production-Ready** - Built-in patterns for caching, rate limiting, error handling, and monitoring
4. **Ecosystem Integration** - Leverage existing financial MCP servers (Financial Datasets, EODHD, etc.)
5. **Scalability** - Stateless design supports horizontal scaling and load balancing

**Next Steps:**

1. **Start with existing financial MCP servers** - Integrate Financial Datasets or Financial Modeling Prep for market data
2. **Build custom risk calculation server** - Implement alpha, VaR, Sharpe ratio tools
3. **Add portfolio management server** - CRUD operations for portfolios and positions
4. **Implement compliance server** - Concentration limits, diversification rules
5. **Test with MCP Inspector** - Visual testing during development
6. **Deploy to production** - Kubernetes with horizontal pod autoscaling

The comprehensive examples and templates in this guide provide a solid foundation for building production-ready MCP servers tailored to financial applications and portfolio validation workflows.

---

*Research compiled: 2025-10-26*
*Sources: Official Anthropic MCP documentation, Python SDK, community implementations, financial MCP servers*
*Next update: As new MCP features and financial integrations emerge*
