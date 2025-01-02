import json
import logging
import re
from langchain_community.utilities import GoogleSerperAPIWrapper
from src.web_extraction.webpage_scraper import scrape_webpage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not GOOGLE_API_KEY or not SERPER_API_KEY:
    raise ValueError("API keys for Google or Serper are missing. Please check your .env file.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_search(query: str, num_results: int = 10) -> dict:
    """
    Perform a search using the Google Serper API.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to retrieve.

    Returns:
        dict: The search results.
    """
    try:
        search = GoogleSerperAPIWrapper(
            k=num_results,
            type="search",
            tbs="qdr:d"  # Restrict results to the past 24 hours
        )
        response = search.results(query)
        return response
    except Exception as e:
        logger.error(f"An error occurred during the search: {e}")
        raise

def extract_links_from_organic_results(results: dict) -> list:
    """
    Extract links from the organic search results.

    Args:
        results (dict): The search results.

    Returns:
        list: A list of links from the organic array.
    """
    try:
        organic_results = results.get("organic", [])
        links = [result["link"] for result in organic_results if "link" in result]
        return links
    except KeyError as e:
        logger.error(f"Error extracting links: {e}")
        return []

def process_scraped_data(scraped_data: dict) -> dict:
    """
    Process scraped data into a structured format, filtering out unnecessary content.

    Args:
        scraped_data (dict): The scraped data from a webpage.

    Returns:
        dict: A structured representation of the scraped data.
    """
    content = '\n'.join(scraped_data.get('content', []))

    # Define patterns to remove unnecessary text
    unnecessary_patterns = [
        r"Subscribe for unlimited access.*",
        r"© \d{4}.*All Rights Reserved",
        r"Please enter a search term.*",
        r".*Privacy Policy.*",
        r"Follow Us.*",
        r".*Subscribe.*",
        r"Related Terms.*"
    ]

    # Filter out matching patterns
    for pattern in unnecessary_patterns:
        content = re.sub(pattern, '', content, flags=re.IGNORECASE)

    # Skip entries with empty or near-empty content
    if not content.strip():
        return None

    return {
        'title': scraped_data.get('title', 'No Title'),
        'content': content.strip().replace("\n", " ")
    }

def parsing_data():
    query = "Artificial Intelligence OR AI news OR AI updates OR AI advancements OR AI breakthroughs OR AI applications"
    parsed_data = []

    try:
        search_results = perform_search(query)
        links = extract_links_from_organic_results(search_results)

        print("\n=== AI News Summary (Last 24 Hours) ===\n")

        tempid = 1
        for idx, link in enumerate(links, start=1):
            scraped_data = scrape_webpage(link)

            if scraped_data:
                structured_data = process_scraped_data(scraped_data)
                if structured_data:  # Only add entries with non-empty content
                    parsed_data.append({
                        'id': tempid,  # Sequential ID
                        'title': structured_data['title'],
                        'link': link,
                        'text': structured_data['content']
                    })
                    tempid += 1
        # Return the parsed data
        return parsed_data

    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")