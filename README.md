# Revo Norm

A Python text normalization library for English and Malay (Bahasa Melayu) Text-to-Speech (TTS) applications.

## Features

- **English Text Normalization**
  - Numbers to words (e.g., "123" → "one hundred twenty-three")
  - Date normalization (e.g., "15/08/2023" → "fifteenth of August, twenty twenty-three")
  - Currency conversion (e.g., "RM100" → "one hundred ringgit")
  - Time expressions (e.g., "2:30 pm" → "two thirty pm")
  - Ordinal numbers (e.g., "1st" → "first")
  - Decimal numbers (e.g., "3.14" → "three point one four")
  - Percentage handling (e.g., "50%" → "fifty percent")
  - Contraction expansion (e.g., "I'm" → "I am")
  - Abbreviation expansion (e.g., "Dr." → "doctor")

- **Malay Text Normalization**
  - Numbers to Malay words (e.g., "123" → "seratus dua puluh tiga")
  - Date normalization in Malay (e.g., "15/08/2023" → "lima belas Ogos dua ribu dua puluh tiga")
  - Currency with Malay units (e.g., "RM100" → "seratus ringgit")
  - Time with Malay meridians (e.g., "9:00 malam" → "sembilan malam")
  - Percentage in Malay (e.g., "50%" → "lima puluh peratus")
  - Decimal handling (e.g., "3.14" → "tiga perpuluhan satu empat")

- **General Features**
  - Acronym expansion (e.g., "UOB" → "U O B", "UITM" → "U I T M")
  - Email to spoken form (e.g., "user@example.com" → "user at example dot com")
  - Sound word removal (e.g., [laughter], [applause])
  - Whitespace normalization
  - Letter period sequence handling (e.g., "I.B.M." → "I B M")

## Installation

```bash
pip install revo-norm
```

### Install from source

```bash
git clone https://github.com/yourusername/revo-norm
cd revo-norm
uv sync
```

## Quick Start

```python
from revo_norm import normalize_text

# English normalization
text_en = "I have 5 cats and 2 dogs. Email me at user@example.com"
result_en = normalize_text(text_en, language="en")
print(result_en)
# Output: "I have five cats and two dogs. Email me at user at example dot com"

# Malay normalization
text_ms = "Saya ada 5 kucing. Hubungi 012-3456789"
result_ms = normalize_text(text_ms, language="ms")
print(result_ms)
# Output: "Saya ada lima kucing. Hubungi kosong satu dua ... tiga lapan sembilan"
```

## Usage Examples

### Basic Normalization

```python
from revo_norm import normalize_text

# English
result = normalize_text("Meeting at 3:30 pm", language="en")
# "Meeting at three thirty pm"

# Malay
result = normalize_text("Jumpa 2:30 petang", language="ms")
# "Jumpa dua tiga puluh petang"
```

### Currency Normalization

```python
from revo_norm import normalize_text

# English
result = normalize_text("Price: RM100", language="en")
# "Price: one hundred ringgit"

# Malay
result = normalize_text("Harga RM50.50", language="ms")
# "Harga lima puluh ringgit lima puluh sen"
```

### Acronym Expansion

```python
from revo_norm import normalize_text, expand_capitalized_initialisms

# Known letter-wise acronyms (UOB, UIA, UITM, KLIA, KLIA2)
result = normalize_text("I flew from KLIA to Singapore", language="en")
# "I flew from K L I A to Singapore"

# Expand acronyms directly
result = expand_capitalized_initialisms("She studies at UITM.")
# "She studies at U I T M."
```

### Email Conversion

```python
from revo_norm import email_to_spoken

email = "john_doe@example.com"
result = email_to_spoken(email)
# "john underscore doe at example dot com"
```

### Date Normalization

```python
from revo_norm import normalize_text

# English
result = normalize_text("Appointment on 15/08/2023", language="en")
# "Appointment on fifteenth of August, two thousand twenty-three"

# Malay
result = normalize_text("Temu janji 15/08/2023", language="ms")
# "Temu janji lima belas Ogos dua ribu dua puluh tiga"
```

### Sound Word Removal

```python
from revo_norm import normalize_text

text = "Hello [laughter] world [applause]"
result = normalize_text(
    text,
    language="en",
    sound_words_field="[laughter]\n[applause]"
)
# "Hello world"
```

### Number to Words (Malay)

```python
from revo_norm import to_cardinal, to_ordinal, to_currency

# Cardinal numbers
print(to_cardinal(123))  # "seratus dua puluh tiga"

# Ordinal numbers
print(to_ordinal(1))     # "pertama"
print(to_ordinal(21))    # "ke dua puluh satu"

# Currency
print(to_currency(500))  # "lima ratus ringgit"
```

## API Reference

### `normalize_text(text, language='en', ...)`

Main text normalization function.

**Parameters:**
- `text` (str): Input text to normalize
- `language` (str): Language code - `'en'` for English, `'ms'` for Malay
- `normalize_spacing` (bool): Whether to normalize whitespace (default: True)
- `fix_dot_letters` (bool): Whether to fix letter period sequences (default: True)
- `sound_words_field` (str): Sound words to remove, newline-separated (default: "")
- `apply_pronunciation_overrides_flag` (bool): Apply pronunciation overrides (default: True)

**Returns:** Normalized text string

### Language-Specific Normalizers

#### `normalize_english(text)` / `text_normalize(text)`

Normalize English text.

```python
from revo_norm import normalize_english
result = normalize_english("I have 5 cats")
# "I have five cats"
```

#### `normalize_malay(text)`

Normalize Malay text.

```python
from revo_norm import normalize_malay
result = normalize_malay("Saya ada 5 kucing")
# "Saya ada lima kucing"
```

### Utility Functions

#### `email_to_spoken(email)`

Convert email to spoken form.

#### `expand_capitalized_initialisms(text)`

Expand capitalized acronyms in text.

#### `normalize_whitespace(text)`

Normalize multiple whitespace to single space.

#### `split_into_sentences(text)`

Split text into sentences.

### Malay Number-to-Words Functions

#### `to_cardinal(number)`

Convert number to Malay cardinal words.

#### `to_ordinal(number)`

Convert number to Malay ordinal words.

#### `to_currency(value)`

Convert number to Malay currency format.

## Known Letter-wise Acronyms

The following acronyms are always expanded letter-by-letter:
- **UOB** → "U O B"
- **UIA** → "U I A"
- **UITM** → "U I T M"
- **KLIA** → "K L I A"
- **KLIA2** → "K L I A 2"

Pronounceable acronyms (like NASA, UNESCO) are kept intact.

## Running Tests

```bash
# Install test dependencies
uv sync

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_acronyms.py

# Run with coverage
uv run pytest --cov=revo_norm --cov-report=html
```

## Dependencies

- `nltk` >= 3.8 - Natural Language Toolkit
- `inflect` >= 6.0 - English number-to-words conversion

## Development

### Project Structure

```
revo-norm/
├── revo_norm/
│   ├── __init__.py           # Package initialization & exports
│   ├── text_normalizer.py    # Main normalization functions
│   ├── normalizer_en.py      # English normalizer
│   ├── normalizer_ms.py      # Malay normalizer
│   └── num2word.py           # Malay number-to-words converter
├── tests/
│   ├── test_text_normalizer.py
│   ├── test_normalizer_en.py
│   ├── test_normalizer_ms.py
│   ├── test_acronyms.py
│   ├── test_currency.py
│   └── test_email.py
├── pyproject.toml            # Package configuration
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Changelog

### 0.1.0 (2024-01-28)
- Initial release
- English and Malay text normalization
- Acronym expansion
- Currency, date, time normalization
- Email to spoken conversion
- Comprehensive unit tests

## Acknowledgments

This library is designed for Text-to-Speech applications and helps normalize text for better pronunciation by TTS engines.
