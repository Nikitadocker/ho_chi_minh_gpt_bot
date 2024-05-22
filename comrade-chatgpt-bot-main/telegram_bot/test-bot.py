import unittest
import os

class TestFileSize(unittest.TestCase):  # предоставляем класс TestCase для создания тестовых случаев

    def test_file_size(self):
        file_path = "./restore.yaml"
        file_size = os.stat(file_path)

        size_in_mb = file_size.st_size / (1024 * 1024)

        # проверка, что размер файла больше 1 МБ
        self.assertTrue(size_in_mb > 1, "File size is less than 1 MB")# проверяем условие на истинну


if __name__ == '__main__': #запускаем тест,эквиталентно команде python3 -m  unittest test-bot.py
    unittest.main()