import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

#goal: create a class of to take HTML input - take search for book, be able to return bookshelves + frequently downloaded, and scroll

class pgAPI:
    def __init__(self):
        self.html_file = None

    def pageLoader(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            return soup
        except ConnectionError:
            page = requests.get(url)
            return "Error, web request could not be made. Status code is: " + str(page.status_code)

    def quickSearch(self, url):
        soup = self.pageLoader(url)
        if "Error, web request" in soup:
            return soup
        listOfBooks = []
        #Note, the list is truncated, starting from index 2, to leave out unnecessary link information
        #Saves information in dictionary in the following manner: (book link, image link, title, author, downloads)
        for link in soup.find_all('a', attrs={'href': re.compile("ebook")})[3:28]:
            listOfBooks.append((link.get('href'),link.contents[1].contents[1].get("src"),
                                link.contents[3].find("span", re.compile("title")).text,link.contents[3].find("span", re.compile("subtitle")).text,
                               link.contents[3].find("span", re.compile("extra")).text))

        return listOfBooks

    def accessBook(self, url):
        soup = self.pageLoader(url)
        if "Error, web request" in soup:
            return soup



test = "https://www.gutenberg.org/ebooks/search/?query=&submit_search=Go%21"


print(pgAPI().quickSearch(test))