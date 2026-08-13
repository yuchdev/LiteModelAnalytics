# Pricing Concepts

All pricing values use `decimal.Decimal`.

## Components

`Pricing` stores normalized `PriceComponent` entries for known keys (prompt, completion, request, image, audio, web_search, internal_reasoning, input_cache_read, input_cache_write) and preserves unknown future keys.

## Overrides

`PricingOverride` supports conditional replacement by:

- prompt-token threshold (`prompt_tokens_gte`)
- UTC windows (`utc_window_start`, `utc_window_end`)

Rules:

- overrides can replace only some keys
- absent keys inherit current/base values
- later applicable overrides win per key
- clock injection enables deterministic boundary tests

## Provenance

`PricingProvenance` tracks per-key source and disagreements when sources conflict.
