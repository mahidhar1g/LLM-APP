import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from src.web_extraction.search_results_extractor import parsing_data

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_embeddings(data):
    """
    Generate embeddings for a list of data items.

    Args:
        data (list): List of dictionaries containing 'content' to be embedded.

    Returns:
        list: List of dictionaries with embeddings and metadata.
    """
    embedded_data = []
    for item in data:
        try:
            # Generate embeddings for the content
            response = client.embeddings.create(
                input=item["content"],
                model="text-embedding-3-small"
            )
            embedding = response.data[0].embedding

            # Prepare the data with metadata
            embedded_data.append({
                "id": str(item["id"]),
                "embedding": embedding,
                "metadata": item["metadata"]
            })
        except Exception as e:
            print(f"Error generating embedding for ID {item['id']}: {e}")
    
    return embedded_data

def process_embeddings():
    # Step 1: Parse data using the search_results_extractor
    parsed_data = parsing_data()
    if not parsed_data:
        print("No data to process.")
        return

    # Step 2: Format parsed data for embedding
    formatted_data = [
        {
            "id": item["id"],
            "content": item["content"],
            "metadata": {
                "title": item["metadata"]["title"],
                "link": item["metadata"]["link"]
            }
        }
        for item in parsed_data
    ]

    # Step 3: Generate embeddings
    print("Generating embeddings...")
    embedded_data = generate_embeddings(formatted_data)
    
    return embedded_data