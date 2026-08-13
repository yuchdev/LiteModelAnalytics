# Model Domain Concepts

The catalog layer normalizes provider metadata into immutable domain objects.

## Identity

- `ModelIdentity` separates provider/model identifiers from display names.
- `ModelEndpoint` captures endpoint-specific information.
- Canonical IDs are stable and provider-scoped (`provider:model_id`).

## Capabilities

Capabilities use tri-state support values:

- `SUPPORTED`
- `UNSUPPORTED`
- `UNKNOWN`

Missing source fields stay `UNKNOWN`; omitted fields are never inferred as unsupported.

## Aggregate

`ModelProfile` is the normalized aggregate consumed by application and selection layers. It stores:

- identity and endpoints
- capabilities
- pricing
- source/provenance metadata
- retrieval timestamp and raw references
