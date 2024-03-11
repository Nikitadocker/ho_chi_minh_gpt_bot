import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPEN_AI_API")

client = OpenAI(api_key=OPENAI_API_KEY)

PROMPT = "Vietnamese resident"


response = client.images.generate(
  model="dall-e-3",
  prompt=PROMPT,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)
