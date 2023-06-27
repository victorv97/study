import os
import unittest
from io import StringIO
from unittest.mock import patch
from analyzer import code_analyzer


def test_template(test_case, test_output):
    with open(os.path.join('output', test_output)) as file:
        expected_output = file.read()

    with patch('sys.stdout', new=StringIO()) as fake_out:
        fake_input = os.path.join('cases', test_case)
        with patch('sys.argv', ['analyzer\\code_analyzer.py', fake_input]):
            code_analyzer.main()
            actual_output = fake_out.getvalue()
    return expected_output, actual_output


class TestAnalyzer(unittest.TestCase):

    def test_1(self):
        expected_output, actual_output = test_template('test_1.py', 'test_1.txt')
        self.assertEqual(expected_output, actual_output)

    def test_2(self):
        expected_output, actual_output = test_template('test_2.py', 'test_2.txt')
        self.assertEqual(expected_output, actual_output)

    def test_3(self):
        expected_output, actual_output = test_template('test_3.py', 'test_3.txt')
        self.assertEqual(expected_output, actual_output)

    def test_4(self):
        expected_output, actual_output = test_template('test_4.py', 'test_4.txt')
        self.assertEqual(expected_output, actual_output)

    def test_5(self):
        expected_output, actual_output = test_template('test_5.py', 'test_5.txt')
        self.assertEqual(expected_output, actual_output)

    def test_6(self):
        expected_output, actual_output = test_template('', 'test_6.txt')
        self.assertEqual(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()
