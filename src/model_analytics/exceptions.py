"""Public exception hierarchy for model_analytics."""


class ModelAnalyticsError(Exception):
    """Base exception for all model_analytics errors."""


class ConfigurationError(ModelAnalyticsError):
    """Raised when configuration is missing or invalid."""


class DependencyError(ModelAnalyticsError):
    """Raised when a required optional dependency is unavailable."""
