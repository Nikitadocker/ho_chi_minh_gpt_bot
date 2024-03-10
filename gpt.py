from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv('telegramm_bot/.env')
OPEN_AI_API = os.getenv("OPEN_AI_API")

client = OpenAI(api_key=OPEN_AI_API)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a soviet comrade helpful assistant."},
        {"role": "user", "content": "Что ты думаешь о товарище Xошимине?"}
    ]
)
# Access text content from "message" within the first "Choice"
ai_response = response.choices[0].message.content
print(ai_response.strip())