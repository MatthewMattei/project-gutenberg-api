import unittest
from project_gutenberg_api import pgAPI

class functionalityTest(unittest.TestCase):
    def test_quick_search(self):
        tests = ["https://www.gutenberg.org/ebooks/search/?query=&submit_search=Go%21",
                 "https://www.gutenberg.org/ebooks/search/?query=xajfafahnfkjawebfkaewbfga&submit_search=Go%21",
                 "https://www.gutenberg.org/ebooks/search/?query=Digters+uit+Suid-Afrika&submit_search=Go%21"]
        sampleAPI = pgAPI()
        for test in tests:
            print(sampleAPI.quickSearch(test))

    # def test_access_book(self):
    #     tests = ["https://gutenberg.org/ebooks/1342",
    #              "https://www.gutenberg.org/ebooks/42302",
    #              "https://gutenberg.org/ebooks/68462"]
    #     sampleAPI = pgAPI()
    #     for test in tests:
    #         print(sampleAPI.accessBook(test))