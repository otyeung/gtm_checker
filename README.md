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

The input csv file should contain a column "company_url", it's the only requirement. The python script will crawl the url and generate a new CSV file in the same directory with name "<filename>\_gtm.csv". The file will contain one additonal columns "Use GTM" with these possible values :

- "yes" means GTM tag is detected
- "no" means GTM tag is not deteced
- 'HTTPError', '403 Client Error: Forbidden for url' means the URL has blocked access
- 'HTTPError', '404 Client Error: Not Found for url' means the URL is invalid
- 'ConnectionError' means the URL is unreachable
- 'Max retries exceeded' means the site takes too long to be loaded completely and it's timeout

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
2. The Urls might have security measures in place that blocked automated access, e.g. CAPTCHA or Cloudflare
3. GTM tags are deployed in the website using an unknown pattern (e.g. iframe etc)
