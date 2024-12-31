from openai import OpenAI
from src.config import OPENAI_API_KEY

def get_chat_response(model: str, messages: list, api_key: str = OPENAI_API_KEY) -> str:
    """
    Generates a response from the OpenAI chat model.

    Parameters:
    - model (str): The model to use (e.g., 'gpt-4' or 'gpt-3.5-turbo').
    - messages (list): A list of message dictionaries with 'role' and 'content'.
    - api_key (str): OpenAI API key. Defaults to the value from config.

    Returns:
    - str: The assistant's response content.
    """

    OpenAI.api_key = api_key
    client = OpenAI()
    
    # Create a chat completion
    completion = client.chat.completions.create(
        model=model,
        messages=messages
    )

    # Extract and return the assistant's reply
    return completion.choices[0].message


# Example usage
if __name__ == "__main__":
    messages = [
        {"role": "assistant", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hi"}
    ]
    reply = get_chat_response(model="gpt-4o", messages=messages)
    print(reply)
