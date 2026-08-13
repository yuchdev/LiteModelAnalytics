# Catalog Ingestion Guide

## Sources

- OpenRouter adapter (`/api/v1/models`) is authoritative for OpenRouter metadata/pricing.
- LiteLLM adapter is secondary/fallback metadata.

## Merge Rules

- OpenRouter pricing wins for fresh authoritative OpenRouter entries.
- LiteLLM can fill unknown capability fields.
- Conflicting values are retained in provenance metadata.
- Models are merged only by canonical identity, never by display name.

## Cache Behavior

OpenRouter snapshots are cached under platform cache paths with:

- cache format version
- fetched timestamp
- source URL
- raw payload
- normalized snapshot
- TTL metadata

Offline mode reads cache only; stale snapshots are explicitly marked.
Corrupt cache raises a clear error in offline mode and is ignored/refreshed in online mode.
