import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_ai_response(text):
    response = client.responses.create(
        model="gpt-5-nano",
        input=text
    )
    return response.output_text

