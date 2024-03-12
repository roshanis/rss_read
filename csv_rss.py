import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import openai

# Load environment variables from .env
load_dotenv()

# Get OpenAI API key and CSV file path from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
csv_file_path = os.getenv("CSV_FILE_PATH")

def extract_text(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all paragraphs
    paragraphs = soup.find_all('p')
    # Concatenate paragraphs into a single string
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def summarize_article(url):
    # Extract article content
    article_content = extract_text(url)

    # Summarize the article using OpenAI
    response = openai.Completion.create(
        engine="davinci",
        prompt=article_content,
        max_tokens=100
    )

    return response['choices'][0]['text'].strip()

def main():
    # Read URLs from CSV
    df = pd.read_csv(csv_file_path)

    for index, row in df.iterrows():
        url = row['URL']
        print(f"Summarizing article from: {url}")
        summary = summarize_article(url)
        print("Summary:", summary)
        print()

if __name__ == "__main__":
    main()
