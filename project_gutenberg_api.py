import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

#goal: create a class of to take HTML input - take search for book, be able to return bookshelves + frequently downloaded, and scroll

class pgAPI:
    def __init__(self):
        self.html_file = None
        self.tests = ["https://www.gutenberg.org/ebooks/search/?query=&submit_search=Go%21",
                   "https://www.gutenberg.org/ebooks/search/?query=xajfafahnfkjawebfkaewbfga&submit_search=Go%21",
        "https://www.gutenberg.org/ebooks/search/?query=Digters+uit+Suid-Afrika&submit_search=Go%21"]

    def _pageLoader(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            return soup
        except ConnectionError:
            page = requests.get(url)
            return "Error, web request could not be made. Status code is: " + str(page.status_code)

    def testFunctionality(self, *args):
        #args arguments exists to add further tests.
        tests = self.tests + args
        for link in tests:
            print(self.quickSearch(link))

    def quickSearch(self, url):
        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
        listOfBooks = []
        #Note, the list is truncated, starting from index 2, to leave out unnecessary link information
        #Saves information in dictionary in the following manner: (book link, image link, title, author, downloads)
        searchList = soup.find_all('a', attrs={'href': re.compile("ebook")})
        if len(searchList) <= 6:
            return "No Results."
        afterSortIndex = 26
        for i in range(len(searchList)):
            if searchList[i].get('href')[8] != "s":
                afterSortIndex = i
                break
        for link in searchList[afterSortIndex:]:
            if link.get('href')[8] == "s":
                break
            listOfBooks.append((link.get('href'),link.contents[1].contents[1].get("src"),
                                link.contents[3].find("span", re.compile("title")).text,link.contents[3].find("span", re.compile("subtitle")).text,
                                link.contents[3].find("span", re.compile("extra")).text))

        return listOfBooks

    #provide epub if possible - if not, provide html file, provide a similar books link, other book shelves, and

    def accessBook(self, url):
        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
