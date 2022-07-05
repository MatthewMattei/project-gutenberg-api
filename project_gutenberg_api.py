import requests
from datetime import datetime
from bs4 import BeautifulSoup

#goal: create a class of to take HTML input - take search for book, be able to return bookshelves + frequently downloaded, and scroll

class pgAPI:
    def __init__(self):
        self.html_file = None

    def quickSearch(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
        except ConnectionError:
            page = requests.get(url)
            return "Error, web request could not be made. Status code is: " + str(page.status_code)
        listOfBooks = []
        #Note, the list is truncated, starting from index 2, to leave out unnecessary link information
        #Saves information in dictionary in the following manner: (book link, image link, title, author, downloads)
        print(soup.find_all("a", class_="link")[2:][0])
        # for book in soup.find_all("a", class_="link")[2:]:
        #     #Adds 6 to ensure bookLink starts after the quotation marks around the link rather than on "href", same idea
        #     #continued throughout rest of the loop
        #     hrefValBeginning = book.find("href")+6
        #     hrefValEnding = book.find("\"", hrefValBeginning)
        #     #Shorten string length to make future searches quicker, same idea continued throughout rest of loop
        #     bookLink = book[hrefValBeginning:hrefValEnding]
        #     book = book[hrefValEnding:]
        #     #Line break for easier readability
        #     srcValueBeginning = book.find("src")+5
        #     srcValueEnding = book.find("\"", srcValueBeginning)
        #     imageLink = book[srcValueBeginning:srcValueEnding]
        #     book = book[srcValueEnding:]
        #     # Line break for easier readability
        #     titleValueBeginning = book.find("title")+7
        #     titleValueEnding = book.find("<", titleValueBeginning)
        #     title = book[titleValueBeginning:titleValueEnding]
        #     book = book[titleValueEnding:]
        #     # Line break for easier readability
        #     subtitleValueBeginning = book.find("subtitle") + 10
        #     subtitleValueEnding = book.find("<", subtitleValueBeginning)
        #     subtitle = book[subtitleValueBeginning:subtitleValueEnding]
        #     book = book[subtitleValueEnding:]
        #     # Line break for easier readability
        #     downloadValueBeginning = book.find("extra") + 7
        #     downloadValueEnding = book.find("<", downloadValueBeginning)
        #     downloadNumber = book[downloadValueBeginning:downloadValueEnding]
        #     listOfBooks.append({"book_link" : bookLink, "image_link" : imageLink, "title" : title, "author" : subtitle, "downloads" : downloadNumber})
        # return listOfBooks


test = "https://www.gutenberg.org/ebooks/search/?query=&submit_search=Go%21"

print(pgAPI().quickSearch(test))