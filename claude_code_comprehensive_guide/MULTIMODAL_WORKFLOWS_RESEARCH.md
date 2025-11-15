# Multi-Modal Workflows Research: Image/PDF/Document Processing with Claude

**Research Date:** 2025-10-26
**Focus:** Portfolio Validation Engine Integration
**Sources:** Official Anthropic Documentation, Community Implementations, Production Examples

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Vision Capabilities](#vision-capabilities)
3. [PDF Processing](#pdf-processing)
4. [File Management & Batch Processing](#file-management--batch-processing)
5. [Agent Skills & Multi-Modal Integration](#agent-skills--multi-modal-integration)
6. [Financial Document Processing Patterns](#financial-document-processing-patterns)
7. [Workflow Orchestration](#workflow-orchestration)
8. [Performance Optimization](#performance-optimization)
9. [Implementation Recommendations for Portfolio Validation Engine](#implementation-recommendations-for-portfolio-validation-engine)
10. [Code Examples & Patterns](#code-examples--patterns)
11. [References & Resources](#references--resources)

---

## Executive Summary

Claude's multi-modal capabilities enable sophisticated document processing workflows combining vision, text analysis, and data extraction. Key findings for portfolio validation engine integration:

### Key Capabilities
- **Vision**: Image analysis, chart reading, OCR with 8000x8000px support (API: 5MB, claude.ai: 10MB)
- **PDF Processing**: 100-page documents up to 32MB with dual text/image analysis
- **Batch Processing**: 100,000 requests/batch at 50% cost reduction, 24-hour completion
- **Agent Skills**: Progressive disclosure architecture with built-in document skills (xlsx, pptx, pdf, docx)
- **Financial Focus**: Specialized capabilities for earnings reports, portfolio statements, technical charts

### Production Metrics
- **Norwegian Sovereign Wealth Fund**: 20% productivity gains (213,000 hours) analyzing 9,000 companies
- **AIG Underwriting**: 5x faster review timelines, 75% → 90% data accuracy improvement
- **Analyst Workflows**: 6 hours → 10 minutes for DCF models, 8 hours → 1.5 hours for quarterly earnings

### Cost Efficiency
- Batch processing: 50% discount on standard pricing
- Claude Sonnet 4.5 Batch: $1.50/MTok input, $7.50/MTok output
- Claude Haiku 4.5 Batch: $0.50/MTok input, $2.50/MTok output
- Token calculation: `(width × height) / 750` for images

---

## Vision Capabilities

### Supported Formats & Limits

**Image Formats:**
- JPEG, PNG, GIF, WebP
- API maximum: 5MB per image
- claude.ai maximum: 10MB per image
- Optimal size: ≤1.15 megapixels for performance

**Resolution Constraints:**
- Up to 20 images: 8000×8000px max
- 21-100 images: 2000×2000px max
- Minimum: 200px (smaller degrades performance)
- API: 100 images/request
- claude.ai: 20 images/turn

**Aspect Ratio Optimization:**
- 1:1 ratio: 1092×1092px (~1,590 tokens, ~$0.0048 for Sonnet 3.7)
- 3:4 ratio: 951×1268px
- 1:2 ratio: 784×1568px

### Best Practices for Chart & Graph Analysis

**Financial Chart Capabilities:**
- Technical analysis indicators (RSI, MACD, moving averages)
- Portfolio performance charts and benchmarking
- Stock price trends and volume patterns
- Financial statement visualizations
- Earnings report graphs and infographics

**Positioning & Quality:**
```markdown
**Best:** Place images before text in prompts
**Multi-image:** Label sequentially: "Image 1:", "Image 2:", etc.
**Quality:** Ensure clarity—no blur, pixelation, or illegible text
**Performance:** Resize to ≤1.15MP before upload to reduce latency
```

### OCR & Text Extraction

Claude can extract text from:
- Financial forms and regulatory documents
- Portfolio statements with tables
- Trading confirmations
- Compliance documentation
- Scanned documents (within resolution limits)

**Limitations:**
- Very small text (<200px edges) degrades performance
- Handwritten text has variable accuracy
- Not designed for medical imaging (CT/MRI)

### Critical Limitations

**Cannot Reliably:**
- Identify people by name in images
- Precise spatial reasoning (clock reading, chess positions)
- Accurate counting of large object quantities
- Detect AI-generated vs. real images

**Financial Use Case Considerations:**
- Chart analysis: Excellent for trend identification, less precise for exact values
- Table extraction: Better through PDF text layer when available
- Logo/brand recognition: Possible but not guaranteed

### Implementation Patterns

**Base64 Encoding:**
```bash
BASE64_IMAGE_DATA=$(curl -s "https://example.com/chart.jpg" | base64)
```

**API Request Structure:**
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 4096,
  "messages": [{
    "role": "user",
    "content": [
      {
        "type": "image",
        "source": {
          "type": "base64",
          "media_type": "image/jpeg",
          "data": "BASE64_IMAGE_DATA"
        }
      },
      {
        "type": "text",
        "text": "Analyze this technical chart and identify key support/resistance levels, trend direction, and momentum indicators."
      }
    ]
  }]
}
```

**URL-Based Reference:**
```json
{
  "type": "image",
  "source": {
    "type": "url",
    "url": "https://example.com/portfolio-performance.png"
  }
}
```

**Files API (Pre-Upload):**
```json
{
  "type": "image",
  "source": {
    "type": "file",
    "file_id": "file_abc123def456"
  }
}
```

---

## PDF Processing

### Upload Methods

**Three Delivery Approaches:**

1. **URL-Based** (Hosted Documents)
```json
{
  "type": "document",
  "source": {
    "type": "url",
    "url": "https://example.com/earnings-report-q4-2024.pdf"
  }
}
```

2. **Base64-Encoded** (Local Files)
```python
import base64

with open("portfolio_statement.pdf", "rb") as pdf_file:
    pdf_data = base64.b64encode(pdf_file.read()).decode('utf-8')

content = {
    "type": "document",
    "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": pdf_data
    }
}
```

3. **Files API** (Reusable References)
```json
{
  "type": "document",
  "source": {
    "type": "file",
    "file_id": "file_uploaded_earnings_report"
  }
}
```

### Size & Page Constraints

- **Maximum Size:** 32MB per request (total payload including text)
- **Page Limit:** 100 pages per PDF
- **Multi-Document:** Multiple PDFs can be included if within size limit

### Processing Architecture

**Dual Analysis System:**
- Each PDF page → converted to image (visual analysis)
- Simultaneous text extraction → structural understanding
- Combined: Understands both content AND layout

**Enables:**
- Chart interpretation within financial reports
- Table extraction with complex layouts
- Diagram analysis alongside textual context
- Visual verification of numerical data

### Cost Estimation

**Token Consumption:**
- Text-heavy pages: 1,500-3,000 tokens/page
- Image-rich pages: Additional image tokens (width × height / 750)
- Example: 3-page PDF on Amazon Bedrock ~7,000 tokens in visual mode

**Cost Calculation Example:**
```
10-page earnings report with charts:
- Text: 10 pages × 2,000 tokens = 20,000 tokens
- Images: 10 charts × 1,500 tokens = 15,000 tokens
- Total: 35,000 tokens

Using Claude Sonnet 4.5 Batch:
- Input: 35,000 × $1.50/1M = $0.0525
- Output: ~2,000 × $7.50/1M = $0.015
- Total: ~$0.07 per document
```

### Financial Document Analysis Use Cases

**Earnings Reports:**
- Revenue/profit trend extraction
- Guidance analysis
- Chart interpretation (growth rates, margins)
- Year-over-year comparisons

**Portfolio Statements:**
- Position extraction with values
- Performance metrics calculation
- Asset allocation analysis
- Transaction history review

**SEC Filings:**
- 10-K/10-Q financial table extraction
- Risk factor identification
- Management discussion analysis
- Exhibit processing

### Best Practices

**Document Preparation:**
- Use standard, legible fonts
- Ensure proper page orientation
- Reference logical page numbers (not physical)
- Split oversized documents (>100 pages or >32MB)

**Query Optimization:**
- Position PDFs before text in requests
- Enable prompt caching for repeated queries on same document
- Use specific page references when possible
- Request structured output formats (JSON, XML)

**Platform Considerations:**

| Platform | Visual PDF | Citations | Notes |
|----------|-----------|-----------|-------|
| Anthropic API | Full support | Optional | Recommended |
| Google Vertex AI | Full support | Optional | All models |
| Amazon Bedrock | Requires citations ON | Forced | Use InvokeModel API to avoid |

**Bedrock Constraint:** Must enable citations for full visual understanding; otherwise, text-only extraction occurs.

---

## File Management & Batch Processing

### Files API Overview

**Capabilities:**
- Upload files up to **500MB** (significantly larger than inline 32MB limit)
- Store once, reference by `file_id` in multiple requests
- Supported formats: PDF, DOCX, TXT, CSV, TSV, HTML, RTF, EPUB
- File lifecycle: Available for 29 days after creation

**API Endpoints:**
- `POST /v1/files` - Create/upload file
- `GET /v1/files` - List files
- `GET /v1/files/{file_id}` - Get file metadata
- `GET /v1/files/{file_id}/content` - Download file
- `DELETE /v1/files/{file_id}` - Delete file

**Upload Example:**
```python
import anthropic

client = anthropic.Anthropic(api_key="your_api_key")

# Upload file
file_response = client.beta.files.create(
    file=open("quarterly_earnings.pdf", "rb"),
    purpose="analysis"
)

file_id = file_response.id

# Use in message
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": file_id}
            },
            {
                "type": "text",
                "text": "Extract all revenue figures by segment and quarter."
            }
        ]
    }]
)
```

### Message Batches API

**Overview:**
- Process up to **100,000 requests** or **256MB** per batch
- **50% cost reduction** on all input/output tokens
- **Asynchronous processing:** Results within 24 hours (most <1 hour)
- **Higher rate limits:** Independent from standard API quotas
- **Results retention:** 29 days after completion

**General Availability:** December 17, 2024

**Pricing Comparison:**

| Model | Standard Input | Batch Input | Standard Output | Batch Output |
|-------|---------------|-------------|-----------------|--------------|
| Sonnet 4.5 | $3.00/MTok | $1.50/MTok | $15.00/MTok | $7.50/MTok |
| Haiku 4.5 | $1.00/MTok | $0.50/MTok | $5.00/MTok | $2.50/MTok |

**Batch Creation Example:**
```bash
curl https://api.anthropic.com/v1/messages/batches \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "requests": [
      {
        "custom_id": "earnings-aapl-q4-2024",
        "params": {
          "model": "claude-sonnet-4-5",
          "max_tokens": 4096,
          "messages": [{
            "role": "user",
            "content": [
              {
                "type": "document",
                "source": {
                  "type": "file",
                  "file_id": "file_aapl_earnings_q4"
                }
              },
              {
                "type": "text",
                "text": "Extract revenue, EPS, and guidance. Return as JSON."
              }
            ]
          }]
        }
      },
      {
        "custom_id": "earnings-msft-q4-2024",
        "params": {
          "model": "claude-sonnet-4-5",
          "max_tokens": 4096,
          "messages": [{
            "role": "user",
            "content": [
              {
                "type": "document",
                "source": {
                  "type": "file",
                  "file_id": "file_msft_earnings_q4"
                }
              },
              {
                "type": "text",
                "text": "Extract revenue, EPS, and guidance. Return as JSON."
              }
            ]
          }]
        }
      }
    ]
  }'
```

**Batch Status Retrieval:**
```bash
curl https://api.anthropic.com/v1/messages/batches/{batch_id} \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

**Response:**
```json
{
  "id": "batch_abc123",
  "processing_status": "ended",
  "request_counts": {
    "processing": 0,
    "succeeded": 2,
    "errored": 0,
    "canceled": 0,
    "expired": 0
  },
  "ended_at": "2025-10-26T15:30:00Z",
  "created_at": "2025-10-26T14:45:00Z",
  "results_url": "https://api.anthropic.com/v1/messages/batches/batch_abc123/results"
}
```

**Results Retrieval (JSONL Stream):**
```python
import anthropic
import json

client = anthropic.Anthropic()

# Download results
results = client.beta.messages.batches.results(batch_id="batch_abc123")

# Parse JSONL
for line in results.text.strip().split('\n'):
    result = json.loads(line)

    if result['result']['type'] == 'succeeded':
        custom_id = result['custom_id']
        message = result['result']['message']
        content = message['content'][0]['text']

        print(f"Request {custom_id}:")
        print(content)
        print("---")

    elif result['result']['type'] == 'errored':
        print(f"Error in {result['custom_id']}:")
        print(result['result']['error'])
```

**Result Types:**
- `succeeded` - Request completed successfully
- `errored` - Invalid request or processing failure
- `canceled` - Manually canceled
- `expired` - Did not complete within 24 hours

**Error Handling:**
- `invalid_request` errors: Cannot be retried without fixes
- Server errors: Retriable by resubmitting
- Expired requests: No billing, can resubmit in new batch

### Financial Document Batch Processing Use Cases

**Portfolio Analysis:**
- Analyze 100s of portfolio statements simultaneously
- Extract positions, values, performance across accounts
- Cost: 50% savings vs. real-time processing

**Earnings Season:**
- Process all S&P 500 earnings reports in 1-2 batches
- Extract key metrics, guidance, sentiment
- Compare YoY performance across all companies

**Compliance Review:**
- Batch process regulatory filings
- Identify risk factors, material changes
- Generate compliance summaries

**Historical Analysis:**
- Process years of quarterly reports
- Build time-series datasets
- Trend analysis and forecasting

**Example: Processing 500 Earnings Reports**
```
Cost Calculation:
- Average: 30 pages, 60,000 tokens per report
- Total: 500 × 60,000 = 30M tokens input
- Expected output: 2,000 tokens per report = 1M tokens

Standard API:
- Input: 30M × $3.00/M = $90
- Output: 1M × $15.00/M = $15
- Total: $105

Batch API (50% discount):
- Input: 30M × $1.50/M = $45
- Output: 1M × $7.50/M = $7.50
- Total: $52.50
- Savings: $52.50 (50%)
```

---

## Agent Skills & Multi-Modal Integration

### Skills Architecture Overview

**Progressive Disclosure Pattern:**

```
Skill Loading Stages:
1. Metadata (always loaded): ~100 tokens
   - name, description, version
   - Enables discovery in system prompt

2. Instructions (on-demand): ~5,000 tokens max
   - SKILL.md body loads when relevant
   - Provides implementation guidance

3. Resources (as-needed): 0 context tokens
   - Scripts execute via bash
   - Only output enters context
   - Reference files load individually
```

**Directory Structure:**
```
skill_name/
├── SKILL.md                 # Main instructions for Claude
├── scripts/
│   ├── extract_data.py      # Data extraction utilities
│   ├── generate_chart.py    # Visualization generation
│   └── validate_output.py   # Quality assurance
└── resources/
    ├── templates/
    │   ├── earnings_schema.json
    │   └── portfolio_template.xlsx
    └── data/
        ├── ticker_mappings.csv
        └── sector_classifications.json
```

### Built-In Document Processing Skills

| Skill | Command | Capabilities | Multi-Modal Support |
|-------|---------|-------------|-------------------|
| **Excel** | `xlsx` | Create/manipulate workbooks, formulas, charts, formatting | Import data from PDFs/images |
| **PowerPoint** | `pptx` | Generate presentations, slides, charts, transitions | Include images, charts from analysis |
| **PDF** | `pdf` | Create formatted PDFs with text, tables, images | Combine text + visualizations |
| **Word** | `docx` | Generate documents with rich formatting, tracked changes | Insert images, tables from data |

**Required Beta Headers:**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    betas=[
        "code-execution-2025-08-25",    # Enable code execution
        "files-api-2025-04-14",          # Enable file operations
        "skills-2025-10-02"              # Activate Skills feature
    ],
    messages=[{
        "role": "user",
        "content": "Use the xlsx skill to create a portfolio summary from this PDF statement."
    }]
)
```

### Custom Skill Creation for Financial Workflows

**Example: Portfolio Statement Analyzer Skill**

**File: `portfolio_analyzer/SKILL.md`**
```markdown
---
name: portfolio_analyzer
description: Extracts positions, values, and performance metrics from broker portfolio statements (PDF, CSV, or images). Validates data accuracy and generates structured output.
version: 1.0.0
---

# Portfolio Statement Analyzer

## Overview
This skill analyzes broker portfolio statements to extract:
- Individual positions (ticker, quantity, cost basis, current value)
- Account-level metrics (total value, cash, margin)
- Performance calculations (returns, gains/losses)
- Asset allocation breakdowns

## Supported Input Formats
- PDF broker statements (Schwab, Fidelity, Interactive Brokers, E*TRADE)
- CSV exports from trading platforms
- Screenshots of portfolio pages

## Output Format
Returns JSON with validated data:

```json
{
  "account_id": "ABC123",
  "statement_date": "2024-10-26",
  "total_value": 125430.50,
  "cash": 5430.50,
  "positions": [
    {
      "ticker": "AAPL",
      "quantity": 100,
      "cost_basis": 15000.00,
      "current_value": 18500.00,
      "gain_loss": 3500.00,
      "gain_loss_pct": 23.33
    }
  ],
  "asset_allocation": {
    "equities": 0.75,
    "fixed_income": 0.15,
    "cash": 0.10
  }
}
```

## Usage

### For PDF Statements
```
Analyze the attached portfolio statement PDF and extract all positions with current values.
```

### For CSV Data
```
Parse this CSV export and calculate total portfolio value and asset allocation.
```

### For Screenshots
```
Extract position data from this portfolio screenshot.
```

## Validation Rules
- Verify ticker symbols against known exchanges
- Ensure numerical values are reasonable (no negative quantities)
- Cross-check totals against sum of positions
- Flag discrepancies in calculated vs. stated values

## Advanced Features
- Multi-account consolidation
- Historical comparison (if multiple statements provided)
- Tax lot analysis
- Dividend tracking

## Scripts
Run `/scripts/validate_tickers.py` to verify ticker symbols.
Run `/scripts/calculate_metrics.py` to compute derived values.
See `/resources/broker_templates/` for format-specific parsing.
```

**File: `portfolio_analyzer/scripts/validate_tickers.py`**
```python
#!/usr/bin/env python3
import sys
import json

# Known ticker validation (simplified - use real API in production)
VALID_EXCHANGES = {
    "NYSE": ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"],
    "NASDAQ": ["NVDA", "META", "NFLX", "AMD", "INTC"],
    # ... expand with real data source
}

def validate_ticker(ticker):
    """Validate ticker symbol against known exchanges"""
    ticker = ticker.upper().strip()

    for exchange, tickers in VALID_EXCHANGES.items():
        if ticker in tickers:
            return {"valid": True, "exchange": exchange, "ticker": ticker}

    # If not found, flag for manual review
    return {"valid": False, "ticker": ticker, "reason": "Unknown ticker"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No ticker provided"}))
        sys.exit(1)

    ticker = sys.argv[1]
    result = validate_ticker(ticker)
    print(json.dumps(result))
```

**File: `portfolio_analyzer/resources/broker_templates/schwab_statement.json`**
```json
{
  "format": "schwab_pdf",
  "version": "2024",
  "extraction_rules": {
    "account_number": {
      "pattern": "Account Number:\\s*(\\d{4}-\\d{4})",
      "page": 1
    },
    "statement_date": {
      "pattern": "Statement Period Ending\\s*(\\d{2}/\\d{2}/\\d{4})",
      "page": 1
    },
    "positions_table": {
      "start_marker": "Symbol & Description",
      "columns": ["symbol", "description", "quantity", "price", "value"],
      "end_marker": "Total Market Value"
    }
  }
}
```

### Multi-Modal Skill Integration Patterns

**Pattern 1: Document → Data → Visualization**
```python
# User uploads PDF earnings report
# Claude uses pdf skill to extract text/images
# Uses xlsx skill to create data analysis
# Uses pptx skill to generate presentation

message = client.messages.create(
    model="claude-sonnet-4-5",
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    max_tokens=8192,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": "earnings_q4_2024"}
            },
            {
                "type": "text",
                "text": """
                1. Extract revenue, EPS, and key metrics from this earnings report
                2. Create Excel analysis with YoY comparisons and charts
                3. Generate PowerPoint summary for executive review
                """
            }
        ]
    }]
)
```

**Pattern 2: Multi-Document Analysis**
```python
# Process multiple broker statements
# Consolidate positions across accounts
# Generate unified portfolio report

message = client.messages.create(
    model="claude-sonnet-4-5",
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    max_tokens=8192,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": "schwab_statement_oct"}
            },
            {
                "type": "document",
                "source": {"type": "file", "file_id": "fidelity_statement_oct"}
            },
            {
                "type": "document",
                "source": {"type": "file", "file_id": "ib_statement_oct"}
            },
            {
                "type": "text",
                "text": """
                Analyze these three portfolio statements and:
                1. Extract all positions from each account
                2. Consolidate into single portfolio view
                3. Calculate total asset allocation
                4. Generate Excel report with individual + consolidated views
                """
            }
        ]
    }]
)
```

**Pattern 3: Visual Verification Workflow**
```python
# Extract data from PDF
# Generate visualization
# Create screenshot for verification
# Iteratively refine based on visual feedback

message = client.messages.create(
    model="claude-sonnet-4-5",
    betas=["code-execution-2025-08-25", "files-api-2025-04-14", "skills-2025-10-02"],
    max_tokens=8192,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": "portfolio_performance"}
            },
            {
                "type": "text",
                "text": """
                Create a portfolio performance dashboard:
                1. Extract monthly returns from the PDF
                2. Generate matplotlib chart with:
                   - Monthly return bars
                   - Cumulative return line
                   - Benchmark comparison (SPY)
                3. Save as PNG and show me the result
                4. I'll provide feedback for refinements
                """
            }
        ]
    }]
)

# Claude generates chart, returns file_id for PNG
# User views chart, provides feedback
# Claude adjusts and regenerates
```

### Skill Best Practices for Multi-Modal Workflows

**1. Context Management**
- Keep SKILL.md under 500 lines
- Use progressive disclosure: overview → details → references
- Assume Claude has foundational knowledge
- Include table of contents for files >100 lines

**2. Resource Organization**
```
Good Structure (one level deep):
skill/
├── SKILL.md              # Overview + navigation
├── pdf_extraction.md     # Specialized guidance
├── csv_parsing.md        # Alternative input handling
└── scripts/             # Executable utilities

Avoid (nested references):
skill/
├── SKILL.md
└── docs/
    └── advanced/
        └── pdf_extraction.md  # Too deep - may not load fully
```

**3. Executable Code Over Generation**
- Provide robust scripts for fragile operations
- Implement error handling with helpful messages
- Justify all parameter values (no "magic constants")
- Return structured output (JSON) for chaining

**4. Validation Patterns**
```
Workflow: Analyze → Plan → Validate → Execute → Verify

Example:
1. Extract data from PDF
2. Generate extraction plan (JSON)
3. Validate plan against schema
4. Execute extraction
5. Verify output completeness
```

**5. Model-Specific Instructions**
- Test across Haiku, Sonnet, Opus
- Add detail for Haiku if needed
- Use consistent terminology
- Include input/output examples

**6. Multi-Modal Specific Guidelines**
- Specify acceptable input formats (PDF, image, CSV)
- Define output structure (JSON schema)
- Handle format conversion internally
- Provide format-specific extraction rules

---

## Financial Document Processing Patterns

### Production Implementation: Multi-Modal Sub-Agents

**Architecture:** Orchestrator (Opus/Sonnet) + Specialist Sub-Agents (Haiku)

**Use Case:** Analyzing Apple's Quarterly Earnings Reports (4 quarters)

**Implementation Pattern:**

```python
import anthropic
import fitz  # PyMuPDF
from PIL import Image
import base64
import io
from concurrent.futures import ThreadPoolExecutor

client = anthropic.Anthropic()

# Step 1: Convert PDF pages to images
def pdf_to_base64_pngs(pdf_path, quality=75, max_size=(1024, 1024)):
    """
    Convert PDF to base64-encoded PNGs for visual analysis

    Args:
        pdf_path: Path to PDF file
        quality: JPEG compression quality (1-100)
        max_size: Maximum dimensions (width, height)

    Returns:
        List of base64-encoded PNG strings
    """
    doc = fitz.open(pdf_path)
    base64_encoded_pngs = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # Render at 300 DPI
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))

        # Convert to PIL Image
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Resize if needed (optimize token usage)
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)

        # Encode as PNG
        image_data = io.BytesIO()
        image.save(image_data, format='PNG', optimize=True, quality=quality)

        # Base64 encode
        base64_encoded = base64.b64encode(image_data.getvalue()).decode('utf-8')
        base64_encoded_pngs.append(base64_encoded)

    doc.close()
    return base64_encoded_pngs


# Step 2: Generate specialized extraction prompt for sub-agents
def generate_haiku_prompt(question):
    """
    Use orchestrator model to create focused extraction prompt

    Returns: Specific prompt for Haiku sub-agents
    """
    messages = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"""
Based on the following question, generate a specific prompt for an LLM sub-agent
to extract relevant information from a quarterly earnings report PDF.

Each sub-agent only has access to a SINGLE quarter's report.

Question: {question}

Generate a focused extraction prompt that:
1. Specifies exactly what data to extract
2. Defines the output format (JSON preferred)
3. Handles missing data gracefully
4. Includes validation rules
"""
        }]
    }]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=messages
    )

    return response.content[0].text


# Step 3: Extract information from single PDF using Haiku
def extract_info(pdf_path, haiku_prompt):
    """
    Process single PDF with Haiku sub-agent

    Returns: (extracted_data, pdf_path)
    """
    base64_encoded_pngs = pdf_to_base64_pngs(pdf_path)

    # Build message with all page images + extraction prompt
    messages = [{
        "role": "user",
        "content": [
            # Include all page images
            *[{
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": img
                }
            } for img in base64_encoded_pngs],

            # Add extraction prompt
            {
                "type": "text",
                "text": haiku_prompt
            }
        ]
    }]

    # Use Haiku for cost-effective extraction
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=2048,
        messages=messages
    )

    return response.content[0].text, pdf_path


# Step 4: Parallel processing with ThreadPoolExecutor
def process_earnings_reports(pdf_paths, user_question):
    """
    Process multiple earnings reports in parallel

    Returns: List of (extracted_data, pdf_path) tuples
    """
    # Generate specialized prompt
    haiku_prompt = generate_haiku_prompt(user_question)

    # Process PDFs in parallel
    with ThreadPoolExecutor(max_workers=4) as executor:
        extracted_info_list = list(
            executor.map(
                lambda path: extract_info(path, haiku_prompt),
                pdf_paths
            )
        )

    return extracted_info_list


# Step 5: Aggregate and synthesize with orchestrator
def synthesize_analysis(extracted_info_list, user_question):
    """
    Use Opus/Sonnet to analyze aggregated data and generate response
    """
    # Format extracted data with XML tags for structure
    extracted_info = ""
    for info, pdf_path in extracted_info_list:
        quarter = pdf_path.split("/")[-1].split("_")[1]  # Extract quarter from filename
        extracted_info += f'<info quarter="{quarter}">{info}</info>\n'

    # Synthesis prompt
    messages = [{
        "role": "user",
        "content": [{
            "type": "text",
            "text": f"""
Based on the following extracted information from quarterly earnings reports,
answer this question: {user_question}

Extracted Data:
{extracted_info}

Provide:
1. Direct answer to the question
2. Supporting data and trends
3. Visualization code (matplotlib) wrapped in <code></code> tags
4. Key insights and analysis

If generating visualization code, ensure it:
- Uses the extracted data
- Is self-contained and executable
- Includes proper labels and titles
- Saves output as PNG
"""
        }]
    }]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=messages
    )

    return response.content[0].text


# Step 6: Extract and execute visualization code
def extract_code_and_response(response):
    """
    Parse response to separate code from narrative
    """
    start_tag = "<code>"
    end_tag = "</code>"

    start_index = response.find(start_tag)
    end_index = response.find(end_tag)

    if start_index != -1 and end_index != -1:
        code = response[start_index + len(start_tag):end_index].strip()
        non_code_response = response[:start_index].strip()
        return code, non_code_response

    return None, response.strip()


# Complete workflow example
def analyze_earnings_with_visualization(pdf_paths, question):
    """
    End-to-end earnings analysis with automated visualization
    """
    # Extract data from all PDFs in parallel
    extracted_data = process_earnings_reports(pdf_paths, question)

    # Synthesize analysis and generate visualization
    analysis = synthesize_analysis(extracted_data, question)

    # Extract and execute matplotlib code
    matplotlib_code, narrative = extract_code_and_response(analysis)

    print("Analysis:")
    print(narrative)
    print("\n" + "="*80 + "\n")

    if matplotlib_code:
        print("Generating visualization...")
        exec(matplotlib_code)
        print("Visualization saved!")

    return narrative, matplotlib_code


# Usage
if __name__ == "__main__":
    pdf_paths = [
        "/data/earnings/AAPL_Q1_2024.pdf",
        "/data/earnings/AAPL_Q2_2024.pdf",
        "/data/earnings/AAPL_Q3_2024.pdf",
        "/data/earnings/AAPL_Q4_2024.pdf"
    ]

    question = """
    What is the trend in iPhone revenue over the past year?
    Show quarterly figures and calculate YoY growth rates.
    """

    narrative, code = analyze_earnings_with_visualization(pdf_paths, question)
```

**Key Patterns:**

1. **PDF → Image Conversion:** Handles complex layouts better than text extraction alone
2. **Specialized Prompts:** Orchestrator generates focused extraction instructions
3. **Parallel Processing:** ThreadPoolExecutor distributes work across sub-agents
4. **Structured Aggregation:** XML tags preserve metadata during synthesis
5. **Code Generation:** Matplotlib visualization automatically generated and executed
6. **Model Stratification:** Haiku for extraction ($), Sonnet for synthesis ($$)

**Cost Analysis:**

```
Example: 4 PDFs, 10 pages each

Extraction Phase (Haiku):
- Per PDF: 10 pages × 1,500 tokens/page = 15,000 tokens input
- 4 PDFs: 60,000 tokens input
- Output: 2,000 tokens per PDF × 4 = 8,000 tokens
- Cost: (60k × $1.00) + (8k × $5.00) = $0.06 + $0.04 = $0.10

Synthesis Phase (Sonnet):
- Input: 8,000 tokens (aggregated data) + 500 tokens (prompt) = 8,500 tokens
- Output: 2,000 tokens (analysis + code)
- Cost: (8.5k × $3.00) + (2k × $15.00) = $0.026 + $0.03 = $0.056

Total: $0.156 for comprehensive multi-document analysis with visualization

Batch Alternative (50% discount):
- Total: $0.078 (if processing delay acceptable)
```

### Chart Analysis Implementation

**Financial Chart Interpretation Pattern:**

```python
def analyze_technical_chart(chart_image_path):
    """
    Analyze technical analysis chart and extract trading signals
    """
    # Encode image
    with open(chart_image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')

    messages = [{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": """
Analyze this technical analysis chart and provide:

1. **Trend Identification:**
   - Primary trend (uptrend/downtrend/sideways)
   - Trend strength
   - Key support and resistance levels

2. **Technical Indicators:**
   - RSI reading and interpretation
   - MACD signal (bullish/bearish)
   - Moving average positioning (50-day, 200-day)
   - Volume patterns

3. **Chart Patterns:**
   - Identify any chart patterns (head & shoulders, triangles, etc.)
   - Breakout/breakdown levels

4. **Trading Signals:**
   - Current signal (buy/sell/hold)
   - Confidence level (1-10)
   - Risk/reward ratio
   - Suggested entry/exit points

5. **Outlook:**
   - Short-term (1-5 days)
   - Medium-term (1-4 weeks)
   - Key levels to watch

Return analysis as structured JSON.
"""
            }
        ]
    }]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=messages
    )

    return response.content[0].text


# Portfolio Performance Chart Analysis
def analyze_portfolio_performance_chart(chart_image_path, benchmark="SPY"):
    """
    Analyze portfolio performance chart vs. benchmark
    """
    with open(chart_image_path, "rb") as img_file:
        image_data = base64.b64encode(img_file.read()).decode('utf-8')

    messages = [{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": f"""
Analyze this portfolio performance chart and extract:

1. **Performance Metrics:**
   - Total return (%)
   - Annualized return
   - Maximum drawdown
   - Recovery periods

2. **Benchmark Comparison:**
   - Portfolio vs. {benchmark}
   - Alpha (excess return)
   - Periods of outperformance/underperformance
   - Correlation with benchmark

3. **Volatility Analysis:**
   - Visual assessment of volatility
   - Periods of high/low volatility
   - Volatility vs. benchmark

4. **Risk Assessment:**
   - Drawdown frequency and severity
   - Recovery speed
   - Consistency of returns

5. **Time Period Analysis:**
   - Start and end dates
   - Identify key periods (bull/bear markets)
   - Performance in different market conditions

Return as JSON with extracted values.
"""
            }
        ]
    }]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=messages
    )

    return response.content[0].text
```

### Table Extraction from Financial Statements

```python
def extract_financial_tables(statement_pdf_path):
    """
    Extract financial statement tables with high accuracy

    Combines:
    1. PDF text layer extraction
    2. Visual table analysis (as backup)
    3. Cross-validation
    """
    # Upload to Files API
    with open(statement_pdf_path, "rb") as pdf_file:
        file_response = client.beta.files.create(
            file=pdf_file,
            purpose="analysis"
        )

    file_id = file_response.id

    messages = [{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "file", "file_id": file_id}
            },
            {
                "type": "text",
                "text": """
Extract all financial statement tables from this document.

For each table, provide:

1. **Table Identification:**
   - Table type (Balance Sheet, Income Statement, Cash Flow)
   - Period covered
   - Page number

2. **Data Extraction:**
   - All line items with values
   - Column headers (periods)
   - Subtotals and totals
   - Units (thousands, millions, etc.)

3. **Validation:**
   - Verify subtotals sum correctly
   - Check year-over-year consistency
   - Flag any anomalies

Return as structured JSON:

```json
{
  "tables": [
    {
      "type": "income_statement",
      "period": "Q4 2024",
      "page": 3,
      "data": {
        "revenue": {
          "2024_Q4": 50000000,
          "2023_Q4": 45000000,
          "yoy_change": 11.1
        },
        "operating_expenses": { ... },
        "net_income": { ... }
      },
      "validation": {
        "totals_verified": true,
        "anomalies": []
      }
    }
  ]
}
```

Prioritize accuracy over speed. If values are unclear, flag for manual review.
"""
            }
        ]
    }]

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=8192,
        messages=messages
    )

    return response.content[0].text
```

---

## Workflow Orchestration

### Claude-Flow: Enterprise Agent Orchestration

**Overview:**
Claude-Flow is a sophisticated agent orchestration platform for Claude Code, enabling:
- Multi-agent swarm deployment
- Autonomous workflow coordination
- Distributed task management
- RAG integration
- Native MCP protocol support

**Installation:**
```bash
npm install -g claude-flow@alpha
```

**Basic Commands:**
```bash
# Spawn individual agent
npx claude-flow@alpha swarm spawn researcher 'analyze API patterns'

# Spawn multiple specialized agents
npx claude-flow@alpha swarm spawn coder 'implement endpoints'
npx claude-flow@alpha swarm spawn tester 'write test suite'

# Complex workflow coordination
npx claude-flow@alpha swarm coordinate \
  backend-architect \
  database-architect \
  frontend-developer \
  test-automator \
  security-auditor \
  deployment-engineer \
  observability-engineer
```

### Sub-Agent Patterns with Claude Agent SDK

**Architecture:**

```
Orchestrator Agent
├── Sub-Agent 1: PDF Processor (Haiku)
├── Sub-Agent 2: Data Validator (Haiku)
├── Sub-Agent 3: Chart Analyzer (Haiku)
└── Sub-Agent 4: Report Generator (Sonnet)
```

**Benefits:**
1. **Parallelization:** Multiple sub-agents work simultaneously
2. **Context Isolation:** Each sub-agent has dedicated context window
3. **Specialization:** Focused expertise per agent
4. **Cost Optimization:** Use appropriate model tiers

**Implementation Example:**

```python
from anthropic import Anthropic, SubAgent

client = Anthropic()

# Define sub-agent for PDF processing
pdf_processor = SubAgent(
    name="pdf_processor",
    model="claude-haiku-4-5",
    instructions="""
    You are a specialized PDF processor. Extract structured data from
    financial documents. Return JSON with validated fields.
    """,
    max_tokens=2048
)

# Define sub-agent for data validation
data_validator = SubAgent(
    name="data_validator",
    model="claude-haiku-4-5",
    instructions="""
    You validate financial data for accuracy and consistency.
    Check calculations, verify totals, flag anomalies.
    """,
    max_tokens=1024
)

# Define sub-agent for chart analysis
chart_analyzer = SubAgent(
    name="chart_analyzer",
    model="claude-haiku-4-5",
    instructions="""
    You analyze technical charts and extract trading signals.
    Identify trends, support/resistance, indicators.
    """,
    max_tokens=2048
)

# Define sub-agent for report generation
report_generator = SubAgent(
    name="report_generator",
    model="claude-sonnet-4-5",
    instructions="""
    You synthesize analysis from other agents and create comprehensive
    investment reports with recommendations.
    """,
    max_tokens=4096
)

# Orchestrator workflow
def process_earnings_report_workflow(pdf_path, chart_path):
    """
    Multi-agent workflow for earnings report analysis
    """
    # Upload files
    with open(pdf_path, "rb") as pdf:
        pdf_file = client.beta.files.create(file=pdf, purpose="analysis")

    with open(chart_path, "rb") as chart:
        chart_data = base64.b64encode(chart.read()).decode('utf-8')

    # Step 1: Parallel extraction (PDF + Chart)
    with ThreadPoolExecutor() as executor:
        # PDF processing
        pdf_future = executor.submit(
            lambda: pdf_processor.process({
                "document": {"file_id": pdf_file.id},
                "task": "Extract revenue, EPS, guidance, and key metrics"
            })
        )

        # Chart analysis
        chart_future = executor.submit(
            lambda: chart_analyzer.process({
                "image": {"data": chart_data, "media_type": "image/png"},
                "task": "Analyze stock price reaction and technical signals"
            })
        )

        pdf_results = pdf_future.result()
        chart_results = chart_future.result()

    # Step 2: Validation
    validation_results = data_validator.process({
        "data": pdf_results["content"],
        "task": "Validate extracted financial metrics and calculations"
    })

    # Step 3: Synthesis
    final_report = report_generator.process({
        "inputs": {
            "financial_data": validation_results["content"],
            "technical_analysis": chart_results["content"]
        },
        "task": """
        Create comprehensive earnings analysis report including:
        1. Financial performance summary
        2. Technical analysis interpretation
        3. Investment recommendation
        4. Risk assessment
        5. Price target and rationale
        """
    })

    return final_report["content"]


# Usage
report = process_earnings_report_workflow(
    pdf_path="/data/earnings/AAPL_Q4_2024.pdf",
    chart_path="/data/charts/AAPL_technical_chart.png"
)

print(report)
```

### Multi-Agent Workflow Patterns

**Pattern 1: Pipeline (Sequential)**
```
Agent 1: Extract → Agent 2: Transform → Agent 3: Validate → Agent 4: Report
```

Use case: Document processing where each stage depends on previous output

**Pattern 2: Fan-Out/Fan-In (Parallel)**
```
                  ┌─ Agent 1: PDF Analysis
Orchestrator ─────┼─ Agent 2: Chart Analysis  ─→ Aggregator → Final Report
                  └─ Agent 3: Sentiment Analysis
```

Use case: Multi-source analysis requiring independent parallel processing

**Pattern 3: Hierarchical (Delegation)**
```
Senior Agent (Sonnet)
├─ Junior Agent 1 (Haiku): Document 1
├─ Junior Agent 2 (Haiku): Document 2
└─ Junior Agent 3 (Haiku): Document 3
     └─ Specialist Agent (Haiku): Complex table extraction
```

Use case: Large-scale document processing with complex sub-tasks

**Pattern 4: Iterative Refinement**
```
Agent 1: Initial Analysis → Agent 2: Critique → Agent 1: Refinement → Agent 2: Validation
```

Use case: High-accuracy requirements where iterative improvement needed

### Financial Workflow Examples

**Earnings Season Processing:**

```python
def earnings_season_workflow(company_tickers):
    """
    Process earnings for multiple companies in parallel

    Returns: Consolidated analysis across all companies
    """
    orchestrator = Agent(model="claude-sonnet-4-5")

    # Create sub-agent pool
    document_agents = [
        SubAgent(name=f"doc_agent_{i}", model="claude-haiku-4-5")
        for i in range(10)  # Pool of 10 agents
    ]

    # Distribute work
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []

        for ticker in company_tickers:
            # Assign to available agent
            agent = document_agents[len(futures) % 10]

            future = executor.submit(
                agent.process,
                {
                    "task": f"Analyze {ticker} Q4 2024 earnings report",
                    "document": {"file_id": f"file_{ticker}_earnings"}
                }
            )
            futures.append((ticker, future))

        # Collect results
        results = {
            ticker: future.result()
            for ticker, future in futures
        }

    # Orchestrator synthesizes
    consolidated = orchestrator.process({
        "task": "Create sector-wide earnings analysis",
        "inputs": results
    })

    return consolidated
```

**Portfolio Validation Pipeline:**

```python
def portfolio_validation_pipeline(portfolio_statement):
    """
    Multi-stage validation workflow for portfolio statements
    """
    # Stage 1: Extraction
    extractor = SubAgent(name="extractor", model="claude-haiku-4-5")
    extracted_data = extractor.process({
        "document": {"file_id": portfolio_statement},
        "task": "Extract all positions, values, and account metadata"
    })

    # Stage 2: Market Data Validation (parallel)
    validator_pool = [
        SubAgent(name=f"validator_{i}", model="claude-haiku-4-5")
        for i in range(5)
    ]

    positions = extracted_data["positions"]
    position_chunks = [positions[i::5] for i in range(5)]  # Split into 5 chunks

    with ThreadPoolExecutor() as executor:
        validation_futures = [
            executor.submit(
                agent.process,
                {
                    "task": "Validate positions against market data",
                    "positions": chunk
                }
            )
            for agent, chunk in zip(validator_pool, position_chunks)
        ]

        validated_positions = [
            f.result() for f in validation_futures
        ]

    # Stage 3: Risk Assessment
    risk_assessor = SubAgent(name="risk_assessor", model="claude-sonnet-4-5")
    risk_analysis = risk_assessor.process({
        "task": "Assess portfolio risk metrics",
        "portfolio": validated_positions
    })

    # Stage 4: Report Generation
    report_generator = SubAgent(name="reporter", model="claude-sonnet-4-5")
    final_report = report_generator.process({
        "task": "Generate validation report with recommendations",
        "inputs": {
            "extracted_data": extracted_data,
            "validated_positions": validated_positions,
            "risk_analysis": risk_analysis
        }
    })

    return final_report
```

---

## Performance Optimization

### Token Usage Optimization

**Image Optimization:**

```python
def optimize_image_for_claude(image_path, target_tokens=1500):
    """
    Resize image to target token count

    Token formula: (width × height) / 750
    """
    from PIL import Image
    import math

    # Open image
    img = Image.open(image_path)
    width, height = img.size

    # Calculate current tokens
    current_tokens = (width * height) / 750

    if current_tokens <= target_tokens:
        return img  # Already optimized

    # Calculate target dimensions
    scale_factor = math.sqrt(target_tokens / current_tokens)
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)

    # Resize maintaining aspect ratio
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    print(f"Optimized: {width}×{height} ({current_tokens:.0f} tokens) "
          f"→ {new_width}×{new_height} ({target_tokens:.0f} tokens)")

    return img_resized


# Usage
optimized_chart = optimize_image_for_claude("portfolio_chart.png", target_tokens=1200)
optimized_chart.save("portfolio_chart_optimized.png", optimize=True, quality=85)
```

**PDF Page Selection:**

```python
def extract_relevant_pdf_pages(pdf_path, page_ranges):
    """
    Extract only relevant pages to reduce token usage

    Example: Extract pages 1-3 and 10-12 from earnings report
    """
    import fitz

    doc = fitz.open(pdf_path)
    new_doc = fitz.open()

    for start, end in page_ranges:
        for page_num in range(start - 1, end):  # Convert to 0-indexed
            new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

    output_path = pdf_path.replace(".pdf", "_extracted.pdf")
    new_doc.save(output_path)
    new_doc.close()
    doc.close()

    return output_path


# Usage: Extract executive summary (pages 1-3) and financial statements (pages 15-25)
optimized_pdf = extract_relevant_pdf_pages(
    "earnings_report_full.pdf",
    page_ranges=[(1, 3), (15, 25)]
)
```

### Prompt Caching for Repeated Analysis

**Enable Caching for Large Documents:**

```python
def analyze_with_caching(document_file_id, queries):
    """
    Process multiple queries on same document with caching

    First query: Full cost
    Subsequent queries: Cached document (90% cost reduction on input)
    """
    results = []

    for query in queries:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            system=[
                {
                    "type": "text",
                    "text": "You are a financial analyst expert.",
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {"type": "file", "file_id": document_file_id},
                        "cache_control": {"type": "ephemeral"}  # Cache document
                    },
                    {
                        "type": "text",
                        "text": query
                    }
                ]
            }]
        )

        results.append({
            "query": query,
            "answer": response.content[0].text,
            "usage": response.usage
        })

    return results


# Usage: Analyze same earnings report with multiple questions
queries = [
    "What was the revenue growth rate?",
    "Extract all operating expense categories and amounts.",
    "What guidance was provided for next quarter?",
    "Summarize key risks mentioned in the report."
]

results = analyze_with_caching("file_earnings_q4", queries)

# Cost analysis
total_input_tokens = sum(r["usage"]["input_tokens"] for r in results)
total_cached_tokens = sum(r["usage"].get("cache_read_input_tokens", 0) for r in results)

print(f"Total input tokens: {total_input_tokens}")
print(f"Cached tokens: {total_cached_tokens}")
print(f"Cache savings: {(total_cached_tokens / total_input_tokens * 100):.1f}%")
```

### Batch Processing Cost Optimization

**Batch vs. Real-Time Decision Matrix:**

| Use Case | Urgency | Volume | Recommendation |
|----------|---------|--------|---------------|
| Portfolio validation | Low | High (100s of statements) | **Batch** (50% savings) |
| Live trading signals | High | Low (single analysis) | Real-time API |
| Earnings season analysis | Medium | Very high (1000s) | **Batch** (massive savings) |
| Compliance review | Low | High | **Batch** |
| Ad-hoc research | High | Low | Real-time API |
| Historical backtesting | Low | Very high | **Batch** |

**Cost Comparison Example:**

```python
def calculate_batch_savings(num_documents, avg_tokens_per_doc, model="claude-sonnet-4-5"):
    """
    Calculate cost savings for batch processing
    """
    pricing = {
        "claude-sonnet-4-5": {
            "input_standard": 3.00,
            "output_standard": 15.00,
            "input_batch": 1.50,
            "output_batch": 7.50
        },
        "claude-haiku-4-5": {
            "input_standard": 1.00,
            "output_standard": 5.00,
            "input_batch": 0.50,
            "output_batch": 2.50
        }
    }

    total_input_tokens = num_documents * avg_tokens_per_doc
    assumed_output_per_doc = 2000
    total_output_tokens = num_documents * assumed_output_per_doc

    # Standard API cost
    standard_cost = (
        (total_input_tokens / 1_000_000) * pricing[model]["input_standard"] +
        (total_output_tokens / 1_000_000) * pricing[model]["output_standard"]
    )

    # Batch API cost
    batch_cost = (
        (total_input_tokens / 1_000_000) * pricing[model]["input_batch"] +
        (total_output_tokens / 1_000_000) * pricing[model]["output_batch"]
    )

    savings = standard_cost - batch_cost
    savings_pct = (savings / standard_cost) * 100

    return {
        "num_documents": num_documents,
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "standard_cost": standard_cost,
        "batch_cost": batch_cost,
        "savings": savings,
        "savings_pct": savings_pct
    }


# Example: 500 earnings reports
result = calculate_batch_savings(
    num_documents=500,
    avg_tokens_per_doc=60000,  # ~30-page PDF
    model="claude-sonnet-4-5"
)

print(f"Processing 500 earnings reports:")
print(f"  Standard API: ${result['standard_cost']:.2f}")
print(f"  Batch API: ${result['batch_cost']:.2f}")
print(f"  Savings: ${result['savings']:.2f} ({result['savings_pct']:.1f}%)")

# Output:
# Processing 500 earnings reports:
#   Standard API: $105.00
#   Batch API: $52.50
#   Savings: $52.50 (50.0%)
```

### Parallel Processing Best Practices

**Optimal Concurrency Levels:**

```python
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def determine_optimal_workers(num_tasks, api_rate_limit=50):
    """
    Calculate optimal thread pool size

    Args:
        num_tasks: Total number of tasks to process
        api_rate_limit: Max requests per minute

    Returns:
        Optimal number of workers
    """
    # Don't exceed rate limits
    max_parallel = min(api_rate_limit, num_tasks)

    # Use system CPU count as upper bound
    cpu_count = os.cpu_count() or 4

    # Heuristic: 2-4x CPU count for I/O-bound tasks
    optimal = min(max_parallel, cpu_count * 3)

    return optimal


def parallel_document_processing(file_ids, processing_func):
    """
    Process documents in parallel with optimal concurrency
    """
    num_workers = determine_optimal_workers(len(file_ids))

    print(f"Processing {len(file_ids)} documents with {num_workers} workers...")

    results = []
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit all tasks
        future_to_file = {
            executor.submit(processing_func, file_id): file_id
            for file_id in file_ids
        }

        # Collect results as they complete
        for future in as_completed(future_to_file):
            file_id = future_to_file[future]
            try:
                result = future.result()
                results.append({"file_id": file_id, "result": result, "success": True})
            except Exception as e:
                results.append({"file_id": file_id, "error": str(e), "success": False})

    # Summary
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful

    print(f"Completed: {successful} successful, {failed} failed")

    return results
```

### Model Selection Strategy

**Cost vs. Capability Matrix:**

| Task | Complexity | Model | Cost/MTok (Input) | Rationale |
|------|-----------|-------|------------------|-----------|
| PDF data extraction | Low | Haiku 4.5 | $0.50 (batch) | Simple structured extraction |
| Chart analysis | Medium | Haiku 4.5 | $1.00 (standard) | Visual interpretation, needs speed |
| Earnings synthesis | High | Sonnet 4.5 | $1.50 (batch) | Complex reasoning, not urgent |
| Real-time trading signals | High | Sonnet 4.5 | $3.00 (standard) | Accuracy critical, time-sensitive |
| Report generation | High | Sonnet 4.5 | $3.00 (standard) | Quality matters, user-facing |
| Compliance validation | Medium | Haiku 4.5 | $0.50 (batch) | Rule-based, high volume |

**Adaptive Model Selection:**

```python
def select_optimal_model(task_type, urgency="low", volume=1):
    """
    Choose model based on task requirements

    Returns: (model, use_batch)
    """
    if urgency == "high":
        # Real-time required, no batching
        if task_type in ["complex_analysis", "report_generation"]:
            return "claude-sonnet-4-5", False
        else:
            return "claude-haiku-4-5", False

    elif volume > 50:
        # High volume, use batch with appropriate model
        if task_type in ["complex_analysis", "synthesis"]:
            return "claude-sonnet-4-5", True
        else:
            return "claude-haiku-4-5", True

    else:
        # Standard use case
        if task_type in ["extraction", "validation", "simple_analysis"]:
            return "claude-haiku-4-5", False
        else:
            return "claude-sonnet-4-5", False


# Usage
model, use_batch = select_optimal_model(
    task_type="extraction",
    urgency="low",
    volume=500
)

print(f"Selected: {model}, Batch: {use_batch}")
# Output: Selected: claude-haiku-4-5, Batch: True
```

---

## Implementation Recommendations for Portfolio Validation Engine

### Architecture Proposal

**Multi-Modal Integration Layers:**

```
┌─────────────────────────────────────────────────────────────┐
│                     Portfolio Validation Engine              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌───────────────────┐  ┌───────────────────┐              │
│  │  Document Input   │  │  Market Data      │              │
│  │  - PDF Statements │  │  - Price Feeds    │              │
│  │  - CSV Exports    │  │  - Fundamental    │              │
│  │  - Screenshots    │  │  - Technical      │              │
│  └─────────┬─────────┘  └────────┬──────────┘              │
│            │                     │                          │
│            └──────────┬──────────┘                          │
│                       ▼                                     │
│           ┌───────────────────────┐                         │
│           │  Multi-Modal Ingestion │                         │
│           │  - Files API Upload    │                         │
│           │  - Image Optimization  │                         │
│           │  - PDF Pre-processing  │                         │
│           └──────────┬─────────────┘                         │
│                      ▼                                      │
│           ┌─────────────────────────┐                       │
│           │  Agent Orchestrator     │                       │
│           │  (Claude Sonnet 4.5)    │                       │
│           └──────────┬──────────────┘                       │
│                      │                                      │
│        ┌─────────────┼─────────────┬─────────────┐         │
│        ▼             ▼             ▼             ▼         │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │
│   │Document │  │ Market  │  │  Risk   │  │Technical│     │
│   │Processor│  │Validator│  │Assessor │  │Analyzer │     │
│   │ (Haiku) │  │ (Haiku) │  │(Sonnet) │  │ (Haiku) │     │
│   └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │
│        │            │            │            │            │
│        └────────────┼────────────┼────────────┘            │
│                     ▼            ▼                         │
│              ┌─────────────────────────┐                   │
│              │  Validation Engine      │                   │
│              │  - Position Reconcile   │                   │
│              │  - Performance Calc     │                   │
│              │  - Risk Metrics         │                   │
│              │  - Compliance Check     │                   │
│              └──────────┬──────────────┘                   │
│                         ▼                                  │
│              ┌─────────────────────────┐                   │
│              │  Report Generator       │                   │
│              │  (Claude Sonnet 4.5)    │                   │
│              │  - Master Trade Ticket  │                   │
│              │  - Board Notes          │                   │
│              │  - Visualizations       │                   │
│              └─────────────────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Recommended Skills for Portfolio Validation

**Skill 1: Portfolio Statement Processor**
- **Purpose:** Extract positions from broker statements (PDF/CSV/screenshots)
- **Model:** Claude Haiku 4.5
- **Processing:** Batch for bulk, real-time for ad-hoc
- **Output:** Structured JSON with positions, values, metadata

**Skill 2: Market Data Validator**
- **Purpose:** Cross-reference extracted positions with live market data
- **Model:** Claude Haiku 4.5
- **Integration:** Connect to market data APIs (Daloopa, Morningstar, etc.)
- **Output:** Validated positions with current prices, discrepancy flags

**Skill 3: Risk Assessor**
- **Purpose:** Calculate portfolio risk metrics (concentration, volatility, VaR)
- **Model:** Claude Sonnet 4.5
- **Processing:** Real-time or scheduled daily
- **Output:** Risk report with concentration analysis, drawdown metrics

**Skill 4: Technical Chart Analyzer**
- **Purpose:** Interpret technical analysis charts for position validation
- **Model:** Claude Haiku 4.5
- **Input:** Chart images from trading platforms
- **Output:** Trend analysis, signal confirmation, support/resistance levels

**Skill 5: Master Trade Ticket Generator**
- **Purpose:** Synthesize all validation results into final recommendation
- **Model:** Claude Sonnet 4.5
- **Input:** Aggregated validation data from all skills
- **Output:** Comprehensive trade ticket, board notes, executive summary

### Implementation Phases

**Phase 1: Document Processing Infrastructure (Weeks 1-2)**

1. Implement Files API integration
   - Upload handler for PDFs, CSVs, images
   - File lifecycle management
   - Storage organization

2. Create Portfolio Statement Processor skill
   - PDF extraction logic
   - CSV parsing
   - Image OCR fallback
   - Validation schemas

3. Build batch processing pipeline
   - Batch API integration
   - Queue management
   - Result aggregation

**Phase 2: Multi-Modal Analysis (Weeks 3-4)**

1. Develop Technical Chart Analyzer skill
   - Image optimization
   - Chart interpretation prompts
   - Signal extraction

2. Implement Market Data Validator skill
   - API integrations (market data sources)
   - Cross-validation logic
   - Discrepancy detection

3. Create sub-agent orchestration
   - Parallel processing framework
   - Agent pool management
   - Result consolidation

**Phase 3: Risk & Compliance (Weeks 5-6)**

1. Build Risk Assessor skill
   - Concentration analysis
   - Volatility calculations
   - VaR/CVaR computation
   - Drawdown tracking

2. Implement compliance validation
   - Position limits checking
   - Regulatory requirements
   - Audit trail generation

3. Develop sentiment analysis integration
   - News sentiment for holdings
   - Social media analysis
   - Analyst rating aggregation

**Phase 4: Report Generation & Visualization (Weeks 7-8)**

1. Create Master Trade Ticket Generator skill
   - Template-based report generation
   - Excel/PowerPoint/PDF outputs
   - Visualization generation

2. Build dashboard integration
   - Real-time position tracking
   - Performance charts
   - Risk metrics visualization

3. Implement feedback loops
   - Visual verification workflows
   - Iterative refinement
   - Quality assurance

**Phase 5: Optimization & Production (Weeks 9-10)**

1. Performance optimization
   - Token usage analysis
   - Caching implementation
   - Batch vs. real-time optimization

2. Cost management
   - Model selection automation
   - Usage monitoring
   - Budget alerts

3. Production deployment
   - CI/CD pipeline
   - Monitoring & logging
   - Error handling & retries

### Cost Projections

**Assumptions:**
- 100 portfolio statements/month (avg 30 pages, 60k tokens each)
- 500 position validations/month (avg 5k tokens each)
- 20 technical charts analyzed/month (avg 1.5k tokens each)
- 100 comprehensive reports/month (avg 10k tokens input, 4k output)

**Monthly Cost Estimate:**

| Task | Volume | Model | Processing | Input Tokens | Output Tokens | Cost |
|------|--------|-------|-----------|-------------|---------------|------|
| Statement extraction | 100 | Haiku 4.5 | Batch | 6M | 200k | $3.50 |
| Position validation | 500 | Haiku 4.5 | Real-time | 2.5M | 500k | $5.00 |
| Chart analysis | 20 | Haiku 4.5 | Real-time | 30k | 40k | $0.23 |
| Risk assessment | 100 | Sonnet 4.5 | Batch | 1M | 200k | $3.00 |
| Report generation | 100 | Sonnet 4.5 | Real-time | 1M | 400k | $9.00 |
| **Total** | | | | **10.53M** | **1.34M** | **$20.73** |

**Annual Cost:** ~$250

**Cost per Portfolio Analysis:** ~$0.21

**ROI Calculation:**
- Manual analyst time saved: ~2 hours per portfolio @ $100/hour = $200/portfolio
- Automated cost: $0.21/portfolio
- **Savings: $199.79 per portfolio (99.9% cost reduction)**
- **Annual savings (100 portfolios/month):** $239,748

### Integration with Existing Codebase

**File Structure:**
```
portfolio_validation_engine/
├── .claude/
│   ├── skills/
│   │   ├── portfolio_processor/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── extract_positions.py
│   │   │   │   ├── validate_data.py
│   │   │   │   └── optimize_pdf.py
│   │   │   └── resources/
│   │   │       ├── broker_templates/
│   │   │       │   ├── schwab.json
│   │   │       │   ├── fidelity.json
│   │   │       │   └── interactive_brokers.json
│   │   │       └── schemas/
│   │   │           └── position_schema.json
│   │   │
│   │   ├── market_validator/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── fetch_prices.py
│   │   │   │   └── validate_positions.py
│   │   │   └── resources/
│   │   │       └── ticker_mappings.csv
│   │   │
│   │   ├── risk_assessor/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── calculate_metrics.py
│   │   │   │   ├── concentration_analysis.py
│   │   │   │   └── var_calculation.py
│   │   │   └── resources/
│   │   │       └── risk_thresholds.json
│   │   │
│   │   ├── technical_analyzer/
│   │   │   ├── SKILL.md
│   │   │   ├── scripts/
│   │   │   │   ├── chart_analysis.py
│   │   │   │   └── signal_extraction.py
│   │   │   └── resources/
│   │   │       └── indicator_definitions.json
│   │   │
│   │   └── trade_ticket_generator/
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       │   ├── generate_report.py
│   │       │   ├── create_visualizations.py
│   │       │   └── export_documents.py
│   │       └── resources/
│   │           ├── templates/
│   │           │   ├── trade_ticket.xlsx
│   │           │   ├── board_notes.pptx
│   │           │   └── executive_summary.docx
│   │           └── styles/
│   │               └── chart_styles.json
│   │
│   └── hooks/
│       ├── pre-validation.sh
│       └── post-report.sh
│
├── multimodal/
│   ├── __init__.py
│   ├── files_api.py              # Files API integration
│   ├── batch_processor.py        # Batch API wrapper
│   ├── image_optimizer.py        # Image preprocessing
│   ├── pdf_handler.py            # PDF utilities
│   ├── sub_agents.py             # Sub-agent orchestration
│   └── visualization.py          # Chart generation
│
├── workflows/
│   ├── portfolio_validation.py   # Main validation workflow
│   ├── earnings_analysis.py      # Earnings processing
│   ├── compliance_check.py       # Compliance validation
│   └── report_generation.py      # Report pipeline
│
└── config/
    ├── models.yaml               # Model selection config
    ├── batch_settings.yaml       # Batch processing config
    └── cost_limits.yaml          # Budget constraints
```

**Integration with Auth Service:**
```python
# multimodal/files_api.py
from anthropic import Anthropic
from auth_service.schwab_auth_provider import SchwabAuthProvider

class MultiModalFileHandler:
    def __init__(self, auth_provider):
        self.client = Anthropic()
        self.auth_provider = auth_provider

    def upload_broker_statement(self, broker_name, account_id):
        """
        Fetch broker statement via auth service and upload to Files API
        """
        # Authenticate with broker
        session = self.auth_provider.get_authenticated_session()

        # Download statement
        statement_pdf = session.download_statement(account_id)

        # Upload to Files API
        file_response = self.client.beta.files.create(
            file=statement_pdf,
            purpose="analysis"
        )

        return file_response.id
```

### Monitoring & Observability

**Key Metrics to Track:**

1. **Performance Metrics:**
   - Documents processed per hour
   - Average processing time per document
   - Sub-agent utilization
   - Parallel processing efficiency

2. **Cost Metrics:**
   - Token usage (input/output) by task type
   - Cost per document processed
   - Batch vs. real-time cost breakdown
   - Monthly budget tracking

3. **Quality Metrics:**
   - Extraction accuracy (validated positions vs. manual review)
   - Validation discrepancy rate
   - Report generation quality scores
   - User feedback ratings

4. **Reliability Metrics:**
   - Success/failure rates by task type
   - Retry counts
   - API error rates
   - Batch completion times

**Monitoring Implementation:**

```python
# workflows/monitoring.py
import time
import json
from datetime import datetime

class WorkflowMonitor:
    def __init__(self):
        self.metrics = {
            "documents_processed": 0,
            "total_tokens": {"input": 0, "output": 0},
            "total_cost": 0.0,
            "errors": [],
            "processing_times": []
        }

    def track_document(self, doc_type, tokens_used, cost, duration, success=True):
        """
        Track metrics for single document processing
        """
        self.metrics["documents_processed"] += 1
        self.metrics["total_tokens"]["input"] += tokens_used["input"]
        self.metrics["total_tokens"]["output"] += tokens_used["output"]
        self.metrics["total_cost"] += cost
        self.metrics["processing_times"].append({
            "doc_type": doc_type,
            "duration": duration,
            "timestamp": datetime.now().isoformat()
        })

        if not success:
            self.metrics["errors"].append({
                "doc_type": doc_type,
                "timestamp": datetime.now().isoformat()
            })

    def get_summary(self):
        """
        Generate monitoring summary
        """
        avg_processing_time = (
            sum(p["duration"] for p in self.metrics["processing_times"]) /
            len(self.metrics["processing_times"])
            if self.metrics["processing_times"] else 0
        )

        return {
            "total_documents": self.metrics["documents_processed"],
            "total_tokens": self.metrics["total_tokens"],
            "total_cost": round(self.metrics["total_cost"], 2),
            "avg_processing_time": round(avg_processing_time, 2),
            "error_rate": (
                len(self.metrics["errors"]) / self.metrics["documents_processed"]
                if self.metrics["documents_processed"] > 0 else 0
            )
        }

    def export_metrics(self, filepath):
        """
        Export metrics to JSON for analysis
        """
        with open(filepath, 'w') as f:
            json.dump(self.metrics, f, indent=2)


# Usage in workflow
monitor = WorkflowMonitor()

start_time = time.time()
try:
    result = process_portfolio_statement(statement_file_id)
    duration = time.time() - start_time

    monitor.track_document(
        doc_type="portfolio_statement",
        tokens_used=result["usage"],
        cost=result["cost"],
        duration=duration,
        success=True
    )
except Exception as e:
    duration = time.time() - start_time
    monitor.track_document(
        doc_type="portfolio_statement",
        tokens_used={"input": 0, "output": 0},
        cost=0,
        duration=duration,
        success=False
    )

# Export daily metrics
monitor.export_metrics(f"metrics_{datetime.now().strftime('%Y%m%d')}.json")
```

---

## Code Examples & Patterns

### Complete Portfolio Statement Processor

**File: `.claude/skills/portfolio_processor/SKILL.md`**

```markdown
---
name: portfolio_processor
description: Extracts positions, values, and metrics from broker portfolio statements (PDF, CSV, images). Supports Schwab, Fidelity, Interactive Brokers, E*TRADE, TD Ameritrade. Returns validated JSON.
version: 2.0.0
triggers: portfolio, statement, positions, broker, account
---

# Portfolio Statement Processor

## Overview
This skill processes broker portfolio statements to extract complete position data with validation.

## Capabilities
- Multi-format input (PDF, CSV, screenshots)
- Multi-broker support (Schwab, Fidelity, IB, E*TRADE, TDA)
- Automatic format detection
- Data validation and reconciliation
- Standardized JSON output

## Input Formats

### PDF Statements
- Scanned or digital PDFs
- Multi-page support
- Table extraction with layout analysis
- Chart/graph interpretation

### CSV Exports
- Position exports from trading platforms
- Transaction history
- Performance reports

### Screenshots
- Portfolio summary pages
- Position detail screens
- Mobile app screenshots

## Output Schema

```json
{
  "account": {
    "account_id": "string",
    "broker": "string",
    "account_type": "string",
    "statement_date": "YYYY-MM-DD"
  },
  "summary": {
    "total_value": "number",
    "cash": "number",
    "margin_balance": "number",
    "buying_power": "number"
  },
  "positions": [
    {
      "symbol": "string",
      "description": "string",
      "quantity": "number",
      "cost_basis": "number",
      "current_price": "number",
      "current_value": "number",
      "unrealized_gain_loss": "number",
      "unrealized_gain_loss_pct": "number",
      "day_change": "number",
      "day_change_pct": "number"
    }
  ],
  "asset_allocation": {
    "equities": "number",
    "fixed_income": "number",
    "cash": "number",
    "other": "number"
  },
  "validation": {
    "positions_sum_matches_total": "boolean",
    "all_tickers_valid": "boolean",
    "discrepancies": ["string"]
  }
}
```

## Usage Examples

### Extract from PDF
```
Analyze the attached Schwab portfolio statement and extract all positions with current values.
```

### Parse CSV Export
```
Parse this Fidelity CSV export and calculate total portfolio value and asset allocation.
```

### Consolidate Multiple Accounts
```
Process these three statements (Schwab, Fidelity, IB) and create a consolidated portfolio view.
```

## Broker-Specific Notes

### Charles Schwab
- Format: PDF with multi-column layout
- Template: `/resources/broker_templates/schwab.json`
- Notes: Account number on page 1, positions table spans pages

### Fidelity
- Format: PDF or CSV
- Template: `/resources/broker_templates/fidelity.json`
- Notes: CSV exports recommended for accuracy

### Interactive Brokers
- Format: PDF or XML
- Template: `/resources/broker_templates/ib.json`
- Notes: Handles multi-currency accounts

### E*TRADE
- Format: PDF
- Template: `/resources/broker_templates/etrade.json`
- Notes: Includes options positions

### TD Ameritrade
- Format: PDF or CSV
- Template: `/resources/broker_templates/tda.json`
- Notes: Now part of Schwab (use Schwab template for new statements)

## Validation Rules

1. **Ticker Validation:** Run `/scripts/validate_tickers.py` to verify symbols
2. **Sum Verification:** Positions total must match account total value
3. **Percentage Check:** Asset allocation must sum to 100%
4. **Date Validation:** Statement date must be valid and recent
5. **Price Reasonableness:** Flag positions with unusual prices

## Error Handling

If extraction fails or data is unclear:
- Return partial data with `validation.discrepancies` populated
- Flag fields as `null` when unavailable
- Provide confidence scores for ambiguous extractions

## Advanced Features

### Multi-Account Consolidation
Process multiple statements and aggregate:
- Combined positions (merge duplicate symbols)
- Total asset allocation
- Cross-account performance

### Historical Comparison
Compare current statement to previous period:
- Position changes
- Performance over time
- Cash flow analysis

### Tax Analysis
Extract tax lot information:
- Acquisition dates
- Cost basis by lot
- Short-term vs. long-term gains

## Scripts

Run `/scripts/extract_positions.py` for PDF processing
Run `/scripts/validate_data.py` for post-extraction validation
Run `/scripts/optimize_pdf.py` to reduce PDF size before upload

See `/resources/schemas/position_schema.json` for complete data schema
```

**File: `.claude/skills/portfolio_processor/scripts/extract_positions.py`**

```python
#!/usr/bin/env python3
"""
Extract positions from broker statement PDF
"""

import sys
import json
import fitz  # PyMuPDF
from PIL import Image
import base64
import io

def pdf_to_images(pdf_path, max_size=(1024, 1024)):
    """Convert PDF pages to optimized images"""
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)

        img_buffer = io.BytesIO()
        img.save(img_buffer, format='PNG', optimize=True, quality=85)
        img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        images.append({
            "page": page_num + 1,
            "data": img_data,
            "width": img.size[0],
            "height": img.size[1]
        })

    doc.close()
    return images

def extract_text(pdf_path):
    """Extract text content from PDF"""
    doc = fitz.open(pdf_path)
    text_content = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text = page.get_text()
        text_content.append({
            "page": page_num + 1,
            "text": text
        })

    doc.close()
    return text_content

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No PDF path provided"}))
        sys.exit(1)

    pdf_path = sys.argv[1]

    try:
        # Extract both images and text
        images = pdf_to_images(pdf_path)
        text_content = extract_text(pdf_path)

        result = {
            "success": True,
            "num_pages": len(images),
            "images": images,
            "text_content": text_content
        }

        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**File: `.claude/skills/portfolio_processor/scripts/validate_data.py`**

```python
#!/usr/bin/env python3
"""
Validate extracted portfolio data
"""

import sys
import json

def validate_position(position):
    """Validate single position data"""
    errors = []

    # Required fields
    required = ["symbol", "quantity", "current_value"]
    for field in required:
        if field not in position or position[field] is None:
            errors.append(f"Missing required field: {field}")

    # Numeric validations
    if "quantity" in position and position["quantity"] <= 0:
        errors.append(f"Invalid quantity for {position.get('symbol')}: {position['quantity']}")

    if "current_value" in position and position["current_value"] < 0:
        errors.append(f"Negative value for {position.get('symbol')}: {position['current_value']}")

    # Calculate fields match
    if all(k in position for k in ["quantity", "current_price", "current_value"]):
        calculated_value = position["quantity"] * position["current_price"]
        if abs(calculated_value - position["current_value"]) > 0.02:  # Allow $0.02 rounding
            errors.append(
                f"Value mismatch for {position.get('symbol')}: "
                f"calculated {calculated_value} != stated {position['current_value']}"
            )

    return errors

def validate_portfolio(data):
    """Validate complete portfolio data"""
    validation_results = {
        "valid": True,
        "errors": [],
        "warnings": []
    }

    # Validate structure
    if "positions" not in data:
        validation_results["errors"].append("No positions array found")
        validation_results["valid"] = False
        return validation_results

    # Validate each position
    for i, position in enumerate(data["positions"]):
        position_errors = validate_position(position)
        if position_errors:
            validation_results["errors"].extend(
                [f"Position {i+1}: {e}" for e in position_errors]
            )

    # Validate totals
    if "summary" in data and "total_value" in data["summary"]:
        positions_sum = sum(p.get("current_value", 0) for p in data["positions"])
        cash = data["summary"].get("cash", 0)
        calculated_total = positions_sum + cash
        stated_total = data["summary"]["total_value"]

        if abs(calculated_total - stated_total) > 1.00:  # Allow $1 rounding
            validation_results["warnings"].append(
                f"Total value mismatch: calculated {calculated_total:.2f} "
                f"vs stated {stated_total:.2f}"
            )

    # Validate asset allocation
    if "asset_allocation" in data:
        total_allocation = sum(data["asset_allocation"].values())
        if abs(total_allocation - 1.0) > 0.01:  # Allow 1% rounding
            validation_results["warnings"].append(
                f"Asset allocation doesn't sum to 100%: {total_allocation*100:.1f}%"
            )

    if validation_results["errors"]:
        validation_results["valid"] = False

    return validation_results

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No data provided"}))
        sys.exit(1)

    try:
        # Read JSON from stdin or file
        if sys.argv[1] == "-":
            data = json.load(sys.stdin)
        else:
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)

        results = validate_portfolio(data)
        print(json.dumps(results, indent=2))

        sys.exit(0 if results["valid"] else 1)

    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Batch Processing Workflow

**File: `workflows/batch_portfolio_processing.py`**

```python
"""
Batch process multiple portfolio statements with monitoring
"""

import anthropic
import json
import time
from datetime import datetime
from pathlib import Path

class BatchPortfolioProcessor:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.batch_id = None

    def upload_statements(self, statement_paths):
        """Upload multiple portfolio statements to Files API"""
        file_ids = {}

        for path in statement_paths:
            with open(path, "rb") as f:
                response = self.client.beta.files.create(
                    file=f,
                    purpose="analysis"
                )
                file_ids[path] = response.id
                print(f"Uploaded {path}: {response.id}")

        return file_ids

    def create_batch(self, file_ids, extraction_prompt):
        """Create batch processing request"""
        requests = []

        for file_path, file_id in file_ids.items():
            account_id = Path(file_path).stem  # Use filename as account ID

            requests.append({
                "custom_id": account_id,
                "params": {
                    "model": "claude-haiku-4-5",
                    "max_tokens": 4096,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {"type": "file", "file_id": file_id}
                            },
                            {
                                "type": "text",
                                "text": extraction_prompt
                            }
                        ]
                    }]
                }
            })

        # Create batch
        batch_response = self.client.beta.messages.batches.create(
            requests=requests
        )

        self.batch_id = batch_response.id
        print(f"Created batch: {self.batch_id}")
        print(f"Status: {batch_response.processing_status}")

        return batch_response

    def wait_for_completion(self, check_interval=60):
        """Poll batch status until completion"""
        if not self.batch_id:
            raise ValueError("No batch ID set")

        print(f"Waiting for batch {self.batch_id} to complete...")

        while True:
            status_response = self.client.beta.messages.batches.retrieve(
                batch_id=self.batch_id
            )

            status = status_response.processing_status
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Status: {status}")

            if status == "ended":
                print("Batch completed!")
                print(f"Results: {status_response.request_counts}")
                return status_response

            elif status in ["canceling", "canceled"]:
                raise Exception(f"Batch was canceled")

            time.sleep(check_interval)

    def retrieve_results(self):
        """Download and parse batch results"""
        if not self.batch_id:
            raise ValueError("No batch ID set")

        results_response = self.client.beta.messages.batches.results(
            batch_id=self.batch_id
        )

        # Parse JSONL results
        results = {}
        for line in results_response.text.strip().split('\n'):
            result = json.loads(line)

            custom_id = result["custom_id"]

            if result["result"]["type"] == "succeeded":
                message = result["result"]["message"]
                content = message["content"][0]["text"]

                # Parse JSON response
                try:
                    parsed_data = json.loads(content)
                    results[custom_id] = {
                        "success": True,
                        "data": parsed_data,
                        "usage": message["usage"]
                    }
                except json.JSONDecodeError:
                    results[custom_id] = {
                        "success": False,
                        "error": "Failed to parse JSON response",
                        "raw_content": content
                    }

            else:
                results[custom_id] = {
                    "success": False,
                    "error": result["result"].get("error", "Unknown error")
                }

        return results

    def process_statements(self, statement_paths):
        """Complete workflow: upload → batch → wait → retrieve"""

        # Step 1: Upload files
        print(f"\n{'='*60}")
        print("Step 1: Uploading statements to Files API")
        print(f"{'='*60}")
        file_ids = self.upload_statements(statement_paths)

        # Step 2: Create batch
        print(f"\n{'='*60}")
        print("Step 2: Creating batch processing request")
        print(f"{'='*60}")

        extraction_prompt = """
Extract all positions from this portfolio statement and return as JSON.

Use this schema:
{
  "account": {
    "account_id": "string",
    "broker": "string",
    "statement_date": "YYYY-MM-DD"
  },
  "summary": {
    "total_value": number,
    "cash": number
  },
  "positions": [
    {
      "symbol": "string",
      "quantity": number,
      "current_value": number,
      "unrealized_gain_loss": number
    }
  ]
}

Validate all calculations and flag discrepancies.
"""

        self.create_batch(file_ids, extraction_prompt)

        # Step 3: Wait for completion
        print(f"\n{'='*60}")
        print("Step 3: Waiting for batch completion")
        print(f"{'='*60}")
        self.wait_for_completion(check_interval=30)

        # Step 4: Retrieve results
        print(f"\n{'='*60}")
        print("Step 4: Retrieving and parsing results")
        print(f"{'='*60}")
        results = self.retrieve_results()

        # Summary
        print(f"\n{'='*60}")
        print("RESULTS SUMMARY")
        print(f"{'='*60}")

        successful = sum(1 for r in results.values() if r["success"])
        failed = len(results) - successful

        print(f"Total statements: {len(results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")

        if failed > 0:
            print("\nFailed accounts:")
            for account_id, result in results.items():
                if not result["success"]:
                    print(f"  - {account_id}: {result['error']}")

        # Calculate total cost
        total_input_tokens = sum(
            r.get("usage", {}).get("input_tokens", 0)
            for r in results.values() if r["success"]
        )
        total_output_tokens = sum(
            r.get("usage", {}).get("output_tokens", 0)
            for r in results.values() if r["success"]
        )

        # Haiku batch pricing
        cost = (total_input_tokens / 1_000_000 * 0.50 +
                total_output_tokens / 1_000_000 * 2.50)

        print(f"\nToken usage:")
        print(f"  Input: {total_input_tokens:,}")
        print(f"  Output: {total_output_tokens:,}")
        print(f"  Total cost: ${cost:.2f}")

        return results


# Usage
if __name__ == "__main__":
    import os

    # Initialize processor
    processor = BatchPortfolioProcessor(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # List of portfolio statements to process
    statements = [
        "/data/portfolios/account_001_schwab.pdf",
        "/data/portfolios/account_002_fidelity.pdf",
        "/data/portfolios/account_003_ib.pdf",
        "/data/portfolios/account_004_etrade.pdf",
        "/data/portfolios/account_005_schwab.pdf",
    ]

    # Process all statements
    results = processor.process_statements(statements)

    # Save results
    output_file = f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")
```

---

## References & Resources

### Official Documentation

1. **Vision Capabilities**
   - https://docs.claude.com/en/docs/build-with-claude/vision
   - Image formats, size limits, best practices
   - Chart/graph reading capabilities

2. **PDF Processing**
   - https://docs.claude.com/en/docs/build-with-claude/pdf-support
   - Upload methods, document analysis
   - Financial report processing examples

3. **Batch Processing**
   - https://docs.claude.com/en/docs/build-with-claude/batch-processing
   - API endpoints, pricing, use cases
   - 100,000 requests/batch, 50% cost reduction

4. **Agent Skills**
   - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
   - Progressive disclosure architecture
   - Built-in document skills (xlsx, pptx, pdf, docx)

5. **Best Practices**
   - https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices
   - Skill design patterns, context management
   - Multi-modal integration guidelines

### Code Repositories

1. **Anthropic Cookbooks**
   - https://github.com/anthropics/anthropic-cookbook
   - Multi-modal workflows and examples
   - Sub-agent patterns, batch processing

2. **Claude Cookbooks (Skills)**
   - https://github.com/anthropics/claude-cookbooks/tree/main/skills
   - Skill authoring examples
   - Financial analysis templates

3. **Financial Data Analyst Quickstart**
   - https://github.com/anthropics/anthropic-quickstarts/tree/main/financial-data-analyst
   - Next.js implementation
   - Data visualization integration

4. **Claude-Flow**
   - https://github.com/ruvnet/claude-flow
   - Agent orchestration platform
   - Multi-agent swarm coordination

### Community Resources

1. **Awesome Claude Skills**
   - https://github.com/travisvn/awesome-claude-skills
   - Curated skill collection
   - Community implementations

2. **Claude Code Agents**
   - https://github.com/wshobson/agents
   - Automation and orchestration
   - Production workflow examples

### Financial Services Implementations

1. **Claude for Financial Services**
   - https://www.anthropic.com/news/claude-for-financial-services
   - Production use cases (NBIM, AIG)
   - ROI metrics and case studies

2. **AWS Financial Markets Blog**
   - https://aws.amazon.com/blogs/machine-learning/generative-ai-and-multi-modal-agents-in-aws-the-key-to-unlocking-new-value-in-financial-markets/
   - Multi-modal agent architecture
   - AWS integration patterns

### Additional Tools

1. **Files API Reference**
   - Upload, manage, retrieve documents
   - 500MB file size support
   - 29-day retention

2. **Message Batches API**
   - Asynchronous processing
   - Cost optimization strategies
   - Result management

3. **Prompt Caching**
   - 90% cost reduction on cached inputs
   - Multi-query optimization
   - Document reuse patterns

---

## Appendix: Quick Reference

### Model Selection Guide

| Task Type | Complexity | Urgency | Volume | Recommended Model | Use Batch? |
|-----------|-----------|---------|--------|------------------|-----------|
| PDF extraction | Low | Low | High (100+) | Haiku 4.5 | Yes |
| Chart analysis | Medium | Medium | Medium | Haiku 4.5 | No |
| Risk assessment | High | Low | Medium | Sonnet 4.5 | Yes |
| Real-time trading | High | High | Low | Sonnet 4.5 | No |
| Report generation | High | Medium | Medium | Sonnet 4.5 | No |
| Compliance check | Medium | Low | High (500+) | Haiku 4.5 | Yes |

### Cost Reference (Per Million Tokens)

| Model | Standard Input | Batch Input | Standard Output | Batch Output |
|-------|---------------|-------------|-----------------|--------------|
| Sonnet 4.5 | $3.00 | $1.50 | $15.00 | $7.50 |
| Haiku 4.5 | $1.00 | $0.50 | $5.00 | $2.50 |

### Token Calculation Formulas

**Images:**
```
tokens = (width_px × height_px) / 750
```

**PDFs:**
```
tokens_per_page = 1,500 to 3,000 (text) + image_tokens
```

**Optimization Target:**
```
optimal_image_size ≤ 1.15 megapixels (~1,500 tokens)
```

### API Endpoints

**Files API:**
- `POST /v1/files` - Upload file
- `GET /v1/files` - List files
- `GET /v1/files/{file_id}` - Get metadata
- `DELETE /v1/files/{file_id}` - Delete file

**Batch API:**
- `POST /v1/messages/batches` - Create batch
- `GET /v1/messages/batches/{batch_id}` - Get status
- `GET /v1/messages/batches/{batch_id}/results` - Download results

### Beta Headers Required

```python
betas = [
    "code-execution-2025-08-25",    # Code execution
    "files-api-2025-04-14",          # File operations
    "skills-2025-10-02"              # Skills feature
]
```

### Size Limits Quick Reference

| Resource | Limit |
|----------|-------|
| Image (API) | 5MB |
| Image (claude.ai) | 10MB |
| Image count (API) | 100 per request |
| Image count (claude.ai) | 20 per turn |
| PDF size | 32MB per request |
| PDF pages | 100 pages |
| Files API upload | 500MB per file |
| Batch size | 100,000 requests OR 256MB |
| Batch timeout | 24 hours |
| Results retention | 29 days |

---

**End of Research Document**

*This comprehensive research provides a foundation for implementing robust multi-modal document processing workflows in the Portfolio Validation Engine, leveraging Claude's vision, PDF analysis, batch processing, and agent orchestration capabilities.*
