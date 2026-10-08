from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
IGNORED_PARTS = {".git", ".idea", "bin", "obj", "specs"}


def project_files(pattern: str) -> list[Path]:
    return sorted(
        path
        for path in ROOT.glob(pattern)
        if path.is_file() and not IGNORED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


def combined_text(patterns: tuple[str, ...], *, lower: bool = False) -> str:
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for pattern in patterns
        for path in project_files(pattern)
    )
    return text.lower() if lower else text


def service_environment(service: dict) -> dict[str, str]:
    environment = service.get("environment", {})
    if isinstance(environment, dict):
        return {str(key): str(value) for key, value in environment.items()}

    result = {}
    for entry in environment:
        key, _, value = str(entry).partition("=")
        result[key] = value
    return result


@pytest.fixture(scope="session")
def project_file() -> Path:
    candidates = project_files("**/*.csproj")
    assert candidates, "No .NET project file was found"
    web_projects = [
        path
        for path in candidates
        if "microsoft.net.sdk.web" in path.read_text(encoding="utf-8").lower()
    ]
    assert len(web_projects) == 1, "Expected exactly one ASP.NET Core web project"
    return web_projects[0]


@pytest.fixture(scope="session")
def csharp_source() -> str:
    return combined_text(("**/*.cs", "**/*.cshtml"))


@pytest.fixture(scope="session")
def csharp_source_lower(csharp_source: str) -> str:
    return csharp_source.lower()


@pytest.fixture(scope="session")
def compose() -> dict:
    path = ROOT / "compose.yaml"
    assert path.is_file(), "compose.yaml is missing"
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict), "compose.yaml must contain a YAML mapping"
    assert isinstance(document.get("services"), dict), "compose.yaml must define services"
    return document


@pytest.fixture(scope="session")
def json_settings() -> list[tuple[Path, dict]]:
    settings = []
    for path in project_files("**/appsettings*.json"):
        settings.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return settings
