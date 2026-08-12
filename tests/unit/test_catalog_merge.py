from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from model_analytics.catalogs.merge import merge_catalog_snapshots
from model_analytics.domain import (
    CatalogSnapshot,
    CatalogSource,
    ModelCapabilities,
    ModelIdentity,
    ModelProfile,
    PriceComponent,
    Pricing,
    PricingProvenance,
    SupportStatus,
    canonical_model_id,
)


def _profile(
    *,
    provider: str,
    model_id: str,
    source_name: str,
    authoritative: bool,
    prompt_price: str | None,
    tools: SupportStatus,
) -> ModelProfile:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    canonical = canonical_model_id(provider, model_id)
    components = {}
    provenance = {}
    if prompt_price is not None:
        components["prompt"] = PriceComponent(key="prompt", amount=prompt_price)
        provenance["prompt"] = source_name

    return ModelProfile(
        identity=ModelIdentity(provider=provider, model_id=model_id, canonical_id=canonical),
        capabilities=ModelCapabilities(tools=tools),
        pricing=Pricing(
            components=components,
            provenance=PricingProvenance(source_by_key=provenance),
        ),
        sources=(
            CatalogSource(
                name=source_name,
                retrieved_at=now,
                authoritative=authoritative,
            ),
        ),
        retrieved_at=now,
    )


@pytest.mark.unit
def test_merge_fills_unknown_capabilities_from_secondary() -> None:
    primary = _profile(
        provider="openrouter",
        model_id="x",
        source_name="openrouter",
        authoritative=True,
        prompt_price="1",
        tools=SupportStatus.UNKNOWN,
    )
    secondary = _profile(
        provider="openrouter",
        model_id="x",
        source_name="litellm",
        authoritative=False,
        prompt_price=None,
        tools=SupportStatus.SUPPORTED,
    )

    merged = merge_catalog_snapshots(
        CatalogSnapshot(
            models={primary.identity.canonical_id: primary},
            sources=primary.sources,
            retrieved_at=primary.retrieved_at,
        ),
        CatalogSnapshot(
            models={secondary.identity.canonical_id: secondary},
            sources=secondary.sources,
            retrieved_at=secondary.retrieved_at,
        ),
    ).snapshot

    profile = merged.models[primary.identity.canonical_id]
    assert profile.capabilities.tools == SupportStatus.SUPPORTED


@pytest.mark.unit
def test_merge_keeps_authoritative_pricing_and_records_conflict() -> None:
    primary = _profile(
        provider="openrouter",
        model_id="x",
        source_name="openrouter",
        authoritative=True,
        prompt_price="1",
        tools=SupportStatus.UNKNOWN,
    )
    secondary = _profile(
        provider="openrouter",
        model_id="x",
        source_name="litellm",
        authoritative=False,
        prompt_price="2",
        tools=SupportStatus.UNKNOWN,
    )

    result = merge_catalog_snapshots(
        CatalogSnapshot(
            models={primary.identity.canonical_id: primary},
            sources=primary.sources,
            retrieved_at=primary.retrieved_at,
        ),
        CatalogSnapshot(
            models={secondary.identity.canonical_id: secondary},
            sources=secondary.sources,
            retrieved_at=secondary.retrieved_at,
        ),
    )

    profile = result.snapshot.models[primary.identity.canonical_id]
    assert profile.pricing.components["prompt"].amount == Decimal("1")
    assert result.conflicts[primary.identity.canonical_id]["pricing"]["prompt"]
