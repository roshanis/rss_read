import os
import feedparser
import requests
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize
import pandas as pd
from dotenv import load_dotenv
import urllib.parse

# Load environment variables from .env file
load_dotenv()

def remove_unwanted_part(url):
    """
    Removes the unwanted part of the Google Alerts link.
    """
    if url.startswith("https://www.google.com/url?"):
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        if 'url' in query_params:
            return query_params['url'][0]
    return url

def fetch_urls(rss_feed_url):
    """
    Fetches the URLs from the Google Alerts RSS feed.
    """
    try:
        # Parse the RSS feed
        feed = feedparser.parse(rss_feed_url)
        # Extract URLs from feed entries and remove unwanted part
        urls = [remove_unwanted_part(entry.link) for entry in feed.entries]
        return urls
    except Exception as e:
        print("Error fetching URLs from Google Alerts RSS feed:", e)
        return []

def extract_first_two_sentences(url):
    """
    Extracts the first two sentences from the content of the specified URL.
    """
    try:
        # Send a GET request to fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text content from paragraphs
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        # Tokenize text into sentences
        sentences = sent_tokenize(text)
        # Extract the first two sentences
        first_two_sentences = ' '.join(sentences[:2])
        return first_two_sentences
    except Exception as e:
        print(f"Error extracting content from URL {url}: {e}")
        return ''

def main():
    # Fetch Google Alerts RSS feed URL from environment variable
    google_alerts_rss_feed_url = os.getenv("GOOGLE_ALERTS_RSS_FEED_URL")

    if not google_alerts_rss_feed_url:
        print("Error: Google Alerts RSS feed URL not found in .env file.")
        return

    # Fetch URLs from Google Alerts feed
    urls = fetch_urls(google_alerts_rss_feed_url)

    if urls:
        # Initialize lists to store data
        url_data = []
        # Loop through each URL
        for url in urls:
            # Extract the first two sentences
            first_two_sentences = extract_first_two_sentences(url)
            # Append URL and first two sentences to the data list
            url_data.append({'URL': url, 'First Two Sentences': first_two_sentences})
        # Create a DataFrame from the data
        df = pd.DataFrame(url_data)
        # Save the DataFrame as a CSV file
        df.to_csv('google_alerts_summary.csv', index=False)
        print("CSV file saved successfully.")
    else:
        print("No URLs found in Google Alerts feed.")

if __name__ == "__main__":
    main()
