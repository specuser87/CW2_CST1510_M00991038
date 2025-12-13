from openai import OpenAI

# Initialize the OpenAI client
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# This is the ONLY function Streamlit will call
def generate_ai_response(text):
    response = client.responses.create(
        model="gpt-5-nano",
        input=text
    )
    return response.output_text
