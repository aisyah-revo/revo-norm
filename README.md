# Revo Norm

Text normalization library for English and Malay TTS applications.

## Installation

From PyPI:
```bash
pip install revo-norm
```

From source:
```bash
git clone https://github.com/yourusername/revo-norm.git
cd revo-norm
pip install -e .
```

## Quick Start

```python
from revo_norm import normalize_text

# English
result = normalize_text("Meeting at 3:30 pm on 15/08/2025", language="en")
print(result)
# "Meeting at three thirty pm on fifteenth of August two thousand and twenty-five"

# Malay
result = normalize_text("Jumpa 2:30 petang pada 12/03/2025", language="ms")
print(result)
# "Jumpa dua tiga puluh petang pada dua belas Mac dua ribu dua puluh lima"
```

## Usage

```python
from revo_norm import normalize_text

# Basic usage
result = normalize_text("Price: RM100.50", language="en")

# With options
result = normalize_text(
    "Email user@example.com for info",
    language="en",
    normalize_spacing=True,
    sound_words_field="[laughter]\\n[applause]"
)
```

## API

| Function | Description |
|----------|-------------|
| `normalize_text(text, language='en')` | Main normalization function |
| `normalize_english(text)` | English normalization |
| `normalize_malay(text)` | Malay normalization |
| `email_to_spoken(email)` | Email to spoken form |
| `expand_capitalized_initialisms(text)` | Expand acronyms |

## Running Tests

```bash
uv run pytest
```

## License

MIT
