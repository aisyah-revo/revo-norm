"""Test cases from test-cases.txt file with assertions."""
import pytest
from revo_norm import normalize_text


def read_test_cases():
    """Read test cases from test-cases.txt."""
    with open("test-cases.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f if line.rstrip("\n")]
    return lines


def read_expected_outputs():
    """Read expected outputs from test-cases-expected.txt."""
    with open("test-cases-expected.txt", "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines


# Prepare test data
test_cases = read_test_cases()
expected = read_expected_outputs()

# English test cases (1-100)
english_params = [
    (i+1, text, exp) for i, (text, exp) in enumerate(zip(test_cases[:100], expected[:100]))
]

# Malay test cases (101-150)
malay_params = [
    (i+101, text, exp) for i, (text, exp) in enumerate(zip(test_cases[100:150], expected[100:150]))
]


@pytest.mark.parametrize("line_num,text,expected_output", english_params)
def test_normalize_english(line_num, text, expected_output):
    """Test normalize_text on English sentences."""
    result = normalize_text(text, language="en")
    print(f"\n[{line_num}]")
    print(f"  Input:  {text}")
    print(f"  Output: {result}")
    assert result == expected_output, f"Line {line_num} (English):\n  Input:    {text}\n  Expected: {expected_output}\n  Got:      {result}"


@pytest.mark.parametrize("line_num,text,expected_output", malay_params)
def test_normalize_malay(line_num, text, expected_output):
    """Test normalize_text on Malay sentences."""
    result = normalize_text(text, language="ms")
    print(f"\n[{line_num}]")
    print(f"  Input:  {text}")
    print(f"  Output: {result}")
    assert result == expected_output, f"Line {line_num} (Malay):\n  Input:    {text}\n  Expected: {expected_output}\n  Got:      {result}"
 