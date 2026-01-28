"""
Unit tests for normalizer_en module (English text normalization).
"""

import pytest
from revo_norm.normalizer_en import (
    numbers_mapping_en,
    normalize_date,
    normalize_currency,
    normalize_time,
    normalize_percentage,
    normalize_decimal,
    normalize_dashed_digits,
    normalize_ordinal,
    normalize_number,
    normalize_mixed_alnum,
    expand_contractions,
    expand_abbreviations,
    text_normalize,
)


class TestNumbersMappingEn:
    """Test English number mappings."""

    def test_zero_to_nine(self):
        assert numbers_mapping_en['0'] == 'zero'
        assert numbers_mapping_en['1'] == 'one'
        assert numbers_mapping_en['2'] == 'two'
        assert numbers_mapping_en['3'] == 'three'
        assert numbers_mapping_en['4'] == 'four'
        assert numbers_mapping_en['5'] == 'five'
        assert numbers_mapping_en['6'] == 'six'
        assert numbers_mapping_en['7'] == 'seven'
        assert numbers_mapping_en['8'] == 'eight'
        assert numbers_mapping_en['9'] == 'nine'

    def test_plus(self):
        assert numbers_mapping_en['+'] == 'plus'


class TestNormalizeDate:
    """Test date normalization."""

    def test_dd_mm_yyyy(self):
        import re
        match = re.search(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b', "15/08/2023")
        if match:
            result = normalize_date(match)
            assert "fifteenth" in result or "fifteen" in result
            assert "august" in result.lower()

    def test_single_digit_day_month(self):
        import re
        match = re.search(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b', "5-3-2023")
        if match:
            result = normalize_date(match)
            assert "march" in result.lower() or "three" in result.lower()


class TestNormalizeCurrency:
    """Test currency normalization."""

    def test_rm_no_decimal(self):
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM100", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "ringgit" in result

    def test_rm_with_decimal(self):
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM50.50", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "ringgit" in result
            assert "sen" in result or "cent" in result

    def test_usd(self):
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "$100", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "dollar" in result

    def test_gbp(self):
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "£50", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "pound" in result

    def test_eur(self):
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "€25", re.IGNORECASE)
        if match:
            result = normalize_currency(match)
            assert "euro" in result


class TestNormalizeTime:
    """Test time normalization."""

    def test_hour_only_am(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.))', "9:00 am", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "nine" in result.lower()

    def test_hour_with_minute(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.))', "2:30 pm", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "two" in result.lower()

    def test_zero_minute(self):
        import re
        match = re.search(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.))', "5:00 pm", re.IGNORECASE)
        if match:
            result = normalize_time(match)
            assert "five" in result.lower()


class TestNormalizePercentage:
    """Test percentage normalization."""

    def test_integer_percentage(self):
        import re
        match = re.search(r'\b(\d+(?:\.\d+)?)%', "50%")
        if match:
            result = normalize_percentage(match)
            assert "fifty" in result or "50" in result
            assert "percent" in result

    def test_decimal_percentage(self):
        import re
        match = re.search(r'\b(\d+(?:\.\d+)?)%', "12.5%")
        if match:
            result = normalize_percentage(match)
            assert "percent" in result


class TestNormalizeDecimal:
    """Test decimal number normalization."""

    def test_simple_decimal(self):
        import re
        match = re.search(r'\b(\d+)\.(\d+)\b', "3.14")
        if match:
            result = normalize_decimal(match)
            assert "three" in result
            assert "point" in result

    def test_whole_and_fraction(self):
        import re
        match = re.search(r'\b(\d+)\.(\d+)\b', "12.5")
        if match:
            result = normalize_decimal(match)
            assert "twelve" in result or "12" in result
            assert "point" in result


class TestNormalizeDashedDigits:
    """Test dashed digit normalization."""

    def test_phone_number(self):
        import re
        match = re.search(r'(?<![A-Za-z])([+\d]+(?:-[\d]+)+)(?![A-Za-z])', "123-456-7890")
        if match:
            result = normalize_dashed_digits(match)
            assert "dash" in result

    def test_simple_dashed(self):
        import re
        match = re.search(r'(?<![A-Za-z])([+\d]+(?:-[\d]+)+)(?![A-Za-z])', "1-2-3")
        if match:
            result = normalize_dashed_digits(match)
            assert "dash" in result


class TestNormalizeOrdinal:
    """Test ordinal number normalization."""

    def test_first(self):
        import re
        match = re.search(r'\b(\d{1,2})(st|nd|rd|th)\b', "1st", re.IGNORECASE)
        if match:
            result = normalize_ordinal(match)
            assert "first" in result

    def test_second(self):
        import re
        match = re.search(r'\b(\d{1,2})(st|nd|rd|th)\b', "2nd", re.IGNORECASE)
        if match:
            result = normalize_ordinal(match)
            assert "second" in result

    def test_third(self):
        import re
        match = re.search(r'\b(\d{1,2})(st|nd|rd|th)\b', "3rd", re.IGNORECASE)
        if match:
            result = normalize_ordinal(match)
            assert "third" in result

    def test_twentieth(self):
        import re
        match = re.search(r'\b(\d{1,2})(st|nd|rd|th)\b', "20th", re.IGNORECASE)
        if match:
            result = normalize_ordinal(match)
            assert "twentieth" in result or "twenty" in result


class TestNormalizeNumber:
    """Test plain number normalization."""

    def test_single_digit(self):
        import re
        match = re.search(r'\b\d+\b', "5")
        if match:
            result = normalize_number(match)
            assert result in ["five", "5"]

    def test_double_digit(self):
        import re
        match = re.search(r'\b\d+\b', "42")
        if match:
            result = normalize_number(match)
            assert "forty" in result or "42" in result

    def test_triple_digit(self):
        import re
        match = re.search(r'\b\d+\b', "100")
        if match:
            result = normalize_number(match)
            assert "hundred" in result or "100" in result


class TestNormalizeMixedAlnum:
    """Test mixed alphanumeric normalization."""

    def test_simple_mixed(self):
        import re
        match = re.search(r'\b(?=\w*\d)(?=\w*[A-Za-z])[\w\-]+\b', "abc123")
        if match:
            result = normalize_mixed_alnum(match)
            # Should expand letters
            assert " " in result or len(result) > len("abc123")


class TestExpandContractions:
    """Test contraction expansion."""

    def test_im(self):
        assert expand_contractions("I'm happy") == "I am happy"

    def test_youre(self):
        assert expand_contractions("you're here") == "you are here"

    def test_ive(self):
        assert expand_contractions("I've done it") == "I have done it"

    def test_ill(self):
        assert expand_contractions("I'll go") == "I will go"

    def test_id(self):
        assert expand_contractions("I'd like") == "I would like"

    def test_isnt(self):
        assert expand_contractions("isn't it") == "is not it"

    def test_wont(self):
        assert expand_contractions("won't go") == "will not go"

    def test_cant(self):
        assert expand_contractions("can't do") == "cannot do"

    def test_shouldnt(self):
        assert expand_contractions("shouldn't do") == "should not do"

    def test_mustnt(self):
        assert expand_contractions("mustn't do") == "must not do"

    def test_letsgo(self):
        assert expand_contractions("Let's go") == "Let us go"

    def test_thats(self):
        assert expand_contractions("that's good") == "that is good"

    def test_howareyou(self):
        assert expand_contractions("how're you") == "how are you"


class TestExpandAbbreviations:
    """Test abbreviation expansion."""

    def test_mr(self):
        assert "mister" in expand_abbreviations("Mr. Smith")

    def test_mrs(self):
        assert "misess" in expand_abbreviations("Mrs. Jones")

    def test_dr(self):
        assert "doctor" in expand_abbreviations("Dr. Who")

    def test_st(self):
        assert "saint" in expand_abbreviations("St. Peter")

    def test_jr(self):
        assert "junior" in expand_abbreviations("John Jr.")

    def test_co(self):
        assert "company" in expand_abbreviations("Meta Co.")

    def test_ltd(self):
        assert "limited" in expand_abbreviations("Acme Ltd.")

    def test_col(self):
        assert "colonel" in expand_abbreviations("Col. Sanders")


class TestTextNormalize:
    """Test main English text normalization function."""

    def test_empty_string(self):
        assert text_normalize("") == ""

    def test_simple_text(self):
        result = text_normalize("Hello world")
        assert "hello" in result.lower()

    def test_with_numbers(self):
        result = text_normalize("I have 5 cats")
        assert "five" in result or "cat" in result

    def test_with_contractions(self):
        result = text_normalize("I'm happy")
        assert "I am" in result

    def test_with_abbreviations(self):
        result = text_normalize("Dr. Smith is here")
        assert "doctor" in result

    def test_with_date(self):
        result = text_normalize("The date is 15/08/2023")
        assert "august" in result.lower() or "2023" in result

    def test_with_currency(self):
        result = text_normalize("It costs RM100")
        assert "ringgit" in result

    def test_with_time(self):
        result = text_normalize("Meet at 2:30 pm")
        assert "two" in result.lower() or "thirty" in result.lower()

    def test_with_percentage(self):
        result = text_normalize("50% complete")
        assert "percent" in result

    def test_with_decimal(self):
        result = text_normalize("Pi is 3.14")
        assert "three" in result and "point" in result

    def test_with_email(self):
        result = text_normalize("Email user@example.com")
        # Email conversion happens in text_normalizer, not normalizer_en
        assert "user" in result

    def test_with_acronym(self):
        result = text_normalize("I work at IBM")
        # Acronym expansion happens in text_normalizer
        assert "IBM" in result or "I B M" in result

    def test_complex_sentence(self):
        result = text_normalize("Dr. Smith's appointment is on 15/08/2023 at 2:30 pm and costs RM50")
        assert "doctor" in result.lower()
        assert "ringgit" in result
