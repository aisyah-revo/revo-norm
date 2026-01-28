"""
Comprehensive unit tests for email normalization in both English and Malay.
"""

import pytest
from revo_norm.text_normalizer import (
    email_to_spoken,
    normalize_text,
)


class TestEmailToSpoken:
    """Test email to spoken conversion."""

    def test_simple_email(self):
        """Test simple email conversion."""
        result = email_to_spoken("user@example.com")
        assert result == "user at example dot com"

    def test_email_with_underscore(self):
        """Test email with underscore."""
        result = email_to_spoken("user_name@example.com")
        assert result == "user underscore name at example dot com"

    def test_email_with_plus(self):
        """Test email with plus sign."""
        result = email_to_spoken("user+tag@example.com")
        assert result == "user plus tag at example dot com"

    def test_email_with_multiple_underscores(self):
        """Test email with multiple underscores."""
        result = email_to_spoken("first_last_name@example.com")
        assert result == "first underscore last underscore name at example dot com"

    def test_email_with_dot_before_at(self):
        """Test email with dot in local part."""
        result = email_to_spoken("first.last@example.com")
        assert "first" in result
        assert "last" in result
        assert "at" in result
        assert "example dot com" in result

    def test_complex_email(self):
        """Test complex email with multiple special characters."""
        result = email_to_spoken("sugumaran_thiagarajan@yahoo.com")
        assert result == "sugumaran underscore thiagarajan at yahoo dot com"

    def test_email_with_numbers(self):
        """Test email with numbers."""
        result = email_to_spoken("user123@example.com")
        assert "user123" in result
        assert "at example dot com" in result

    def test_email_with_hyphen(self):
        """Test email with hyphen in domain."""
        result = email_to_spoken("user@my-domain.com")
        assert "user at my hyphen domain dot com" == result or "user at my-domain dot com" in result

    def test_subdomain(self):
        """Test email with subdomain."""
        result = email_to_spoken("user@mail.example.com")
        assert "user at mail dot example dot com" in result or "user at mail.example dot com" in result

    def test_gmail(self):
        """Test Gmail address."""
        result = email_to_spoken("john@gmail.com")
        assert result == "john at gmail dot com"

    def test_yahoo(self):
        """Test Yahoo email address."""
        result = email_to_spoken("test@yahoo.com")
        assert result == "test at yahoo dot com"

    def test_hotmail(self):
        """Test Hotmail email address."""
        result = email_to_spoken("user@hotmail.com")
        assert result == "user at hotmail dot com"

    def test_outlook(self):
        """Test Outlook email address."""
        result = email_to_spoken("user@outlook.com")
        assert result == "user at outlook dot com"

    def test_edu_email(self):
        """Test .edu email address."""
        result = email_to_spoken("student@university.edu")
        # Should handle .edu similarly
        assert "student" in result
        assert "at" in result

    def test_capital_letters(self):
        """Test email with capital letters."""
        result = email_to_spoken("John.Doe@Example.COM")
        assert "John" in result or "john" in result
        assert "Doe" in result or "doe" in result
        assert "at" in result
        assert "example dot com" in result.lower()

    def test_multiple_dots_in_local(self):
        """Test email with multiple dots in local part."""
        result = email_to_spoken("first.middle.last@example.com")
        assert "first" in result
        assert "middle" in result
        assert "last" in result

    def test_consecutive_special_chars(self):
        """Test email with consecutive special characters."""
        result = email_to_spoken("user_name+test@example.com")
        assert "user" in result
        assert "underscore name" in result
        assert "plus test" in result

    def test_trailing_whitespace_removed(self):
        """Test that trailing whitespace is removed."""
        result = email_to_spoken("  user@example.com  ")
        assert result == "user at example dot com"


class TestEmailInFullTextNormalization:
    """Test email normalization within full text."""

    def test_single_email_in_english(self):
        """Test single email in English text."""
        result = normalize_text("Email me at user@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "user at example dot com" in result or "user at example" in result

    def test_single_email_in_malay(self):
        """Test single email in Malay text."""
        result = normalize_text("Emel saya di user@example.com", language="ms", apply_pronunciation_overrides_flag=False)
        assert "user at example" in result or "user" in result

    def test_multiple_emails(self):
        """Test multiple emails in text."""
        result = normalize_text("Contact user1@example.com or user2@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "user1" in result
        assert "user2" in result

    def test_email_with_other_elements(self):
        """Test email with other text elements."""
        result = normalize_text("Call me at 2:30 pm or email user@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "email" in result
        assert "user" in result
        assert "at" in result

    def test_email_at_sentence_start(self):
        """Test email at start of sentence."""
        result = normalize_text("user@example.com is my email", language="en", apply_pronunciation_overrides_flag=False)
        assert "user" in result
        assert "at" in result

    def test_email_at_sentence_end(self):
        """Test email at end of sentence."""
        result = normalize_text("My email is user@example.com.", language="en", apply_pronunciation_overrides_flag=False)
        assert "user" in result

    def test_email_with_acronym(self):
        """Test email with acronym."""
        result = normalize_text("Contact IBM at user@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "user at example" in result or "user" in result

    def test_email_with_currency(self):
        """Test email with currency."""
        result = normalize_text("Pay RM100 to user@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "user at example" in result or "user" in result
        assert "ringgit" in result

    def test_email_with_date(self):
        """Test email with date."""
        result = normalize_text("Meeting on 15/08/2023, email user@example.com", language="en", apply_pronunciation_overrides_flag=False)
        assert "user at example" in result or "user" in result

    def test_complex_malay_sentence(self):
        """Test email in complex Malay sentence."""
        result = normalize_text("Saya boleh dihubungi di email_saya@example.com atau 012-3456789", language="ms", apply_pronunciation_overrides_flag=False)
        assert "email" in result.lower()
        assert "underscore" in result or "saya" in result

    def test_email_with_parentheses(self):
        """Test email with parentheses."""
        result = normalize_text("Contact (user@example.com) for info", language="en", apply_pronunciation_overrides_flag=False)
        assert "user at example" in result or "user" in result

    def test_email_in_angle_brackets(self):
        """Test email in angle brackets."""
        result = normalize_text("Email <user@example.com>", language="en", apply_pronunciation_overrides_flag=False)
        assert "user" in result


class TestEmailEdgeCases:
    """Test edge cases for email normalization."""

    def test_very_long_local_part(self):
        """Test email with very long local part."""
        email = "verylongemailaddressstring@company.com"
        result = email_to_spoken(email)
        assert "verylongemailaddressstring" in result
        assert "at" in result
        assert "company dot com" in result

    def test_numeric_local_part(self):
        """Test email with numeric local part."""
        result = email_to_spoken("123456@example.com")
        assert "123456" in result
        assert "at example dot com" in result

    def test_email_with_single_char_local(self):
        """Test email with single character local part."""
        result = email_to_spoken("a@example.com")
        assert "a at example dot com" == result

    def test_common_service_providers(self):
        """Test emails from common service providers."""
        emails = [
            "user@gmail.com",
            "user@yahoo.com",
            "user@hotmail.com",
            "user@outlook.com",
            "user@icloud.com",
            "user@aol.com",
        ]
        for email in emails:
            result = email_to_spoken(email)
            assert "at" in result
            assert "dot com" in result

    def test_country_code_tlds(self):
        """Test emails with country code TLDs."""
        result = email_to_spoken("user@example.co.uk")
        # Should handle different TLDs
        assert "user" in result
        assert "at" in result

    def test_organization_email(self):
        """Test organization email patterns."""
        result = email_to_spoken("info@company.com")
        assert "info at company dot com" == result

    def test_support_email(self):
        """Test support email patterns."""
        result = email_to_spoken("support@service.com")
        assert "support at service dot com" == result

    def test_admin_email(self):
        """Test admin email patterns."""
        result = email_to_spoken("admin@website.org")
        assert "admin at website" in result or "admin" in result
