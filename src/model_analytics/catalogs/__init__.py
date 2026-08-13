"""Catalog adapters and service facade."""

from model_analytics.catalogs.exceptions import (
    CatalogCacheError,
    CatalogError,
    CatalogFetchError,
    CatalogParseError,
)
from model_analytics.catalogs.litellm import LiteLLMCatalogAdapter
from model_analytics.catalogs.merge import merge_catalog_snapshots
from model_analytics.catalogs.openrouter import OpenRouterCatalogAdapter
from model_analytics.catalogs.protocols import CatalogProvider
from model_analytics.catalogs.service import CatalogService

__all__ = [
    "CatalogCacheError",
    "CatalogError",
    "CatalogFetchError",
    "CatalogParseError",
    "CatalogProvider",
    "CatalogService",
    "LiteLLMCatalogAdapter",
    "OpenRouterCatalogAdapter",
    "merge_catalog_snapshots",
]
