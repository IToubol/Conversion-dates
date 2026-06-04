# ממיר תאריכים | Hebrew Date Converter

A bilingual (Hebrew/Civil) date conversion tool with a Streamlit web interface.

## Features

- Convert Hebrew dates to Gregorian dates
- Convert Gregorian dates to Hebrew dates
- Handles leap years (שנה מעוברת), variable month lengths (Heshvan/Kislev)
- Interface in Hebrew

## Stack

- Python 3
- Streamlit

## Project Structure
```
├─ calendarcomputing.py  # Core calendar logic (Hebrew calendar algorithms)
└─ memir.py              # Streamlit web interface
```
## Run locally

```bash
pip install streamlit
streamlit run memir.py
```

## How it works

`calendarcomputing.py` implements the Hebrew calendar computation from scratch:
- **Molad** calculation (lunar cycle approximation)
- **Dechiyot** rules (postponement rules for Rosh Hashana)
- Bidirectional conversion between Hebrew and Gregorian day counts

`memir.py` is the Streamlit UI layer, with two panels:
- Right panel: Gregorian → Hebrew
- Left panel: Hebrew → Gregorian

## Notes

- Hebrew year input must be a number (e.g. `5785`)
- The app dynamically adds Adar Aleph/Bet options for leap years
