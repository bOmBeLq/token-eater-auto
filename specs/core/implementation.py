from conftest import ROOT, project_files


def test_application_required_by_spec_tests_is_implemented():
    assert project_files("**/*.csproj"), "The ASP.NET Core project is missing"
    assert (ROOT / "Program.cs").is_file(), "The application entry point is missing"
    assert project_files("**/Controllers/*Controller.cs"), "MVC controllers are missing"
    assert project_files("**/Views/**/*.cshtml"), "MVC views are missing"


def test_complete_specification_suite_is_configured():
    config = (ROOT / "pytest.ini").read_text(encoding="utf-8")
    assert "testpaths = specs" in config


def test_local_artifacts_and_credentials_are_ignored_by_git():
    content = (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
    for entry in ("bin/", "obj/", ".venv/", ".idea/", ".pytest_cache/", ".env"):
        assert entry in content
