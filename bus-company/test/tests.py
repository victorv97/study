import os
import unittest
from io import StringIO
from unittest.mock import patch
import bus_data_analyzer


def template(test_case, test_output):
    with open(os.path.join('output', test_output)) as file:
        expected_output = file.read()

    with patch('sys.stdout', new=StringIO()) as fake_out:
        fake_input = StringIO(os.path.join('cases', test_case))
        with patch('sys.stdin', fake_input):
            bus_data_analyzer.main()
            actual_output = fake_out.getvalue()
    return expected_output, actual_output


class TestAnalyzer(unittest.TestCase):

    def test_1(self):
        expected_output, actual_output = template('test_1.json', 'test_1.txt')
        self.assertEqual(actual_output.endswith(expected_output), True)

    def test_2(self):
        expected_output, actual_output = template('test_2.json', 'test_2.txt')
        self.assertEqual(actual_output.endswith(expected_output), True)

    def test_3(self):
        expected_output, actual_output = template('test_3.json', 'test_3.txt')
        self.assertEqual(actual_output.endswith(expected_output), True)

    def test_4(self):
        expected_output, actual_output = template('test_4.json', 'test_4.txt')
        self.assertEqual(actual_output.endswith(expected_output), True)


if __name__ == '__main__':
    unittest.main()
