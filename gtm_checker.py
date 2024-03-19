import sys
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import time
from multiprocessing import Pool

def extract_js_urls(html_content, base_url):
    """Extract JavaScript file URLs from HTML content."""
    js_urls = []
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tags = soup.find_all('script', src=True)
    for tag in script_tags:
        js_url = tag['src']
        if js_url.startswith('//'):
            js_url = 'https:' + js_url
        elif not js_url.startswith('http'):
            js_url = base_url + '/' + js_url.lstrip('/')
        js_urls.append(js_url)
    return js_urls

def search_for_google_tags(content):
    """Search for Google Tag Manager or Google Analytics tags."""
    gtm_regex = re.compile(r'(googletagmanager\.com|googletagmanager\.gtag\.js)')
    gtag_regex = re.compile(r'www\.googletagmanager\.com\/gtag\/js\?id=')
    gtm_detected = False

    if gtm_regex.search(content) or gtag_regex.search(content):
        gtm_detected = True

    return gtm_detected

def crawl_website(domain):
    """Crawl a website and search for Google Tag Manager tags."""
    try:
        website_url = domain if domain.startswith(('http://', 'https://')) else 'https://' + domain

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        }

        response = requests.get(website_url, headers=headers, allow_redirects=True, timeout=10)  # Allow redirects and set timeout to 10 seconds
        response.raise_for_status()

        base_url = response.url.split('//')[0] + '//' + response.url.split('//')[1].split('/')[0]
        html_content = response.text

        # Search for Google Tag Manager tags in HTML content
        gtm_detected = search_for_google_tags(html_content)

        # Extract JavaScript URLs from HTML content and search for Google Tag Manager tags in them
        js_urls = extract_js_urls(html_content, base_url)
        for js_url in js_urls:
            js_response = requests.get(js_url, headers=headers, timeout=10)
            js_response.raise_for_status()
            js_content = js_response.text
            if not gtm_detected:
                gtm_detected = search_for_google_tags(js_content)

        # Update detection flags
        gtm_use = 'yes' if gtm_detected else 'no'

        return gtm_use

    except requests.exceptions.HTTPError as e:
        return 'n/a'
    except requests.exceptions.ConnectionError as e:
        return 'n/a'
    except requests.exceptions.Timeout:
        return 'n/a'
    except Exception as e:
        return 'n/a'

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python gtm_checker.py <csv_filename>")
        sys.exit(1)

    csv_filename = sys.argv[1]

    # Read CSV into DataFrame
    try:
        df = pd.read_csv(csv_filename)
    except FileNotFoundError:
        print("Error: CSV file not found.")
        sys.exit(1)
    except pd.errors.ParserError:
        print("Error: Invalid CSV file format.")
        sys.exit(1)

    start_time = time.time()  # Start time for the entire script
    total_domains = len(df)
    domains_processed = 0

    print(f"Processing {domains_processed} of {total_domains} domains, elapsed time: 0 seconds")

    # Multiprocessing
    pool = Pool(processes=min(20, os.cpu_count()))  # Limiting to a maximum of 20 concurrent processes
    results = []
    for result in pool.imap_unordered(crawl_website, df['company_url']):
        domains_processed += 1
        elapsed_time = time.time() - start_time
        print(f"Processing {domains_processed} of {total_domains} domains, elapsed time: {elapsed_time:.2f} seconds")
        results.append(result)
    pool.close()
    pool.join()

    # Assign results to DataFrame
    df['use GTM'] = results

    total_execution_time = time.time() - start_time  # Total execution time of the script
    print(f"\nTotal execution time: {total_execution_time:.2f} seconds")

    # Save updated DataFrame to CSV, overwriting if the file already exists
    output_csv = os.path.splitext(csv_filename)[0] + "_gtm.csv"
    df.to_csv(output_csv, index=False, mode='w')

    print("\nCrawling and analysis completed. Results saved to:", output_csv)
