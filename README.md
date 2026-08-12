# Model Analytics

> **Warning:** Model recommendations produced by this tool are evidence-based estimates, not guarantees. Always validate model choices for your specific workload.

A production-quality Python library and CLI for **request-aware LLM model analytics, comparison, and selection**.

## What it does

Model Analytics provides:

- OpenRouter and LiteLLM catalog ingestion and normalization
- Pricing normalization and cost estimation (with Decimal precision)
- Request requirements and capability matching
- Quality evidence and benchmark results
- Latency and reliability observations
- Constrained model selection (cheapest/best/fastest/most-reliable/cost-efficient)
- Pareto-frontier analysis
- Explanations of why a model was selected or rejected
- Local persistent analytics storage (SQLite)
- CLI access to all stable capabilities

## Status

🚧 **Alpha — bootstrap skeleton only.** Core analytics functionality is not yet implemented.

## Install from source

```bash
git clone https://github.com/yuchdev/LiteModelAnalytics.git
cd LiteModelAnalytics
uv sync --all-groups
uv run model-analytics --help
```

## Development setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install
git clone https://github.com/yuchdev/LiteModelAnalytics.git
cd LiteModelAnalytics
uv sync --all-groups
```

## Quality commands

```bash
# Format check
uv run ruff format --check .

# Lint
uv run ruff check .

# Type check
uv run mypy src tests

# Tests (no live API calls)
uv run pytest -m "not live" --cov=model_analytics --cov-branch --cov-fail-under=90

# Docs build
uv run mkdocs build --strict

# Package build
uv build
```

## CLI

```bash
# Show help
model-analytics --help

# Show version
model-analytics version

# Environment health check
model-analytics doctor
model-analytics doctor --format json
```

## Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

**Note:** API keys are read from environment variables only. They are never persisted by this tool.
