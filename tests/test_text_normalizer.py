"""
Unit tests for text_normalizer module.
"""

import pytest
from revo_norm.text_normalizer import (
    normalize_whitespace,
    email_to_spoken,
    replace_letter_period_sequences,
    remove_inline_reference_numbers,
    is_pronounceable,
    expand_acronym,
    expand_capitalized_initialisms,
    split_into_sentences,
    parse_sound_word_field,
    smart_remove_sound_words,
    insert_comma_after_repeated_words,
    apply_pronunciation_overrides,
    special_replace,
    normalize_text,
)


class TestNormalizeWhitespace:
    """Test whitespace normalization."""

    def test_single_spaces(self):
        assert normalize_whitespace("hello   world") == "hello world"

    def test_multiple_spaces(self):
        assert normalize_whitespace("hello     world     test") == "hello world test"

    def test_tabs_and_newlines(self):
        assert normalize_whitespace("hello\t\tworld\n\ntest") == "hello world test"

    def test_leading_trailing_spaces(self):
        assert normalize_whitespace("  hello world  ") == "hello world"

    def test_mixed_whitespace(self):
        assert normalize_whitespace("  hello\t\t\nworld   test  ") == "hello world test"


class TestEmailToSpoken:
    """Test email to spoken conversion."""

    def test_basic_email(self):
        assert email_to_spoken("user@example.com") == "user at example dot com"

    def test_email_with_underscore(self):
        assert email_to_spoken("user_name@example.com") == "user underscore name at example dot com"

    def test_email_with_plus(self):
        assert email_to_spoken("user+tag@example.com") == "user plus tag at example dot com"

    def test_complex_email(self):
        assert email_to_spoken("sugumaran_thiagarajan@yahoo.com") == \
            "sugumaran underscore thiagarajan at yahoo dot com"


class TestReplaceLetterPeriodSequences:
    """Test letter period sequence replacement."""

    def test_ibm(self):
        assert replace_letter_period_sequences("I.B.M.") == "I B M"

    def test_usa(self):
        assert replace_letter_period_sequences("U.S.A.") == "U S A"

    def test_mixed_text(self):
        assert replace_letter_period_sequences("I work at I.B.M. in the U.S.A.") == \
            "I work at I B M in the U S A"

    def test_single_letter(self):
        assert replace_letter_period_sequences("A.") == "A."


class TestRemoveInlineReferenceNumbers:
    """Test removal of inline reference numbers."""

    def test_reference_after_period(self):
        assert remove_inline_reference_numbers("Hello world.1") == "Hello world."

    def test_reference_after_exclamation(self):
        assert remove_inline_reference_numbers("Hello!2") == "Hello!"

    def test_multiple_references(self):
        assert remove_inline_reference_numbers("Hello.1 How are you?2") == "Hello. How are you?"


class TestIsPronounceable:
    """Test acronym pronounceability check."""

    def test_pronounceable_two_vowels(self):
        assert is_pronounceable("NASA") is True

    def test_pronounceable_three_vowels(self):
        assert is_pronounceable("UNESCO") is True

    def test_not_pronounceable_one_vowel(self):
        assert is_pronounceable("IBM") is False

    def test_not_pronounceable_no_vowels(self):
        assert is_pronounceable("XYZ") is False


class TestExpandAcronym:
    """Test acronym expansion."""

    def test_known_letterwise_uob(self):
        assert expand_acronym("UOB") == "U O B"

    def test_known_letterwise_uia(self):
        assert expand_acronym("UIA") == "U I A"

    def test_known_letterwise_uitm(self):
        assert expand_acronym("UITM") == "U I T M"

    def test_known_letterwise_klia(self):
        assert expand_acronym("KLIA") == "K L I A"

    def test_pronounceable_acronym(self):
        assert expand_acronym("NASA") == "NASA"

    def test_non_pronounceable_short(self):
        assert expand_acronym("IBM") == "I B M"


class TestExpandCapitalizedInitialisms:
    """Test expansion of capitalized initialisms in text."""

    def test_single_acronym(self):
        assert expand_capitalized_initialisms("I work at IBM.") == "I work at I B M."

    def test_multiple_acronyms(self):
        assert expand_capitalized_initialisms("NASA and IBM are organizations.") == \
            "NASA and I B M are organizations."

    def test_known_letterwise(self):
        assert expand_capitalized_initialisms("I flew from KLIA.") == "I flew from K L I A."

    def test_mixed_case_not_expanded(self):
        assert expand_capitalized_initialisms("Ibm") == "Ibm"


class TestSplitIntoSentences:
    """Test sentence splitting."""

    def test_simple_sentences(self):
        result = split_into_sentences("Hello world. How are you?")
        assert result == ["Hello world.", "How are you?"]

    def test_multiple_sentences(self):
        result = split_into_sentences("First. Second. Third.")
        assert len(result) == 3

    def test_single_sentence(self):
        result = split_into_sentences("Hello world")
        assert result == ["Hello world"]


class TestParseSoundWordField:
    """Test sound word field parsing."""

    def test_simple_patterns(self):
        result = parse_sound_word_field("[laughter]\n[applause]")
        assert result == [("[laughter]", ""), ("[applause]", "")]

    def test_with_replacements(self):
        result = parse_sound_word_field("[laughter]=>chuckles\n[applause]=>claps")
        assert result == [("[laughter]", "chuckles"), ("[applause]", "claps")]

    def test_mixed(self):
        result = parse_sound_word_field("[laughter]\n[applause]=>claps")
        assert result == [("[laughter]", ""), ("[applause]", "claps")]

    def test_empty_lines(self):
        result = parse_sound_word_field("[laughter]\n\n\n[applause]")
        assert result == [("[laughter]", ""), ("[applause]", "")]


class TestSmartRemoveSoundWords:
    """Test sound word removal."""

    def test_remove_laughter(self):
        result = smart_remove_sound_words("Hello [laughter] world", [("[laughter]", "")])
        assert result == "Hello world"

    def test_replace_laughter(self):
        result = smart_remove_sound_words("Hello [laughter] world", [("[laughter]", "chuckles")])
        assert result == "Hello chuckles world"

    def test_multiple_sound_words(self):
        result = smart_remove_sound_words(
            "Hello [laughter] world [applause]",
            [("[laughter]", ""), ("[applause]", "")]
        )
        assert result == "Hello world"

    def test_with_possessive(self):
        result = smart_remove_sound_words("Someone [laughter]'s here", [("[laughter]", "chuckles")])
        assert "chuckles" in result


class TestInsertCommaAfterRepeatedWords:
    """Test comma insertion after repeated words."""

    def test_three_repeats(self):
        result = insert_comma_after_repeated_words("test test test test")
        assert result == "test test test, test"

    def test_four_repeats(self):
        result = insert_comma_after_repeated_words("hello hello hello hello")
        assert result == "hello hello hello, hello"

    def test_no_repeats(self):
        result = insert_comma_after_repeated_words("hello world test")
        assert result == "hello world test"

    def test_case_insensitive(self):
        result = insert_comma_after_repeated_words("Test TEST test TEST")
        assert "," in result


class TestApplyPronunciationOverrides:
    """Test pronunciation overrides."""

    def test_twenty_three(self):
        assert apply_pronunciation_overrides("twenty-three") == "twenty tree"

    def test_cut_off(self):
        assert apply_pronunciation_overrides("cut-off") == "kad off"

    def test_a_l(self):
        assert apply_pronunciation_overrides("a/l") == "anak lelaki"

    def test_a_p(self):
        assert apply_pronunciation_overrides("a/p") == "anak perempuan"

    def test_no_malaysia(self):
        assert apply_pronunciation_overrides("1Malaysia") == "satu malaysia"

    def test_no_dot(self):
        assert apply_pronunciation_overrides("No. 5") == "number 5"

    def test_mg_unit(self):
        assert apply_pronunciation_overrides("500mg") == "500 milligram"

    def test_kg_unit(self):
        assert apply_pronunciation_overrides("60kg") == "60 kilogram"

    def test_gb_unit(self):
        assert apply_pronunciation_overrides("100GB") == "100 gigabyte"

    def test_hb_unit(self):
        assert apply_pronunciation_overrides("15hb") == "15 haribulan"

    def test_slash(self):
        assert apply_pronunciation_overrides("and/or") == "and strok or"


class TestSpecialReplace:
    """Test special character replacement."""

    def test_ampersand(self):
        assert special_replace("Tom & Jerry") == "Tom and Jerry"

    def test_plus(self):
        assert special_replace("1+1") == "1 plus 1"

    def test_equals(self):
        assert special_replace("1=1") == "1 equals 1"

    def test_at(self):
        assert special_replace("@home") == "at home"

    def test_hash(self):
        assert special_replace("#tag") == "hash tag"

    def test_star(self):
        assert special_replace("*test") == "star test"

    def test_percent(self):
        assert special_replace("50%") == "50 percent"

    def test_dollar(self):
        assert special_replace("$100") == "dollar 100"

    def test_combined(self):
        result = special_replace("AT&T")
        assert "at" in result.lower()


class TestNormalizeText:
    """Test main normalize_text function."""

    def test_empty_text(self):
        assert normalize_text("") == ""

    def test_whitespace_only(self):
        assert normalize_text("   ") == ""

    def test_english_language(self):
        result = normalize_text("I have 2 cats.", language="en")
        assert "two" in result

    def test_malay_language(self):
        result = normalize_text("Saya ada 2 kucing.", language="ms")
        assert "dua" in result

    def test_with_sound_words(self):
        result = normalize_text(
            "Hello [laughter] world.",
            sound_words_field="[laughter]",
            apply_pronunciation_overrides_flag=False
        )
        assert "[laughter]" not in result

    def test_normalize_spacing_true(self):
        result = normalize_text("Hello    world", normalize_spacing=True)
        assert result == "Hello world"

    def test_normalize_spacing_false(self):
        result = normalize_text("Hello    world", normalize_spacing=False)
        assert "    " in result

    def test_fix_dot_letters(self):
        result = normalize_text("I work at I.B.M.", language="en")
        assert "I B M" in result

    def test_email_in_text(self):
        result = normalize_text("Email me at user@example.com", language="en")
        assert "user at example dot com" in result or "user at example" in result

    def test_acronym_expansion(self):
        result = normalize_text("I flew from KLIA.", language="en", apply_pronunciation_overrides_flag=False)
        assert "K L I A" in result

    def test_pronunciation_overrides(self):
        result = normalize_text("a/l Ahmad", language="en")
        assert "anak lelaki" in result

    def test_special_characters(self):
        result = normalize_text("Tom & Jerry", language="en", apply_pronunciation_overrides_flag=False)
        assert "and" in result

    def test_combined_normalization(self):
        result = normalize_text(
            "Contact me at user_name@example.com or call 123-456-7890.",
            language="en",
            apply_pronunciation_overrides_flag=False
        )
        # Should have email conversion and number expansion
        assert "underscore" in result
