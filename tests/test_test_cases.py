"""Test cases from test-cases.csv file with assertions."""
import pytest
import csv
from revo_norm import normalize_text


def read_test_cases_from_csv():
    """Read test cases from test-cases.csv."""
    test_cases = []
    with open("test-cases.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append((row["original_text"], row["expected_normalized"]))
    return test_cases


# Prepare test data
all_test_cases = read_test_cases_from_csv()

# English test cases (lines 1-100 in original file, indices 0-99 here)
english_params = [
    (i+1, text, exp) for i, (text, exp) in enumerate(all_test_cases[:100])
]

# Malay test cases (lines 101-150 in original file, indices 100-149 here)
malay_params = [
    (i+101, text, exp) for i, (text, exp) in enumerate(all_test_cases[100:150])
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
