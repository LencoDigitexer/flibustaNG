import unittest
from app import api


class TestStringMethods(unittest.TestCase):

    def test(self):
        handler = api.search("тайна часовни ")
        print(handler)
        #print(handler[0]["book"]["details"]["file"]["pdf"])


if __name__ == '__main__':
    unittest.main()