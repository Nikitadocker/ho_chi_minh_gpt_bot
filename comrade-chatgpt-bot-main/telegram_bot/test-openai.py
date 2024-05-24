import unittest
from bot import check_openai_connection
from openai import OpenAI
import os

class Testopenai(unittest.TestCase):
    def test_check_openai_connection(self):
        
        check_openai_connection()
        
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        )

        

    
    self.assertTrue(completion.choices[0].message, "OpenAI connection  work")




if __name__ == '__main__': #запускаем тест,эквиталентно команде python3 -m  unittest test-bot.py
    unittest.main()