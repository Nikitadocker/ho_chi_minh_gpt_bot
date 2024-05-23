import unittest
import os
import asyncpg

from openai import OpenAI
# from bot import check_openai_connection
from bot import generate_image
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from telegram import Update, Message, Chat, User, MessageEntity


from unittest.mock import MagicMock
from datetime import datetime, timezone
from telegram import Update, Message, Chat, User, MessageEntity

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class Testbot(unittest.TestCase):
    
   async def test_generate_image(self):
        fake_user = User(
                    id=524046168,
                    first_name='vezyn4ik',
                    is_bot=False,
                    username='vezyn4ik_official',
                    language_code='ru'
                )
        
        fake_chat = Chat(
            id=524046168,
            type='private',
            username='vezyn4ik_official',
            first_name='vezyn4ik'
        )

        fake_message = Message(
            message_id=582,
            from_user=fake_user,
            chat=fake_chat,
            date=datetime(2024, 5, 23, 17, 4, 53, tzinfo=timezone.utc),
            text='/image уставший студент',
            entities=[MessageEntity(type='bot_command', offset=0, length=6)]
        )

        fake_update = Update(
            update_id=748556194,
            message=fake_message
        )   
        
        fake_context = MagicMock()    
        
        await generate_image(update=fake_update,context=fake_context)
        
        
        file_path = "/images/image.png"
        file_size = os.stat(file_path)

        size_in_mb = file_size.st_size / (1024 * 1024)

        # проверка, что размер файла больше 1 МБ
        self.assertTrue(size_in_mb > 1, "File size is less than 1 MB")# проверяем условие на истинну
        
        

# def test_check_openai_connection():
    
    
# class TestFileSize(unittest.TestCase):  # предоставляем класс TestCase для создания тестовых случаев

#     def test_file_size(self):
#         file_path = "/images/image.png"
#         file_size = os.stat(file_path)

#         size_in_mb = file_size.st_size / (1024 * 1024)

#         # проверка, что размер файла больше 1 МБ
#         self.assertTrue(size_in_mb > 1, "File size is less than 1 MB")# проверяем условие на истинну
        
#     def test_connect_openai(self):
        
#         client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


#         completion = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": "Hello"}
#         ]
#         )

        

#         self.assertTrue(completion.choices[0].message, "OpenAI connection  work")


if __name__ == '__main__': #запускаем тест,эквиталентно команде python3 -m  unittest test-bot.py
    unittest.main()