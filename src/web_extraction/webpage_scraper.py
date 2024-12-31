import requests
from bs4 import BeautifulSoup
import logging
from requests.exceptions import HTTPError, Timeout, ConnectionError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_webpage(url: str) -> dict:
    """
    Scrape data from the specified webpage using Beautiful Soup.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        dict: Extracted title and content from the webpage.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract and return the data
        page_title = soup.title.string if soup.title else "No Title Found"
        paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
        
        return {
            "title": page_title,
            "content": paragraphs[:]  # Return the first 5 paragraphs
        }
    except HTTPError as http_err:
        logger.error(f"HTTP error occurred while scraping {url}: {http_err}")
    except Timeout as timeout_err:
        logger.error(f"Timeout error occurred while scraping {url}: {timeout_err}")
    except ConnectionError as conn_err:
        logger.error(f"Connection error occurred while scraping {url}: {conn_err}")
    except Exception as e:
        logger.error(f"An error occurred while scraping {url}: {e}")
    return None
