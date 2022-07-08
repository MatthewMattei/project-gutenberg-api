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
        # try:
        #     epubImages = soup.find("a", class_="link", attrs={'href': re.compile("epub.images")})
        # except:
        #     epubImages = "EPUB book file with images cannot be found."
        # try:
        #     epubPlain = soup.find("a", class_="link", attrs={'href': re.compile("epub.noimages")})
        # except:
        #     epubPlain = "EPUB book file without images cannot be found"
        # try:
        #     alsoDownloaded = (soup.find("div", id="more_stuff").find("a", rel="nofollow").get("href"))
        # except:
        #     alsoDownloaded = "Also downloaded link cannot be found"
        # bookAttrs = [coverPicture, html, epubImages, epubPlain, alsoDownloaded]
        # try:
        #     author = soup.find("a", itemprop="creator").text
        # except:
        #     author = "Author cannot be found"
        # try:
        #     translator = soup.find("th", text=re.compile("Translator")).find_next_sibling().text
        # except:
        #     translator = "No translator or no translator found."

pgAPI().accessBook("https://gutenberg.org/ebooks/68462")