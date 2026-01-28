import re
from typing import Dict
import os
from revo_norm.num2word import to_cardinal as num2word


numbers_mapping_malay = {
    '0': 'kosong', '1': 'satu', '2': 'dua', '3': 'tiga',
    '4': 'empat', '5': 'lima', '6': 'enam', '7': 'tujuh',
    '8': 'lapan', '9': 'sembilan'
}

_months = {
    '01': 'Januari', '1': 'Januari', '02': 'Februari', '2': 'Februari',
    '03': 'Mac', '3': 'Mac', '04': 'April', '4': 'April',
    '05': 'Mei', '5': 'Mei', '06': 'Jun', '6': 'Jun',
    '07': 'Julai', '7': 'Julai', '08': 'Ogos', '8': 'Ogos',
    '09': 'September', '9': 'September', '10': 'Oktober',
    '11': 'November', '12': 'Disember'
}

# Regex
_date_re = re.compile(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b')

_currency_re = re.compile(
    r'(RM|\$|£|€|USD|EUR|GBP|MYR)(?:\s?)([\d,]+(?:[\.,]\d{1,2})?)\b',
    re.IGNORECASE
)
_decimal_re = re.compile(r'\b(\d+)\.(\d+)\b')
_dashed_digit_re = re.compile(r'(?<![A-Za-z])([+\d]+(?:-[\d]+)+)(?![A-Za-z])')
_alnum_re = re.compile(r'\b[\w\-]+\b')
_number_re = re.compile(r'\b\d+\b')
_percentage_re = re.compile(r'\b(\d+(?:\.\d+)?)%')
_time_re = re.compile(r'\b(\d{1,2})[:\.](\d{2})\s*(?:(am|pm|a\.m\.|p\.m\.|malam|petang))', re.IGNORECASE)


def is_mixed_alnum(token):
    return any(c.isalpha() for c in token) and any(c.isdigit() for c in token)


def is_only_digits_and_dashes(token):
    return all(c.isdigit() or c in '+-' for c in token.replace('-', ''))


def normalize_percentage(m):
    number = m.group(1)
    if '.' in number:
        whole, frac = number.split('.')
        return f"{num2word(int(whole))} perpuluhan {num2word(int(frac))} peratus"
    else:
        return f"{num2word(int(number))} peratus"


def normalize_time(m):
    hour, minute, meridian = m.groups()
    hour_word = num2word(int(hour))
    minute_word = num2word(int(minute))

    meridian_word = ''
    if meridian:
        if len(meridian) > 2:
            meridian_word = meridian
        else:
            meridian_word = f"{meridian[0]} m"

    if minute_word == 'kosong':
        return f"{hour_word} {meridian_word}".strip()
    else:
        return f"{hour_word} {minute_word} {meridian_word}".strip()


def normalize_date(m):
    day, month, year = m.groups()
    month_name = _months.get(month.lstrip("0"), month)
    return f"{num2word(int(day))} {month_name} {num2word(int(year))}"


def normalize_currency(m):
    symbol, amount = m.groups()
    amount = amount.replace(",", "")
    if symbol.upper() == 'RM':
        unit_main, unit_sub = 'ringgit', 'sen'
    elif symbol == '$':
        unit_main, unit_sub = 'dollar', 'sen'
    elif symbol == '£':
        unit_main, unit_sub = 'pound', 'pence'
    elif symbol == '€':
        unit_main, unit_sub = 'euro', 'sen'
    elif symbol == 'USD':
        unit_main, unit_sub = 'dollar', 'sen'
    elif symbol == 'MYR':
        unit_main, unit_sub = 'ringgit', 'sen'
    else:
        unit_main, unit_sub = 'unit', 'subunit'

    if '.' in amount:
        ringgit, sen = amount.split('.')
        if sen != '00':
            return f"{num2word(int(ringgit))} {unit_main} {num2word(int(sen[:2]))} {unit_sub}"
        else:
            return f"{num2word(int(ringgit))} {unit_main}"
    else:
        return f"{num2word(int(amount))} {unit_main}"


def normalize_decimal(m):
    return f"{num2word(int(m.group(1)))} perpuluhan {num2word(int(m.group(2)))}"


def normalize_dashed_digits(m):
    raw = m.group(1)
    return ' '.join(numbers_mapping_malay.get(ch, ch) for ch in raw if ch in numbers_mapping_malay)


def normalize_mixed_alnum(m):
    token = m.group(0)
    if is_only_digits_and_dashes(token):
        return token
    if is_mixed_alnum(token):
        return ' '.join(numbers_mapping_malay.get(ch, ch.upper()) for ch in token if ch.isalnum())
    return token


def normalize_number(m):
    if len(m.group(0)) > 4:
        return ' '.join(num2word(int(digit)) for digit in m.group(0))
    else:
        return num2word(int(m.group(0)))


def normalize_malay(text: str) -> str:
    """Main Malay text normalization function."""
    text = re.sub(_date_re, normalize_date, text)
    text = re.sub(_currency_re, normalize_currency, text)
    text = re.sub(_time_re, normalize_time, text)
    text = re.sub(_percentage_re, normalize_percentage, text)
    text = re.sub(_decimal_re, normalize_decimal, text)
    text = re.sub(_dashed_digit_re, normalize_dashed_digits, text)
    text = re.sub(_alnum_re, normalize_mixed_alnum, text)
    text = re.sub(_number_re, normalize_number, text)
    return text
