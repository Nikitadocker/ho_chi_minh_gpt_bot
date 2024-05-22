import os
import unittest

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TestOenAIconnect(unittest.TestCase):  # предоставляем класс TestCase для создания тестовых случаев

    def test_connect_openai(self):

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello"}
        ]
        )

        # print(completion.choices[0].message)
        

        self.assertTrue(completion.choices[0].message, "OpenAI connection  work")

       
        


if __name__ == '__main__': #запускаем тест,эквиталентно команде python3 -m  unittest test-bot.py
    unittest.main()