import re

from conftest import project_files


def _texts(pattern):
    return [path.read_text(encoding="utf-8", errors="ignore") for path in project_files(pattern)]


def test_login_redirects_to_protected_dashboard(csharp_source_lower):
    assert "dashboardcontroller" in csharp_source_lower
    assert re.search(r"redirecttoaction\s*\([^)]*dashboard", csharp_source_lower)
    dashboard_sources = "\n".join(_texts("**/Controllers/*Dashboard*Controller.cs"))
    assert re.search(r"\[Authorize(?:Attribute)?(?:\([^]]*\))?\]", dashboard_sources, re.I)


def test_dashboard_greets_user_and_links_to_profile():
    views = _texts("**/Views/Dashboard/*.cshtml")
    assert views, "Dashboard view is missing"
    content = "\n".join(views)
    assert re.search(r"welcome|hello", content, re.I)
    assert re.search(r"asp-(?:controller|action)=[\"'][^\"']*profile", content, re.I)


def test_profile_is_protected_and_displays_current_email(csharp_source_lower):
    profile_sources = "\n".join(_texts("**/Controllers/*Profile*Controller.cs"))
    assert profile_sources, "Profile controller is missing"
    assert re.search(r"\[Authorize(?:Attribute)?(?:\([^]]*\))?\]", profile_sources, re.I)
    assert re.search(r"getuserasync|findbyidasync", profile_sources, re.I)
    profile_views = "\n".join(_texts("**/Views/Profile/*.cshtml"))
    assert re.search(r"email", profile_views, re.I)


def test_navigation_exposes_post_only_logout():
    layouts = _texts("**/Views/Shared/_Layout.cshtml")
    assert layouts, "Shared layout is missing"
    layout = "\n".join(layouts)
    assert re.search(r"<form[^>]+(?:logout|asp-action=[\"']Logout)", layout, re.I)
    assert re.search(r"<button[^>]*>[^<]*(?:log\s*out|sign\s*out)", layout, re.I)
