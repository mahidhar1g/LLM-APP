from src.web_extraction.search_results_extractor import parsing_data
from openai import OpenAI

client = OpenAI()

print(parsing_data())

# response = client.embeddings.create(
#     input=parsing_data(),
#     model="text-embedding-3-small"
# )

# print(response.data[0].embedding)
