from unittest import TestCase
from db import DB


class TestDB(TestCase):

    def test_DB_is_Singleton(self):
        instance = [str(DB()) for i in range(0, 10)]

        self.assertEqual(len(instance), 10)
        self.assertEqual(len(set(instance)), 1)
