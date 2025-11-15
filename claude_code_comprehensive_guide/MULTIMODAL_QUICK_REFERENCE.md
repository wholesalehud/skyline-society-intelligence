# Multi-Modal Quick Reference Guide

**Quick access guide for multi-modal document processing capabilities**

---

## Key Capabilities at a Glance

### Vision
- **Formats:** JPEG, PNG, GIF, WebP
- **Max Size:** 5MB (API), 10MB (claude.ai)
- **Resolution:** Up to 8000×8000px (20 images), 2000×2000px (21-100 images)
- **Optimal:** ≤1.15 megapixels (~1,500 tokens)
- **Token Formula:** `(width × height) / 750`

### PDF Processing
- **Max Size:** 32MB per request
- **Max Pages:** 100 pages
- **Processing:** Dual text + image analysis
- **Cost:** 1,500-3,000 tokens/page (text) + image tokens

### Batch Processing
- **Capacity:** 100,000 requests OR 256MB per batch
- **Discount:** 50% off standard pricing
- **Completion:** <24 hours (most <1 hour)
- **Retention:** 29 days

### Files API
- **Max Size:** 500MB per file
- **Retention:** 29 days
- **Formats:** PDF, DOCX, TXT, CSV, TSV, HTML, RTF, EPUB, images

---

## Cost Reference (Per Million Tokens)

| Model | Standard Input | Batch Input | Standard Output | Batch Output |
|-------|---------------|-------------|-----------------|--------------|
| **Sonnet 4.5** | $3.00 | $1.50 | $15.00 | $7.50 |
| **Haiku 4.5** | $1.00 | $0.50 | $5.00 | $2.50 |

---

## Common Use Cases

### Portfolio Statement Processing
```python
# Upload PDF
file_id = file_manager.upload_document("statement.pdf")

# Extract positions
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {"type": "file", "file_id": file_id}},
            {"type": "text", "text": "Extract all positions as JSON"}
        ]
    }]
)
```

### Chart Analysis
```python
# Encode image
with open("chart.png", "rb") as f:
    img_data = base64.b64encode(f.read()).decode('utf-8')

# Analyze
response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_data}},
            {"type": "text", "text": "Analyze technical indicators and provide trading signals"}
        ]
    }]
)
```

### Batch Processing
```python
# Create batch
batch = client.beta.messages.batches.create(
    requests=[{
        "custom_id": "doc_1",
        "params": {
            "model": "claude-haiku-4-5",
            "max_tokens": 4096,
            "messages": [...]
        }
    }]
)

# Wait and retrieve
results = client.beta.messages.batches.results(batch_id=batch.id)
```

---

## Model Selection Decision Tree

```
Is it urgent (real-time)?
├─ Yes → Use standard API
│   ├─ Complex analysis? → Sonnet 4.5
│   └─ Simple extraction? → Haiku 4.5
└─ No → Can wait up to 24 hours?
    └─ Yes → Use Batch API (50% discount)
        ├─ Complex analysis? → Sonnet 4.5 Batch
        └─ Simple extraction? → Haiku 4.5 Batch
```

---

## Performance Tips

1. **Image Optimization**
   - Resize to ~1.15MP before upload
   - Use 1:1 aspect ratio (1092×1092px)
   - Save with 85-90% quality

2. **PDF Optimization**
   - Extract only relevant pages
   - Use PDF text layer when available
   - Split documents >100 pages

3. **Batch Processing**
   - Use for volumes >50 documents
   - Group similar tasks together
   - Monitor completion via polling

4. **Prompt Caching**
   - Enable for repeated document analysis
   - 90% cost reduction on cached inputs
   - Cache large documents/instructions

---

## Required Beta Headers

```python
betas = [
    "code-execution-2025-08-25",    # Code execution
    "files-api-2025-04-14",          # File operations
    "skills-2025-10-02"              # Skills feature
]
```

---

## Error Handling

```python
try:
    response = client.messages.create(...)
except anthropic.APIError as e:
    if e.status_code == 429:
        # Rate limit - retry with backoff
        time.sleep(60)
    elif e.status_code == 400:
        # Invalid request - check parameters
        print(f"Invalid request: {e}")
    else:
        # Other error
        raise
```

---

## Cost Estimation Examples

### Single Portfolio Analysis
- 30-page PDF: 60,000 tokens input
- Analysis: 2,000 tokens output
- Model: Haiku 4.5 (standard)
- **Cost:** (60k × $1.00/M) + (2k × $5.00/M) = $0.07

### Batch Processing (100 portfolios)
- 100 × 60,000 = 6M tokens input
- 100 × 2,000 = 200k tokens output
- Model: Haiku 4.5 (batch)
- **Cost:** (6M × $0.50/M) + (200k × $2.50/M) = $3.50

### Chart Analysis (single)
- 1500 tokens per chart
- 500 tokens output
- Model: Haiku 4.5 (standard)
- **Cost:** (1.5k × $1.00/M) + (0.5k × $5.00/M) = $0.0040

---

## Useful Links

**Documentation:**
- Vision: https://docs.claude.com/en/docs/build-with-claude/vision
- PDF: https://docs.claude.com/en/docs/build-with-claude/pdf-support
- Batch: https://docs.claude.com/en/docs/build-with-claude/batch-processing
- Skills: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview

**Code Examples:**
- Cookbooks: https://github.com/anthropics/anthropic-cookbook
- Skills: https://github.com/anthropics/claude-cookbooks/tree/main/skills
- Quickstarts: https://github.com/anthropics/anthropic-quickstarts

**Tools:**
- Claude-Flow: https://github.com/ruvnet/claude-flow
- Awesome Skills: https://github.com/travisvn/awesome-claude-skills

---

## Portfolio Validation Engine Integration

### Files Created
1. `MULTIMODAL_WORKFLOWS_RESEARCH.md` - Complete research (100+ pages)
2. `MULTIMODAL_IMPLEMENTATION_PLAN.md` - 10-week implementation roadmap
3. `MULTIMODAL_QUICK_REFERENCE.md` - This quick reference

### Recommended Skills to Create
1. `portfolio_processor` - Extract positions from broker statements
2. `market_validator` - Validate against market data (exists)
3. `risk_assessor` - Calculate risk metrics (exists)
4. `technical_analyzer` - Analyze charts for signals
5. `trade_ticket_generator` - Generate final reports

### Estimated Costs
- **Per portfolio:** $0.21
- **Monthly (100 portfolios):** $21
- **Annual:** $252
- **ROI vs manual:** $239,748 savings/year

---

**Version:** 1.0
**Last Updated:** 2025-10-26
