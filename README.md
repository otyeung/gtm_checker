# gtm_checker

## What is it

A python script that analyse whether a web site has GTM scripts installed. It will parse the web page as well as embedded javascript files for any GTM tags.

## How to Install

Clone the repository

```
git clone https://github.com/otyeung/gtm_checker.git
```

With Python 3.x, create virtual environment and activate it :

```
virtualenv env
source env/bin/activate
pip install -r requirements.txt --yes
```

## How to run

The input csv file should contain a column "company_url", it's the only requirement. The python script will crawl the url and generate a new CSV file in the same directory with name "<filename>\_gtm.csv". The file will contain one additonal columns "Use GTM" with 3 possible values "yes", "no", "n/a".

- "yes" means GTM tag is detected
- "no" means GTM tag is not deteced
- "n/a" unable to determine

```
python gtm_checker.py <csv_filename>
```

### Example

```
python gtm_checker.py url.csv
```

An output file "url_gtm.csv" will be generated.

## Limitation

Three (probably more) possible reasons for showing "n/a" / not able to detect GTM :

1. Urls are unreachable
2. The Urls might have security measures in place that prevent automated access, e.g. CAPTCHA
3. GTM tags are deployed in the website using an unknown pattern (e.g. iframe etc)
