"""테스트 패키지."""

from book.utils import to_table
from django.test import TestCase


class YourTestClass(TestCase):
    """
    일단은 더미 Test Case.

    TODO: 추후 보강
    """

    @classmethod
    def setUpTestData(cls):
        """
        테스트 데이터 setup.

        :return:
        """
        print(
            "setUpTestData: Run once to set up non-modified data for all class methods."
        )

    def setUp(self):
        """
        테스트 setUp.

        :return:
        """
        print("setUp: Run once for every test method to setup clean data.")

    def test_one_plus_one_equals_two(self):
        """
        Sample Test.

        :return:
        """
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

    def test_make_table(self):
        """
        Table 만드는 함수의 테스트.

        :return:
        """
        contents = range(10)
        table = to_table(contents, 3)
        assert table == [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]

        contents = range(10)
        table = to_table(contents, 4)
        assert table == [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]
