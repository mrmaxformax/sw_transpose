import io
import logging
import os
import unittest.mock
from os.path import join
from unittest.mock import patch

from main import transpose, file_reading, parse_args, main


class TestTranspose(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.raw_data = ['a', 'ab', '', ' ', 'abc', '33', 'False', 'abcd', 'abcde', 'YGKNkfdfs', 'Sierra_Nevada',
                        'Sierra-Nevada', 'Sierra - Nevada', 'SierraNevada', 'Sierra Nevada']
        cls.data = ['a', 'ab', 'abc', '33', 'False', 'abcd', 'abcde', 'YGKNkfdfs', 'Sierra_Nevada', 'Sierra-Nevada',
                    'Sierra - Nevada', 'SierraNevada', 'Sierra Nevada']
        cls.test_file_name = 'test_word_list.txt'
        cls.project_root = join(os.getcwd(), 'txt_files')
        cls.path = join(cls.project_root, cls.test_file_name)
        logging.disable(logging.CRITICAL)

        with open(cls.path, 'w') as f:
            for data in cls.raw_data:
                f.write(data + '\n')

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.path)
        except IOError as e:
            print(e)

    def test_file_reads_correctly(self):
        actual_data = file_reading(file_path=self.path)
        self.assertEqual(self.data, actual_data)

    def test_no_empty_elements_in_list(self):
        actual_data = file_reading(file_path=self.path)
        for item in actual_data:
            self.assertTrue(len(item) > 0)

    def test_correct_type_returned(self):
        actual_data = file_reading(file_path=self.path)
        self.assertTrue(isinstance(actual_data, list))

    def test_wrong_file_format(self):
        path = join(self.project_root, 'test_word_list.doc')
        with self.assertRaises(SystemExit) as cm:
            file_reading(file_path=path)
        self.assertEqual(cm.exception.code, 1)

    def test_wrong_file_path(self):
        with self.assertRaises(SystemExit) as cm:
            file_reading(file_path='/Users/Transpose/txt_files/empty_word_list1.txt')
        self.assertEqual(cm.exception.code, 1)

    def test_empty_file_path(self):
        with self.assertRaises(SystemExit) as cm:
            file_reading(file_path='')
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_we_get_longest_transposed_word(self, mock_stdout):
        transpose(string_list=self.raw_data)
        self.assertEqual(mock_stdout.getvalue(), 'Original: Sierra_Nevada\nTransposed: adaveN_arreiS\n\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_we_get_only_one_word(self, mock_stdout):
        data = ["cool"]
        transpose(string_list=data)
        self.assertEqual(mock_stdout.getvalue(), 'Original: cool\nTransposed: looc\n\n')

    def test_empty_list(self):
        data = []
        with self.assertRaises(SystemExit) as cm:
            transpose(string_list=data)
        self.assertEqual(cm.exception.code, 1)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_empty_string(self, mock_stdout):
        data = [""]
        transpose(string_list=data)
        self.assertEqual(mock_stdout.getvalue(), 'There is only empty strings. Try to use another file.\n\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_characters(self, mock_stdout):
        data = ["cool@#$!*"]
        transpose(string_list=data)
        self.assertEqual(mock_stdout.getvalue(), 'Original: cool\nTransposed: looc\n\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_digits(self, mock_stdout):
        data = ["346 cool6"]
        transpose(string_list=data)
        self.assertEqual(mock_stdout.getvalue(), 'Original: cool\nTransposed: looc\n\n')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_remove_spaces(self, mock_stdout):
        data = [" Sierra - Nevada "]
        transpose(string_list=data)
        self.assertEqual(mock_stdout.getvalue(), 'Original: Sierra\nTransposed: arreiS\n\n')

    def test_arg_parser_no_args(self):
        parser = []
        with self.assertRaises(SystemExit) as cm:
            parse_args(parser)
        self.assertEqual(cm.exception.code, 2)

    def test_arg_parser_file(self):
        parser = parse_args(['-f', 'test.txt'])
        self.assertEqual(parser.f, 'test.txt')

    def test_arg_parser_path(self):
        parser = parse_args(['-p', '/User/max/'])
        self.assertEqual(parser.p, '/User/max/')

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_e2e(self, mock_stdout):
        main(path=self.path)
        self.assertEqual(mock_stdout.getvalue(), 'Original: Sierra_Nevada\nTransposed: adaveN_arreiS\n\n')

    def test_wrong_file_name_in_main(self):
        test_file_name = 'test_word_list2.txt'
        project_root = join(os.getcwd(), 'txt_files')
        path = join(project_root, test_file_name)

        with self.assertRaises(SystemExit) as cm:
            main(path=path)
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
