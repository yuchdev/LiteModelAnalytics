"""Model Analytics — request-aware LLM model analytics, comparison, and selection."""

from importlib.metadata import PackageNotFoundError, version

from model_analytics.exceptions import (
    ConfigurationError,
    DependencyError,
    ModelAnalyticsError,
)

try:
    __version__: str = version("model-analytics")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0.dev0"

from model_analytics.application import analytics

__all__ = [
    "ConfigurationError",
    "DependencyError",
    "ModelAnalyticsError",
    "analytics",
    "__version__",
]
