# Alepa Fillarit Käpylä

A small Python script to fetch Alepa city bike availability for Pohjolankatu and Koskelantie stations in Helsinki using the Digitransit API.

## Requirements

- Python 3.8+
- A Digitransit API key (free to get from [https://digitransit.fi/en/developers/api-registration/](https://digitransit.fi/en/developers/api-registration/))

## Setup

1. Clone this repository
2. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

3. Edit `.env` and insert your API key:

```
DIGITRANSIT_API_KEY=your_api_key_here
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the script:

```bash
python alepa-fillarit-kapyla.py
```
