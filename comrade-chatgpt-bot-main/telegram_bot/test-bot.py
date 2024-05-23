import unittest
import os
from openai import OpenAI


class TestFileSize(unittest.TestCase):  # предоставляем класс TestCase для создания тестовых случаев

    def test_file_size(self):
        file_path = "/images/image.png"
        file_size = os.stat(file_path)

        size_in_mb = file_size.st_size / (1024 * 1024)

        # проверка, что размер файла больше 1 МБ
        self.assertTrue(size_in_mb > 1, "File size is less than 1 MB")# проверяем условие на истинну
        
    def test_connect_openai(self):
        
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