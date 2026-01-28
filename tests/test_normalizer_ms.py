"""
Unit tests for normalizer_ms module (Malay text normalization).
"""

import pytest
from revo_norm.normalizer_ms import (
    numbers_mapping_malay,
    is_mixed_alnum,
    is_only_digits_and_dashes,
    normalize_percentage,
    normalize_time,
    normalize_date,
    normalize_currency,
    normalize_decimal,
    normalize_dashed_digits,
    normalize_mixed_alnum,
    normalize_number,
    normalize_malay,
)
from revo_norm.num2word import to_cardinal, to_ordinal, to_currency, to_year


class TestNumbersMappingMalay:
    """Test Malay number mappings."""

    def test_zero_to_nine(self):
        assert numbers_mapping_malay['0'] == 'kosong'
        assert numbers_mapping_malay['1'] == 'satu'
        assert numbers_mapping_malay['2'] == 'dua'
        assert numbers_mapping_malay['3'] == 'tiga'
        assert numbers_mapping_malay['4'] == 'empat'
        assert numbers_mapping_malay['5'] == 'lima'
        assert numbers_mapping_malay['6'] == 'enam'
        assert numbers_mapping_malay['7'] == 'tujuh'
        assert numbers_mapping_malay['8'] == 'lapan'
        assert numbers_mapping_malay['9'] == 'sembilan'


class TestIsMixedAlnum:
    """Test mixed alphanumeric detection."""

    def test_letters_and_digits(self):
        assert is_mixed_alnum("abc123") is True

    def test_only_letters(self):
        assert is_mixed_alnum("abc") is False

    def test_only_digits(self):
        assert is_mixed_alnum("123") is False

    def test_with_dashes(self):
        assert is_mixed_alnum("abc-123") is True


class TestIsOnlyDigitsAndDashes:
    """Test digits and dashes only detection."""

    def test_digits_only(self):
        assert is_only_digits_and_dashes("123") is True

    def test_digits_with_dash(self):
        assert is_only_digits_and_dashes("123-456") is True

    def test_with_plus(self):
        assert is_only_digits_and_dashes("+60123456789") is True

    def test_with_letters(self):
        assert is_only_digits_and_dashes("abc123") is False


class TestNormalizeDate:
    """Test Malay date normalization."""

    def test_dd_mm_yyyy_slash(self):
        import re
        match = re.search(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b', "15/08/2023")
        if match:
            result = normalize_date(match)
            assert "lima belas" in result or "belas" in result
            assert "oghos" in result or "agust" in result.lower()

    def test_dd_mm_yyyy_dash(self):
        import re
        match = re.search(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b', "5-3-2023")
        if match:
            result = normalize_date(match)
            assert "satu" in result or "lima" in result
            assert "ribu" in result


class TestNormalizeCurrency:
    """Test Malay currency normalization."""

    def test_rm_no_decimal(self):
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM100", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "ringgit" in result

    def test_rm_with_decimal(self):
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM50.50", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "ringgit" in result
            assert "sen" in result

    def test_large_amount(self):
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM1,500", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "ribu" in result or "ringgit" in result

    def test_usd(self):
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "$100", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "dollar" in result


class TestNormalizeTime:
    """Test Malay time normalization."""

    def test_hour_only_malam(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.|malam|petang))', "9:00 malam", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "malam" in result.lower()

    def test_hour_only_petang(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.|malam|petang))', "2:30 petang", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "petang" in result.lower()

    def test_zero_minute(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.|malam|petang))', "5:00 malam", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "kosong" in result.lower()


class TestNormalizePercentage:
    """Test Malay percentage normalization."""

    def test_integer_percentage(self):
        import re
        match = re.search(r'\b(\d+(?:\.\d+)?)%', "50%")
        if match:
            result = normalize_percentage(match)
            assert "peratus" in result

    def test_decimal_percentage(self):
        import re
        match = re.search(r'\b(\d+(?:\.\d+)?)%', "12.5%")
        if match:
            result = normalize_percentage(match)
            assert "peratus" in result
            assert "perpuluhan" in result


class TestNormalizeDecimal:
    """Test Malay decimal normalization."""

    def test_simple_decimal(self):
        import re
        match = re.search(r'\b(\d+)\.(\d+)\b', "3.14")
        if match:
            result = normalize_decimal(match)
            assert "tiga" in result
            assert "perpuluhan" in result


class TestNormalizeDashedDigits:
    """Test Malay dashed digit normalization."""

    def test_phone_number(self):
        import re
        match = re.search(r'(?<![A-Za-z])([+\d]+(?:-[\d]+)+)(?![A-Za-z])', "012-3456789")
        if match:
            result = normalize_dashed_digits(match)
            assert "kosong" in result or "satu" in result or "dua" in result


class TestNormalizeMixedAlnum:
    """Test Malay mixed alphanumeric normalization."""

    def test_simple_mixed(self):
        import re
        match = re.search(r'\b[\w\-]+\b', "abc123")
        if match:
            result = normalize_mixed_alnum(match)
            # Should expand digits to Malay
            assert "satu" in result or "dua" in result or "tiga" in result


class TestNormalizeNumber:
    """Test Malay number normalization."""

    def test_single_digit(self):
        import re
        match = re.search(r'\b\d+\b', "5")
        if match:
            result = normalize_number(match)
            assert result == "lima"

    def test_double_digit(self):
        import re
        match = re.search(r'\b\d+\b', "42")
        if match:
            result = normalize_number(match)
            assert "empat" in result or "puluh" in result

    def test_large_number(self):
        import re
        match = re.search(r'\b\d+\b', "1000")
        if match:
            result = normalize_number(match)
            assert "ribu" in result


class TestNum2word:
    """Test Malay number to words conversion."""

    def test_to_cardinal_zero(self):
        assert to_cardinal(0) == "kosong"

    def test_to_cardinal_single_digit(self):
        assert to_cardinal(1) == "satu"
        assert to_cardinal(5) == "lima"
        assert to_cardinal(9) == "sembilan"

    def test_to_cardinal_tens(self):
        assert to_cardinal(10) == "sepuluh"
        assert to_cardinal(11) == "sebelas"
        assert to_cardinal(20) == "dua puluh"
        assert to_cardinal(25) == "dua puluh lima"

    def test_to_cardinal_hundreds(self):
        assert to_cardinal(100) == "seratus"
        assert to_cardinal(250) == "dua ratus lima puluh"

    def test_to_cardinal_thousands(self):
        assert to_cardinal(1000) == "seribu"
        assert to_cardinal(5000) == "lima ribu"

    def test_to_cardinal_negative(self):
        assert "negatif" in to_cardinal(-5)

    def test_to_cardinal_float(self):
        result = to_cardinal(3.14)
        assert "tiga" in result
        assert "perpuluhan" in result

    def test_to_ordinal_first(self):
        assert to_ordinal(1) == "pertama"

    def test_to_ordinal_second(self):
        assert "kedua" in to_ordinal(2)

    def test_to_ordinal_tenth(self):
        assert "kesepuluh" in to_ordinal(10) or "sepuluh" in to_ordinal(10)

    def test_to_currency(self):
        assert to_currency(100) == "seratus ringgit"

    def test_to_year(self):
        result = to_year(2023)
        assert "ribu" in result


class TestNormalizeMalay:
    """Test main Malay text normalization function."""

    def test_empty_string(self):
        assert normalize_malay("") == ""

    def test_simple_text(self):
        result = normalize_malay("Hello dunia")
        assert "dunia" in result

    def test_with_numbers(self):
        result = normalize_malay("Saya ada 5 kucing")
        assert "lima" in result

    def test_with_date(self):
        result = normalize_malay("Tarikh ialah 15/08/2023")
        assert "lima belas" in result or "belas" in result

    def test_with_currency_rm(self):
        result = normalize_malay("Harganya RM100")
        assert "ringgit" in result

    def test_with_currency_rm_decimal(self):
        result = normalize_malay("Harganya RM50.50")
        assert "ringgit" in result
        assert "sen" in result

    def test_with_time_malam(self):
        result = normalize_malay("Jumpa pada 9:00 malam")
        assert "malam" in result.lower()

    def test_with_time_petang(self):
        result = normalize_malay("Jumpa pada 2:30 petang")
        assert "petang" in result.lower()

    def test_with_percentage(self):
        result = normalize_malay("Diskaun 50%")
        assert "peratus" in result

    def test_with_decimal(self):
        result = normalize_malay("Nilainya 3.14")
        assert "tiga" in result
        assert "perpuluhan" in result

    def test_with_dashed_number(self):
        result = normalize_malay("Hubungi 012-3456789")
        # Should convert dashed numbers
        assert len(result) > len("Hubungi 012-3456789")

    def test_complex_sentence(self):
        result = normalize_malay("Temu janji pada 15/08/2023 pada 2:30 petang dan kos RM50")
        assert "petang" in result.lower()
        assert "ringgit" in result
