"""Package import and public API smoke tests."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

import model_analytics
from model_analytics import (
    ConfigurationError,
    DependencyError,
    ModelAnalyticsError,
    __version__,
)
from model_analytics.cli.app import app
from model_analytics.config import AppPaths, default_paths

runner = CliRunner()


@pytest.mark.unit
def test_import() -> None:
    """Package imports without error."""
    assert model_analytics is not None


@pytest.mark.unit
def test_version_is_string() -> None:
    """__version__ is a non-empty string."""
    assert isinstance(__version__, str)
    assert __version__


@pytest.mark.unit
def test_exception_hierarchy() -> None:
    """Public exceptions are correctly related."""
    assert issubclass(ConfigurationError, ModelAnalyticsError)
    assert issubclass(DependencyError, ModelAnalyticsError)
    assert issubclass(ModelAnalyticsError, Exception)


@pytest.mark.unit
def test_cli_help() -> None:
    """CLI --help exits 0."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "model-analytics" in result.output.lower() or "usage" in result.output.lower()


@pytest.mark.unit
def test_cli_version() -> None:
    """CLI version prints the version string."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output


@pytest.mark.unit
def test_cli_doctor_table() -> None:
    """CLI doctor default table output exits 0 and reports the version."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "doctor" in result.output.lower()


@pytest.mark.unit
def test_cli_doctor_json() -> None:
    """CLI doctor --format json emits valid JSON with required keys."""
    result = runner.invoke(app, ["doctor", "--format", "json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "schema_version" in data
    assert "package_version" in data
    assert "python_version" in data
    assert "platform" in data
    assert "litellm_available" in data
    assert "paths" in data
    paths_data = data["paths"]
    assert "config_dir" in paths_data
    assert "data_dir" in paths_data
    assert "cache_dir" in paths_data


@pytest.mark.unit
def test_cli_doctor_reports_litellm_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """Doctor reports an unavailable LiteLLM instead of crashing."""
    import builtins

    real_import = builtins.__import__

    def fake_import(name: str, *args: object, **kwargs: object) -> object:
        if name == "litellm":
            raise ImportError("litellm is not installed")
        return real_import(name, *args, **kwargs)  # type: ignore[arg-type]

    monkeypatch.delitem(sys.modules, "litellm", raising=False)
    monkeypatch.setattr(builtins, "__import__", fake_import)

    json_result = runner.invoke(app, ["doctor", "--format", "json"])
    table_result = runner.invoke(app, ["doctor"])

    assert json_result.exit_code == 0
    data = json.loads(json_result.output)
    assert data["litellm_available"] is False
    assert data["litellm_error"]
    assert table_result.exit_code == 0


@pytest.mark.unit
def test_doctor_json_no_secrets() -> None:
    """Doctor JSON output must not contain known secret environment variable values."""
    secret_vars = ["OPENROUTER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    for var in secret_vars:
        secret_value = os.environ.get(var, "")
        if not secret_value:
            continue
        result = runner.invoke(app, ["doctor", "--format", "json"])
        assert secret_value not in result.output, f"Secret {var} found in doctor output"


@pytest.mark.unit
def test_import_does_not_create_dirs(tmp_path: Path) -> None:
    """Importing model_analytics does not create user config/data/cache directories."""
    env = dict(os.environ)
    env["HOME"] = str(tmp_path)
    env["XDG_CONFIG_HOME"] = str(tmp_path / "config")
    env["XDG_DATA_HOME"] = str(tmp_path / "data")
    env["XDG_CACHE_HOME"] = str(tmp_path / "cache")

    code = "import model_analytics, model_analytics.config as c; c.default_paths()"
    completed = subprocess.run(
        [sys.executable, "-c", code],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert not (tmp_path / "config").exists()
    assert not (tmp_path / "data").exists()
    assert not (tmp_path / "cache").exists()


@pytest.mark.unit
def test_application_module_imports() -> None:
    """The application facade module imports without side effects."""
    from model_analytics import application

    assert application is not None


@pytest.mark.unit
def test_default_paths_returns_app_paths() -> None:
    """default_paths() returns an AppPaths instance with Path attributes."""
    paths = default_paths()
    assert isinstance(paths, AppPaths)
    assert isinstance(paths.config_dir, Path)
    assert isinstance(paths.data_dir, Path)
    assert isinstance(paths.cache_dir, Path)
