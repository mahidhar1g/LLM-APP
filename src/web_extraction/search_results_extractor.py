import json
import logging
from langchain_community.utilities import GoogleSerperAPIWrapper
from webpage_scraper import scrape_webpage
from src.config import GOOGLE_API_KEY, SERPER_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def perform_search(query: str, num_results: int = 25) -> dict:
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

def main():
    query = "Artificial Intelligence OR AI news OR AI updates OR AI advancements OR AI breakthroughs OR AI applications"
    try:
        search_results = perform_search(query)
        links = extract_links_from_organic_results(search_results)

        print("\n=== AI News Summary (Last 24 Hours) ===\n")
        for idx, link in enumerate(links, start=1):
            scraped_data = scrape_webpage(link)
            if scraped_data:
                print(f"Article {idx}")
                print(f"Link: {link}")
                print(f"Title: {scraped_data['title']}\n")
                print("Content:")
                for paragraph in scraped_data["content"]:
                    print(f"- {paragraph}")
                print("\n" + "="*80 + "\n")
            else:
                print(f"Article {idx}")
                print(f"Link: {link}")
                print("Failed to extract content.\n")
                print("\n" + "="*80 + "\n")

    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")

if __name__ == "__main__":
    main()
