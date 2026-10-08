import re

from conftest import ROOT, service_environment


def _service_with(services, predicate, description):
    matches = [service for service in services.values() if predicate(service)]
    assert matches, f"No {description} service found in compose.yaml"
    return matches[0]


def test_dockerfile_is_multistage_and_uses_dotnet_10():
    path = ROOT / "Dockerfile"
    assert path.is_file(), "Dockerfile is missing"
    content = path.read_text(encoding="utf-8", errors="ignore")
    from_lines = re.findall(r"^FROM\s+([^\s]+)", content, re.MULTILINE | re.IGNORECASE)
    assert len(from_lines) >= 2, "Dockerfile must use a multi-stage build"
    assert any("sdk:10" in image.lower() for image in from_lines)
    assert any("aspnet:10" in image.lower() for image in from_lines)
    assert re.search(r"\bdotnet\s+(?:publish|build)\b", content, re.I)


def test_compose_runs_application_postgres_and_mailpit(compose):
    services = compose["services"]
    _service_with(services, lambda item: "build" in item, "application")
    _service_with(
        services,
        lambda item: "postgres" in str(item.get("image", "")).lower(),
        "PostgreSQL",
    )
    mailpit = _service_with(
        services,
        lambda item: "mailpit" in str(item.get("image", "")).lower(),
        "Mailpit",
    )
    assert any("8025" in str(port) for port in mailpit.get("ports", [])), (
        "Mailpit web interface must be published"
    )


def test_postgres_data_is_persisted_in_a_named_volume(compose):
    postgres = _service_with(
        compose["services"],
        lambda item: "postgres" in str(item.get("image", "")).lower(),
        "PostgreSQL",
    )
    mounts = [str(item) for item in postgres.get("volumes", [])]
    assert any(":/var/lib/postgresql/data" in mount for mount in mounts)
    volume_names = {mount.split(":", 1)[0] for mount in mounts if ":" in mount}
    assert volume_names.intersection((compose.get("volumes") or {}).keys())


def test_application_waits_for_healthy_database(compose):
    services = compose["services"]
    app_name, app = next((name, item) for name, item in services.items() if "build" in item)
    db_name, database = next(
        (name, item)
        for name, item in services.items()
        if "postgres" in str(item.get("image", "")).lower()
    )
    assert database.get("healthcheck"), "PostgreSQL must define a health check"
    dependency = app.get("depends_on", {}).get(db_name)
    assert isinstance(dependency, dict) and dependency.get("condition") == "service_healthy", (
        f"{app_name} must wait until {db_name} is healthy"
    )


def test_application_applies_migrations_at_startup(csharp_source_lower):
    assert re.search(r"database\s*\.\s*migrate(?:async)?\s*\(", csharp_source_lower)


def test_database_and_smtp_settings_are_injected_into_application(compose):
    app = _service_with(compose["services"], lambda item: "build" in item, "application")
    environment = {key.lower(): value for key, value in service_environment(app).items()}
    assert any(key.startswith("connectionstrings__") for key in environment)
    assert any(key.startswith("smtp__") and key.endswith("host") for key in environment)


def test_local_test_environment_defines_postgres_password():
    environment_file = ROOT / ".env"
    assert environment_file.is_file(), ".env is missing"
    assert "POSTGRES_PASSWORD=gabi123" in environment_file.read_text(encoding="utf-8")


def test_application_is_published_on_local_port_8080(compose):
    application = _service_with(compose["services"], lambda item: "build" in item, "application")
    assert any("8080:8080" in str(port) for port in application.get("ports", []))
