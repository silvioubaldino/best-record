import unittest
from fileManager import is_file_older_than

class TestFileManager(unittest.TestCase):

    def test_is_file_older_than_x_minutes(self):
        # Testa um arquivo que é mais antigo que 30 minutos
        file_name = 'fullRecord-camera0-21-05-2024_211826.avi'
        self.assertTrue(is_file_older_than(file_name, 30))

        # Testa um arquivo que não é mais antigo que 30 minutos
        file_name = 'fullRecord-camera0-21-05-2024_221826.avi'
        self.assertFalse(is_file_older_than(file_name, 30))

        # Testa um arquivo com um nome que não segue o padrão esperado
        file_name = 'invalid_file_name.avi'
        self.assertFalse(is_file_older_than(file_name, 30))

if __name__ == '__main__':
    unittest.main()