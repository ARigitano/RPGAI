from openai import OpenAI
import os

# Read the API key from the text file
api_key_file = os.path.join(os.path.dirname(__file__), 'api_key.txt')
with open(api_key_file, 'r') as f:
    OPENAI_API_KEY = f.read().strip()

client = OpenAI(api_key=OPENAI_API_KEY)


def call_openai_api(prompt, max_tokens, temperature=0.7):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return response.choices[0].text.strip()