import re
import xml.etree.ElementTree as ET


def _package_names(project_file):
    root = ET.parse(project_file).getroot()
    return {
        node.attrib.get("Include", "").lower()
        for node in root.iter("PackageReference")
    }


def test_identity_is_persisted_in_postgresql(project_file, csharp_source_lower):
    packages = _package_names(project_file)
    assert "microsoft.aspnetcore.identity.entityframeworkcore" in packages
    assert "npgsql.entityframeworkcore.postgresql" in packages
    assert "usenpgsql" in csharp_source_lower
    assert re.search(r"add(?:default)?identity(?:core)?", csharp_source_lower)


def test_registration_uses_unique_email_and_password(csharp_source_lower):
    assert "register" in csharp_source_lower
    assert "createasync" in csharp_source_lower
    assert re.search(r"requireuniqueemail\s*=\s*true", csharp_source_lower)
    assert re.search(r"\bemail\b", csharp_source_lower)
    assert re.search(r"\bpassword\b", csharp_source_lower)


def test_login_uses_email_and_identity_cookie(csharp_source_lower):
    assert "login" in csharp_source_lower
    assert "passwordsigninasync" in csharp_source_lower
    assert "configureapplicationcookie" in csharp_source_lower
    assert re.search(r"cookie\s*\.\s*httponly\s*=\s*true", csharp_source_lower)
    assert re.search(r"securepolicy\s*=\s*cookiesecurepolicy\.always", csharp_source_lower)


def test_user_can_log_out(csharp_source_lower):
    assert "logout" in csharp_source_lower
    assert "signoutasync" in csharp_source_lower
    assert "[httppost" in csharp_source_lower


def test_dashboard_and_profile_require_authentication(csharp_source_lower):
    assert "[authorize" in csharp_source_lower
    assert "dashboardcontroller" in csharp_source_lower
    assert "profile" in csharp_source_lower


def test_email_must_be_confirmed_before_login(csharp_source_lower):
    assert re.search(
        r"requireconfirmed(?:account|email)\s*=\s*true",
        csharp_source_lower,
    )
    assert "generateemailconfirmationtokenasync" in csharp_source_lower
    assert "confirmemailasync" in csharp_source_lower
    assert re.search(r"sendemailasync|smtpclient", csharp_source_lower)


def test_password_can_be_reset_via_one_time_email_link(csharp_source_lower):
    assert "forgotpassword" in csharp_source_lower
    assert "generatepasswordresettokenasync" in csharp_source_lower
    assert "resetpasswordasync" in csharp_source_lower
    assert re.search(r"sendemailasync|smtpclient", csharp_source_lower)


def test_forgot_password_does_not_disclose_account_existence(csharp_source_lower):
    assert "forgotpasswordconfirmation" in csharp_source_lower
    forbidden_messages = (
        "email does not exist",
        "user does not exist",
        "account not found",
        "email not found",
    )
    assert not any(message in csharp_source_lower for message in forbidden_messages)


def test_password_policy_requires_all_character_classes(csharp_source_lower):
    expected_settings = {
        "requiredlength": "8",
        "requiredigit": "true",
        "requirelowercase": "true",
        "requireuppercase": "true",
        "requirenonalphanumeric": "true",
    }
    for setting, value in expected_settings.items():
        assert re.search(rf"{setting}\s*=\s*{value}", csharp_source_lower), (
            f"Identity password option {setting} must be {value}"
        )
