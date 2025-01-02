import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
from embedding_data import process_embeddings

load_dotenv()
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

def store_embeddings(parsed_data):
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "ai-trending-news-embeddings"
    
    # Check if the index already exists
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        print(f"Created Pinecone index '{index_name}'.")
    else:
        print(f"Pinecone index '{index_name}' already exists. Using the existing index.")
    
    # Wait for the index to be ready
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)
    
    index = pc.Index(index_name)
    
    vectors_to_upsert = [
        {
            'id': str(item['id']),
            'values': item['embedding'],
            'metadata': item['metadata']
        }
        for item in parsed_data
    ]
    
    # Upsert data into the Pinecone index
    index.upsert(
        vectors=vectors_to_upsert,
        namespace="ns1"
    )
    
    print(f"Upserted {len(vectors_to_upsert)} vectors into Pinecone index '{index_name}'.")

if __name__ == "__main__":
    embeddings = process_embeddings()
    if embeddings:
        store_embeddings(embeddings)
    else:
        print("No embeddings to store.")
