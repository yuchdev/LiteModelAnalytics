"""Application facade — thin public entry point."""

from __future__ import annotations

from dataclasses import dataclass, field

from model_analytics.catalogs import CatalogService


@dataclass
class AnalyticsFacade:
    """Small public facade for application features."""

    catalog: CatalogService = field(default_factory=CatalogService)


analytics = AnalyticsFacade()

__all__ = ["AnalyticsFacade", "analytics"]
