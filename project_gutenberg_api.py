import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

#goal: create a class of to take HTML input - take search for book, be able to return bookshelves + frequently downloaded, and scroll

class pgAPI:
    def __init__(self):
        self.html_file = None
        self.openURL = "gutenberg.org"

    def _pageLoader(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            return soup
        except ConnectionError:
            page = requests.get(url)
            return "Error, web request could not be made. Status code is: " + str(page.status_code)

    def formatting(self, str):
        return "".join([s.strip() for s in str.splitlines()])

    def quickSearch(self, url):

        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
        listOfBooks = []
        #Note, the list is truncated, starting from index 2, to leave out unnecessary link information
        #Saves information in dictionary in the following manner: (book link, image link, title, author, downloads)
        searchList = soup.find_all(class_="booklink")

        for bookInfo in searchList:
            listOfBooks.append({"book_link" : self.openURL + bookInfo.find("a", href=re.compile("ebook")).get("href"),
                                "image_link" : self.openURL + bookInfo.find("img").get("src"),
                                #some titles on project gutenberg include \r, should it be removed?
                                "title" : bookInfo.find(class_="title").text,
                                "author" : bookInfo.find(class_="subtitle").text,
                                "download_count" : bookInfo.find(class_="extra").text})
        if listOfBooks:
            try:
                nextPageLink = soup.find_all(class_="statusline")[-1].find(title=re.compile("Go to")).get("href")
            except:
                nextPageLink = "No additional pages."
            return (listOfBooks, nextPageLink)
        else:
            return ("No books found.", "No additional pages.")

    #provide cover, epub, and html file
    #provide a similar books link to readers also downloaded
    #provide title, return author, translator, original publication, and subject

    def accessBook(self, url):
        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
        bookDetails = {}
        try:
            bookDetails["coverPicture"] = soup.find("img", class_="cover-art").get("src")
        except:
            bookDetails["coverPicture"] = "No cover available."
        files = []
        try:
            for file in soup.find_all(class_="unpadded icon_save"):
                files.append({file.find("a", title=re.compile("Download")).text : self.openURL+file.find("a", title=re.compile("Download")).get("href")})
        except:
            files = "No book files found."
        bookDetails["book_files"] = files
        similarBooks = "Similar Books not found."
        try:
            similarBooks = self.openURL+ soup.find(id="more_stuff").find(rel="nofollow").get("href")
        except:
            pass
        bookDetails["similar_books"] = similarBooks
        records = []
        try:
            for row in soup.find("table", class_="bibrec").find_all("tr")[:-1]:
                if row.find("a") and row.find("a", href=re.compile("ebook")):
                    records.append((row.find("th").text, self.formatting(row.find("td").text), self.openURL+row.find("a").get("href")))
                else:
                    records.append((row.find("th").text, self.formatting(row.find("td").text)))
        except:
            records = "Bibliographic record not found."
        bookDetails["records"] = records
        return bookDetails