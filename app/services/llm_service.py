from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generate_response(messages):

    response = client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )

    text = response.choices[0].message.content
    tokens = response.usage.total_tokens

    return text, tokens