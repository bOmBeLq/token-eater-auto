import re
import xml.etree.ElementTree as ET

from conftest import ROOT, project_files


def test_project_is_aspnet_core_web_targeting_net_10(project_file):
    root = ET.parse(project_file).getroot()
    assert root.attrib.get("Sdk", "").lower() == "microsoft.net.sdk.web"
    frameworks = [node.text for node in root.iter("TargetFramework")]
    assert "net10.0" in frameworks


def test_project_uses_server_rendered_mvc(csharp_source_lower):
    assert "addcontrollerswithviews" in csharp_source_lower
    assert "mapcontrollerroute" in csharp_source_lower
    assert project_files("**/Controllers/*Controller.cs"), "MVC controllers are missing"
    assert project_files("**/Views/**/*.cshtml"), "Server-rendered Razor views are missing"


def test_interface_declares_english_language():
    layouts = project_files("**/Views/Shared/_Layout.cshtml")
    assert layouts, "The shared MVC layout is missing"
    layout = layouts[0].read_text(encoding="utf-8", errors="ignore")
    assert re.search(r'<html[^>]+lang=["\']en(?:-[A-Za-z]+)?["\']', layout, re.I)


def test_credentials_are_not_hardcoded_in_csharp_or_appsettings(json_settings):
    csharp = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in project_files("**/*.cs")
    )
    assignments = re.findall(
        r"(?:password|secret|api[_]?key)\s*=\s*\"([^\"]+)\"",
        csharp,
        re.I,
    )
    assert not assignments, "Credentials must come from configuration, not C# literals"

    def values(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                yield str(key), nested
                yield from values(nested)
        elif isinstance(value, list):
            for nested in value:
                yield from values(nested)

    for path, document in json_settings:
        for key, value in values(document):
            if key.lower() in {"password", "secret", "apikey", "api_key"}:
                assert value in (None, ""), f"Hardcoded credential found in {path.relative_to(ROOT)}"
            if key.lower() == "connectionstrings" and isinstance(value, dict):
                assert all("password=" not in str(item).lower() for item in value.values())
