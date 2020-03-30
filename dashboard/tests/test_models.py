from book.utils import to_table
from django.test import TestCase


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print(
            "setUpTestData: Run once to set up non-modified data for all class methods."
        )

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def test_make_table(self):
        contents = range(10)
        table = to_table(contents, 3)
        assert table == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        contents = range(10)
        table = to_table(contents, 4)
        assert table == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
