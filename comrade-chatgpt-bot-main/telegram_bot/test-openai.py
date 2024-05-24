import unittest
from bot import check_openai_connection
from openai import OpenAI
import os

class Testopenai(unittest.TestCase):
    def test_check_openai_connection(self):
    
     self.assertTrue(check_openai_connection())




if __name__ == '__main__': #запускаем тест,эквиталентно команде python3 -m  unittest test-bot.py
    unittest.main()