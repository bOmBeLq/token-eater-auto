from pathlib import Path

from conftest import ROOT


def test_every_markdown_specification_has_matching_python_tests():
    markdown_specs = sorted((ROOT / "specs").glob("**/*.md"))
    assert markdown_specs, "No Markdown specifications found"
    missing = [path.with_suffix(".py") for path in markdown_specs if not path.with_suffix(".py").is_file()]
    assert not missing, "Missing test files: " + ", ".join(
        str(path.relative_to(ROOT)) for path in missing
    )


def test_pytest_is_configured_to_collect_spec_files():
    config = ROOT / "pytest.ini"
    assert config.is_file(), "pytest.ini is missing"
    content = config.read_text(encoding="utf-8", errors="ignore").lower()
    assert "testpaths" in content and "specs" in content
    assert "python_files" in content and "*.py" in content


def test_test_dependencies_are_declared():
    requirements = ROOT / "requirements-test.txt"
    assert requirements.is_file(), "requirements-test.txt is missing"
    dependencies = requirements.read_text(encoding="utf-8", errors="ignore").lower()
    assert "pytest" in dependencies
    assert "pyyaml" in dependencies
