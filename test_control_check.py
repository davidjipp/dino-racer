import unittest
import unittest.mock as mock
from main import *


class MyTestCase(unittest.TestCase):
    @mock.patch("random.randint")
    def test_control_check_crit_failure(self, patched_randint):
        jockey = Jockey("test", 10)
        dino = Dino("dino", 10, 50)

        patched_randint.return_value = 1

        expected = False
        actual = control_check(jockey, dino)

        self.assertEqual(expected, actual)

    @mock.patch("random.randint")
    def test_control_check_crit_success(self, patched_randint):
        jockey = Jockey("test", 10)
        dino = Dino("dino", 10, 50)

        patched_randint.return_value = 20

        expected = True
        actual = control_check(jockey, dino)

        self.assertEqual(expected, actual)

    @mock.patch("random.randint")
    def test_control_check_greater_than_ferocity_success(self, patched_randint):
        jockey = Jockey("test", 5)
        dino = Dino("dino", 10, 50)

        patched_randint.return_value = 6

        expected = True
        actual = control_check(jockey, dino)

        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
