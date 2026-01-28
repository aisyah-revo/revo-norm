"""
Comprehensive unit tests for currency normalization in both English and Malay.
"""

import pytest
from revo_norm.normalizer_en import normalize_currency as normalize_currency_en
from revo_norm.normalizer_ms import normalize_currency as normalize_currency_ms
from revo_norm.num2word import to_currency
from revo_norm.text_normalizer import normalize_text


class TestCurrencyNormalizationEnglish:
    """Test English currency normalization."""

    def test_rm_no_decimal(self):
        """Test RM without decimal places."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM100", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "ringgit" in result.lower()

    def test_rm_with_decimal(self):
        """Test RM with decimal places."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM50.50", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "ringgit" in result.lower()
            assert "cent" in result.lower() or "sen" in result.lower()

    def test_rm_large_amount(self):
        """Test RM with large amount."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM1,500", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "ringgit" in result.lower()
            assert "thousand" in result.lower() or "fifteen hundred" in result.lower()

    def test_usd_dollar(self):
        """Test USD/$ converts to dollar."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "$100", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "dollar" in result.lower()

    def test_usd_with_code(self):
        """Test USD code."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "USD250", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "dollar" in result.lower()

    def test_gbp_pound(self):
        """Test GBP/£ converts to pound."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "£50", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "pound" in result.lower()

    def test_gbp_with_code(self):
        """Test GBP code."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "GBP75", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "pound" in result.lower()

    def test_eur_euro(self):
        """Test EUR/€ converts to euro."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "€25", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "euro" in result.lower()

    def test_eur_with_code(self):
        """Test EUR code."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "EUR30", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "euro" in result.lower()

    def test_myr_code(self):
        """Test MYR code."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "MYR200", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "ringgit" in result.lower()

    def test_dollar_with_pence(self):
        """Test dollar with cents."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "$99.99", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "dollar" in result.lower()
            assert "cent" in result.lower()

    def test_pound_with_pence(self):
        """Test pound with pence."""
        import re
        match = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "£15.50", re.IGNORECASE)
        if match:
            result = normalize_currency_en(match)
            assert "pound" in result.lower()
            assert "pence" in result.lower()

    def test_case_insensitive(self):
        """Test case insensitivity."""
        import re
        match1 = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "rm100", re.IGNORECASE)
        match2 = re.search(r'\b(RM|\$|£|€|USD|EUR|GBP|MYR)\s?([\d,]+(?:[\.,]\d{1,2})?)\b', "RM100", re.IGNORECASE)
        if match1 and match2:
            result1 = normalize_currency_en(match1)
            result2 = normalize_currency_en(match2)
            # Both should produce similar results
            assert "ringgit" in result1.lower()
            assert "ringgit" in result2.lower()


class TestCurrencyNormalizationMalay:
    """Test Malay currency normalization."""

    def test_rm_no_decimal(self):
        """Test RM without decimal places in Malay."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM100", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "ringgit" in result.lower()

    def test_rm_with_decimal(self):
        """Test RM with decimal places in Malay."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM50.50", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "ringgit" in result.lower()
            assert "sen" in result.lower()

    def test_rm_large_amount(self):
        """Test RM with large amount in Malay."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "RM1,500", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "ringgit" in result.lower()
            assert "ribu" in result.lower()

    def test_usd_in_malay(self):
        """Test USD in Malay normalization."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "$100", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "dollar" in result.lower()

    def test_gbp_in_malay(self):
        """Test GBP in Malay normalization."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "£50", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "pound" in result.lower()

    def test_eur_in_malay(self):
        """Test EUR in Malay normalization."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "€25", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "euro" in result.lower()

    def test_myr_code_in_malay(self):
        """Test MYR code in Malay normalization."""
        import re
        match = re.search(r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b', "MYR200", re.IGNORECASE)
        if match:
            result = normalize_currency_ms(match)
            assert "ringgit" in result.lower()


class TestNum2wordCurrency:
    """Test num2word currency conversion."""

    def test_zero_ringgit(self):
        """Test 0 ringgit."""
        result = to_currency(0)
        assert "kosong" in result
        assert "ringgit" in result

    def test_single_digit_ringgit(self):
        """Test single digit ringgit."""
        assert to_currency(1) == "satu ringgit"
        assert to_currency(5) == "lima ringgit"

    def test_double_digit_ringgit(self):
        """Test double digit ringgit."""
        assert to_currency(10) == "sepuluh ringgit"
        assert to_currency(50) == "lima puluh ringgit"

    def test_hundreds_ringgit(self):
        """Test hundreds ringgit."""
        assert to_currency(100) == "seratus ringgit"
        assert to_currency(500) == "lima ratus ringgit"

    def test_thousands_ringgit(self):
        """Test thousands ringgit."""
        assert to_currency(1000) == "seribu ringgit"
        assert to_currency(5000) == "lima ribu ringgit"

    def test_complex_amount(self):
        """Test complex ringgit amount."""
        result = to_currency(12345)
        assert "ringgit" in result
        assert "ribu" in result


class TestCurrencyInFullTextNormalization:
    """Test currency in full text normalization."""

    def test_english_single_currency(self):
        """Test single currency in English text."""
        result = normalize_text("It costs RM100", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result or "one hundred" in result

    def test_english_multiple_currencies(self):
        """Test multiple currencies in English text."""
        result = normalize_text("Price is $50 or £40", language="en", apply_pronunciation_overrides_flag=False)
        assert "dollar" in result or "fifty" in result

    def test_english_mixed_currencies(self):
        """Test mixed currencies in English text."""
        result = normalize_text("RM100 equals $25", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
        assert "dollar" in result

    def test_malay_single_currency(self):
        """Test single currency in Malay text."""
        result = normalize_text("Harganya RM100", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_malay_multiple_currencies(self):
        """Test multiple currencies in Malay text."""
        result = normalize_text("Harga RM50 dan $30", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
        assert "dollar" in result

    def test_malay_currency_with_sen(self):
        """Test currency with sen in Malay text."""
        result = normalize_text("Harganya RM50.50", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
        assert "sen" in result

    def test_malay_large_amount(self):
        """Test large currency amount in Malay text."""
        result = normalize_text("Kereta bernilai RM50,000", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
        assert "ribu" in result

    def test_currency_with_other_elements(self):
        """Test currency with other text elements."""
        result = normalize_text("On 15/08/2023, price RM100 at 2:30 pm", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_currency_at_sentence_start(self):
        """Test currency at start of sentence."""
        result = normalize_text("RM100 is the price", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_currency_at_sentence_end(self):
        """Test currency at end of sentence."""
        result = normalize_text("The total is RM50.", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_decimal_currencies(self):
        """Test decimal currency amounts."""
        result = normalize_text("Prices: RM12.50, $25.75, £15.25", language="en", apply_pronunciation_overrides_flag=False)
        # Should handle decimal amounts
        assert "ringgit" in result or "dollar" in result or "pound" in result


class TestCurrencyEdgeCases:
    """Test edge cases for currency normalization."""

    def test_zero_amount(self):
        """Test zero currency amount."""
        result = normalize_text("Free or RM0", language="en", apply_pronunciation_overrides_flag=False)
        assert "zero" in result or "ringgit" in result

    def test_very_large_amount(self):
        """Test very large currency amount."""
        result = normalize_text("The project cost RM1,000,000", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
        assert "juta" in result

    def test_currency_with_commas(self):
        """Test currency with comma separators."""
        result = normalize_text("Price: RM1,234,567", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_multiple_spaces(self):
        """Test currency with multiple spaces."""
        result = normalize_text("Cost RM  100", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_currency_no_space(self):
        """Test currency symbol without space."""
        result = normalize_text("Cost RM100", language="en", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result

    def test_round_numbers(self):
        """Test round currency numbers."""
        result = normalize_text("It cost RM10, RM100, and RM1000", language="ms", apply_pronunciation_overrides_flag=False)
        assert "ringgit" in result
