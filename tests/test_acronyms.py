"""
Comprehensive unit tests for acronym expansion in both English and Malay.
"""

import pytest
from revo_norm.text_normalizer import (
    expand_acronym,
    expand_capitalized_initialisms,
    normalize_text,
    KNOWN_LETTERWISE,
)


class TestExpandAcronym:
    """Test individual acronym expansion."""

    def test_uob_expansion(self):
        """Test UOB expands to U O B."""
        assert expand_acronym("UOB") == "U O B"

    def test_uia_expansion(self):
        """Test UIA expands to U I A."""
        assert expand_acronym("UIA") == "U I A"

    def test_uitm_expansion(self):
        """Test UITM expands to U I T M."""
        assert expand_acronym("UITM") == "U I T M"

    def test_klia_expansion(self):
        """Test KLIA expands to K L I A."""
        assert expand_acronym("KLIA") == "K L I A"

    def test_klia2_expansion(self):
        """Test KLIA2 expands to K L I A 2."""
        assert expand_acronym("KLIA2") == "K L I A 2"

    def test_nasa_pronounceable(self):
        """Test NASA is kept as pronounceable."""
        assert expand_acronym("NASA") == "NASA"

    def test_unesco_pronounceable(self):
        """Test UNESCO is kept as pronounceable."""
        assert expand_acronym("UNESCO") == "UNESCO"

    def test_ibm_not_pronounceable(self):
        """Test IBM expands to I B M."""
        assert expand_acronym("IBM") == "I B M"

    def test_fbi_not_pronounceable(self):
        """Test FBI expands to F B I."""
        assert expand_acronym("FBI") == "F B I"

    def test_ceo_not_pronounceable(self):
        """Test CEO expands to C E O."""
        assert expand_acronym("CEO") == "C E O"

    def test_cia_not_pronounceable(self):
        """Test CIA expands to C I A."""
        assert expand_acronym("CIA") == "C I A"

    def test_ata_pronounceable(self):
        """Test ATA is pronounceable (two vowels)."""
        assert expand_acronym("ATA") == "ATA"

    def test_single_letter(self):
        """Test single letter raises no error."""
        result = expand_acronym("A")
        assert result == "A"

    def test_two_letter(self):
        """Test two letter acronym."""
        result = expand_acronym("IT")
        assert result == "I T"


class TestExpandCapitalizedInitialisms:
    """Test expansion of acronyms within text."""

    def test_single_uob_in_text(self):
        """Test UOB is expanded in text."""
        result = expand_capitalized_initialisms("I bank with UOB.")
        assert result == "I bank with U O B."

    def test_klia_in_text(self):
        """Test KLIA is expanded in text."""
        result = expand_capitalized_initialisms("I flew from KLIA to Singapore.")
        assert result == "I flew from K L I A to Singapore."

    def test_uitm_in_text(self):
        """Test UITM is expanded in text."""
        result = expand_capitalized_initialisms("She studies at UITM.")
        assert result == "She studies at U I T M."

    def test_uia_in_text(self):
        """Test UIA is expanded in text."""
        result = expand_capitalized_initialisms("UIA is a university.")
        assert result == "U I A is a university."

    def test_nasa_kept_intact(self):
        """Test NASA is not expanded in text."""
        result = expand_capitalized_initialisms("NASA launched a rocket.")
        assert result == "NASA launched a rocket."

    def test_multiple_acronyms(self):
        """Test multiple acronyms in one sentence."""
        result = expand_capitalized_initialisms("IBM and NASA are different.")
        assert result == "I B M and NASA are different."

    def test_mixed_case_not_expanded(self):
        """Test mixed case words are not expanded."""
        result = expand_capitalized_initialisms("The ibm mainframe is old.")
        assert result == "The ibm mainframe is old."

    def test_acronym_at_start(self):
        """Test acronym at the start of sentence."""
        result = expand_capitalized_initialisms("IBM is a tech company.")
        assert result == "I B M is a tech company."

    def test_acronym_at_end(self):
        """Test acronym at the end of sentence."""
        result = expand_capitalized_initialisms("He works at IBM.")
        assert result == "He works at I B M."

    def test_consecutive_acronyms(self):
        """Test consecutive acronyms."""
        result = expand_capitalized_initialisms("IBM CEO announced.")
        assert result == "I B M C E O announced."

    def test_possessive_acronym(self):
        """Test acronym with possessive."""
        result = expand_capitalized_initialisms("NASA's mission is complete.")
        # Should keep NASA intact
        assert "NASA" in result


class TestAcronymNormalizationEnglish:
    """Test acronym normalization in full English text normalization."""

    def test_uob_with_numbers(self):
        """Test UOB with phone numbers."""
        result = normalize_text("Call UOB at 03-12345678", language="en", apply_pronunciation_overrides_flag=False)
        assert "U O B" in result

    def test_klia_with_time(self):
        """Test KLIA with time."""
        result = normalize_text("Flight to KLIA at 2:30 pm", language="en", apply_pronunciation_overrides_flag=False)
        assert "K L I A" in result

    def test_uitm_with_date(self):
        """Test UITM with date."""
        result = normalize_text("UITM exam on 15/08/2023", language="en", apply_pronunciation_overrides_flag=False)
        assert "U I T M" in result

    def test_multiple_known_letterwise(self):
        """Test multiple known letterwise acronyms."""
        result = normalize_text("From KLIA to KLIA2", language="en", apply_pronunciation_overrides_flag=False)
        assert "K L I A" in result

    def test_pronounceable_not_expanded(self):
        """Test pronounceable acronyms are not expanded."""
        result = normalize_text("NASA mission successful", language="en", apply_pronunciation_overrides_flag=False)
        assert "NASA" in result

    def test_ibm_expanded(self):
        """Test IBM is expanded."""
        result = normalize_text("IBM computer", language="en", apply_pronunciation_overrides_flag=False)
        assert "I B M" in result


class TestAcronymNormalizationMalay:
    """Test acronym normalization in full Malay text normalization."""

    def test_uob_in_malay(self):
        """Test UOB in Malay text."""
        result = normalize_text("Saya pelanggan UOB", language="ms", apply_pronunciation_overrides_flag=False)
        assert "U O B" in result

    def test_klia_in_malay(self):
        """Test KLIA in Malay text."""
        result = normalize_text("Penerbangan ke KLIA", language="ms", apply_pronunciation_overrides_flag=False)
        assert "K L I A" in result

    def test_uitm_in_malay(self):
        """Test UITM in Malay text."""
        result = normalize_text("Pelajar UITM", language="ms", apply_pronunciation_overrides_flag=False)
        assert "U I T M" in result

    def test_with_numbers(self):
        """Test acronym with Malay numbers."""
        result = normalize_text("2 pelajar UITM", language="ms", apply_pronunciation_overrides_flag=False)
        assert "U I T M" in result
        assert "dua" in result

    def test_with_currency(self):
        """Test acronym with Malay currency."""
        result = normalize_text("Yuran UITM RM500", language="ms", apply_pronunciation_overrides_flag=False)
        assert "U I T M" in result
        assert "ringgit" in result


class TestKnownLetterwiseSet:
    """Test the KNOWN_LETTERWISE set."""

    def test_all_letterwise_present(self):
        """Test all known letterwise acronyms are in the set."""
        assert "UOB" in KNOWN_LETTERWISE
        assert "UIA" in KNOWN_LETTERWISE
        assert "UITM" in KNOWN_LETTERWISE
        assert "KLIA" in KNOWN_LETTERWISE
        assert "KLIA2" in KNOWN_LETTERWISE

    def test_case_sensitivity(self):
        """Test the set is case-sensitive."""
        assert "uob" not in KNOWN_LETTERWISE
        assert "Uob" not in KNOWN_LETTERWISE
        assert "UOB" in KNOWN_LETTERWISE
