# Shodan Account Generator
Updated and optimized version of [Shodan-Generator](https://github.com/Xosrov/Shodan-Generator)

⚠️Warning: Overusing this tool with the same IP address over a short period can trigger Shodan's WAF, resulting in unstable results.

## Install
```bash
git clone https://github.com/jhond0e/Shodan-Generator
cd Shodan-Generator
pip3 install -r requirements.txt
```

## Usage
```
usage: generator.py [-h] [--creds] [--count [COUNT]] [--apikey] [--raw]

Shodan account generator

options:
  -h, --help       show this help message and exit
  --creds          output will only be the credentials
  --count [COUNT]  number of generated accounts (default: 1)
  --apikey         output will only be the api-key
  --raw            output raw data, without any more text
```

## Examples
Generate 3 shodan accounts and only display the API keys :
```bash
~$ python3 generator.py --apikey --raw --count 3
zo6ql2CY1nF*********************
0PSUjYn07Dm*********************
AtF2ucs2bBH*********************
```

Generate one shodan account, display all informations (credientials + API key) :
```bash
~$ python3 generator.py
Account #1 info:
User: jzb50c******
Pass: kpetbsyss9********
API Key: 68hNEhyrdiBcm1y*****************
```

