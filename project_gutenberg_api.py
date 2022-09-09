import requests
import urllib.parse
import re
from bs4 import BeautifulSoup

#API class with functions to scrape search result and book data from Project Gutenberg.

class pgAPI:
    #initialization of API
    def __init__(self):
        #URL variables
        #Used to fix/alter URLs
        self.genericURL = "https://www.gutenberg.org"
        #Used to store current URL
        self.openURL = self.genericURL

    #Method to take a search term and create the URL that leads to the search results.
    def createURL(self, query):
        encodedQuery = urllib.parse.quote(query)
        createdURL = "https://www.gutenberg.org/ebooks/search/?query=" + encodedQuery + "&submit_search=Go%21"
        return createdURL

    #Method to stitch together a search result link, taken from a direct access url call, that was broken up by Flask.
    def reconstructSearchURL(self, remainingLink, term, index):
        index = str(index)
        finalLink = remainingLink + "?query=" + term + "&submit_search=Go%21&start_index=" + index
        return finalLink

    #Method to create a whole, searchable URL from scraped data.
    def constructWholeURL(self, bookURL):
        return "https://www.gutenberg.org/" + bookURL

    #Method to attempt to load web pages; it's independently defined for frequent re-use:
    #Returns page data if website connection is made. Otherwise, it throws a connection error and status code.
    #Method takes a Project Gutenberg search result page URL.
    def _pageLoader(self, url):
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            return soup
        except ConnectionError:
            page = requests.get(url)
            return "Error, web request could not be made. Status code is: " + str(page.status_code)

    #Method to remove new line characters, used multiple times in accessBook()
    def formatting(self, str):
        return "".join([s.strip() for s in str.splitlines()])

    #Method to query Project Gutenberg for books. Returns page data from the list of results.
    def quickSearch(self, url):
        #Loads webpage.
        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
        self.openURL = url
        #List of search result data that will be returned.
        listOfBooks = []

        #List of raw data for each book found in the search result.
        searchList = soup.find_all(class_="booklink")

        #Page information is saved as a list of dictionaries in the following manner:
        #(book link, image link, title, author, downloads)
        #Each dictionary holds information for one book.
        for bookInfo in searchList:
            listOfBooks.append({"book_link" : self.genericURL + bookInfo.find("a", href=re.compile("ebook")).get("href"),
                                "image_link" : self.genericURL + bookInfo.find("img").get("src") if bookInfo.find("img") != None else None,
                                #Some titles on project gutenberg include \r; it is left in the titles.
                                "title" : bookInfo.find(class_="title").text,
                                "author" : bookInfo.find(class_="subtitle").text if bookInfo.find(class_="subtitle") != None else None,
                                "download_count" : bookInfo.find(class_="extra").text})
        #Conditional statement that places the listOfBooks list into a tuple.
        if listOfBooks:
            #If another page of search results exists (pulled with a -1 index from the list of search results since
            #it is always the last element of the list of search results, even if any results aren't found), the link
            #to the next page of search results is placed into the tuple with the listOfBooks list.
            try:
                nextPageLink = self.genericURL + soup.find_all(class_="links")[-1].find(title=re.compile("next")).get("href")
            except:
                #Message "No additional pages." replaces a link to another page of search results if there isn't
                #another page of search results.
                nextPageLink = "No additional pages."
            #A tuple of listOfBooks and the nextPageLink is returned if the search result includes any books.
            return (nextPageLink, listOfBooks)
        else:
            #Message "No books found." replaces the listOfBooks list if there aren't any books found in the search.
            return ("No additional pages.", "No books found.")

    #Method to pull book data:
    #Returns the book cover, all basic book files (excludes zip files, txt files, etc.),
    #a link to a search result page of other books commonly downloaded by users who downloaded the original book,
    #and the bibliographic record of the book.
    #Method takes a Project Gutenberg page of book data URL.
    def accessBook(self, url):
        #Loads webpage.
        soup = self._pageLoader(url)
        if "Error, web request" in soup:
            return soup
        self.openURL = url
        #Dictionary of book data that will be returned.
        bookDetails = {}
        #Key "coverPicture" is added to dictionary, value is the URL for the book cover image file if it can be foumd.
        #If the URL cannot be found, the value is defined as "No cover available." instead.
        try:
            bookDetails["coverPicture"] = soup.find("img", class_="cover-art").get("src")
        except:
            bookDetails["coverPicture"] = "No cover available."
        #List of files for the book.
        files = []
        #If book files can be found, they are appended to the list, with the exception of older files listed under
        #"More Files..." as these extra files are repetitive and generally less useful than the formatted files.
        #If book files cannot be found, the files list is redefined as the string "No book files found."
        try:
            for file in soup.find_all(class_="unpadded icon_save"):
                files.append({file.find("a", title=re.compile("Download")).text : self.openURL+file.find("a", title=re.compile("Download")).get("href")})
        except:
            files = "No book files found."
        #Key "book_files" is added to dictionary, the files variable is defined as the value of the key.
        bookDetails["book_files"] = files
        #similarBooks is the variable that will be assigned as the value for the "similar_books" key. It is a link to
        #a list of books, similar to a search result page.
        similarBooks = self.openURL+ "/also/"
        #The "similar_books" key is defined with similarBooks as the value.
        bookDetails["similar_books"] = similarBooks
        #records is the list of the book's bibliographic record table's rows.
        records = []
        #If records can be found, the text of the record rows are saved as tuples in the format (row title, row info)
        #if the row doesn't have a Project Gutenberg hyperlink. If the row does have a hyperlink, it is added as a
        #third element in the tuple. (Note - hyperlinks to websites other than Project Gutenberg are not saved due
        #to them being less applicable to an API meant to collect information from the Project Gutenberg site)
        #If bibliographic records are not found, the records variable is redefined as "Bibliographic record not found."
        try:
            #-1 index is used to exclude the last row of the Bibliographic Record as it is always a note that
            #doesn't specifically pertain to the book data.
            for row in soup.find("table", class_="bibrec").find_all("tr")[:-1]:
                if row.find("a") and row.find("a", href=re.compile("ebook")):
                    records.append((row.find("th").text, self.formatting(row.find("td").text), self.openURL+row.find("a").get("href")))
                else:
                    records.append((row.find("th").text, self.formatting(row.find("td").text)))
        except:
            records = "Bibliographic record not found."
        #The "records" key is defined with records as the value.
        bookDetails["records"] = records
        #The bookDetails dictionary is returned.
        return bookDetails