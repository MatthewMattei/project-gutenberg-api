# Project Gutenberg API
This repository contains the code for scraping Project Gutenberg search result and book download pages for individual book details including, but not limited to, book titles, the number of book downloads, and the book download links. Full information on exactly what data can be retrieved, and the documentation to do so, can be found below.

The link to the API Testing page (deployed on Heroku): [API](https://matthews-project-gutenberg-api.herokuapp.com/)

API Sample of search results for: [Pride and Prejudice](https://matthews-project-gutenberg-api.herokuapp.com/api/searchTerm/pride%20and%20prejudice)

![PNG](https://github.com/MatthewMattei/project-gutenberg-api/blob/master/GithubAssets/APITesting.png)

## API Usage Documentation
To directly access the API rather than using the testing form, a URL needs to be entered in the following format:
```
https://matthews-project-gutenberg-api.herokuapp.com/api/<dataType>/<givenData>
```
`dataType` is a string that clarifies how to handle the data given to the API. <br>

There are three data types that the API will accept: <br>
`searchTerm` - this indicates that you have a string that you want the API to make search the Project Gutenberg database for and scrape. <br>
`searchLink` - this indicates that you have a link to a specific search result page that you want the API to scrape data from. <br> 
`bookLink` - this indicates that you have a link to a book download page that you want the API to scrape data from. <br>

`givenData` is the data that you want entered into the API. <br>

The format of entered data is specific to the dataType that is defined: <br>

`searchTerm` takes any string. <br>
Example entry: `Pride and Prejudice` <br>
Full URL search example: `https://matthews-project-gutenberg-api.herokuapp.com/api/searchTerm/pride%20and%20prejudice` <br>

`searchLink` takes a url in the format `https://www.gutenberg.org/ebooks/search/?query=<Some search parameter here>&submit_search=Go%21&start_index=<Some index here>` <br>
Example entry: `https://www.gutenberg.org/ebooks/search/?query=pride+and+prejudice&submit_search=Go%21&start_index=1` <br>
Full URL search example: `https://matthews-project-gutenberg-api.herokuapp.com/api/searchLink/https://www.gutenberg.org/ebooks/search/?query=pride+and+prejudice&submit_search=Go%21&start_index=1` <br>

`bookLink` takes a url in the format `https://www.gutenberg.org/ebooks/<Some book value here>` <br>
Example entry: `https://www.gutenberg.org/ebooks/1260` <br>
Full URL search example: `https://matthews-project-gutenberg-api.herokuapp.com/api/bookLink/https://www.gutenberg.org/ebooks/1260` <br>

## API Data Documentation
API calls for `searchTerm` and `searchLink` both return the same types of data and in the same format:
```
["No additional pages.",[{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/1342","download_count":"53593 downloads","image_link":"https://www.gutenberg.org/cache/epub/1342/pg1342.cover.small.jpg","title":"Pride and Prejudice"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/42671","download_count":"2384 downloads","image_link":"https://www.gutenberg.org/cache/epub/42671/pg42671.cover.small.jpg","title":"Pride and Prejudice"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/31100","download_count":"610 downloads","image_link":"https://www.gutenberg.org/cache/epub/31100/pg31100.cover.small.jpg","title":"The Complete Project Gutenberg Works of Jane Austen"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/20687","download_count":"401 downloads","image_link":null,"title":"Pride and Prejudice"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/20686","download_count":"236 downloads","image_link":null,"title":"Pride and Prejudice"},{"author":"Jane Austen and Mrs. Steele MacKaye","book_link":"https://www.gutenberg.org/ebooks/37431","download_count":"219 downloads","image_link":"https://www.gutenberg.org/cache/epub/37431/pg37431.cover.small.jpg","title":"Pride and Prejudice, a play founded on Jane Austen's novel"},{"author":null,"book_link":"https://www.gutenberg.org/ebooks/10471","download_count":"207 downloads","image_link":"https://www.gutenberg.org/cache/epub/10471/pg10471.cover.small.jpg","title":"The World's Greatest Books \u2014 Volume 01 \u2014 Fiction"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/26301","download_count":"191 downloads","image_link":null,"title":"Pride and Prejudice"},{"author":"Jane Austen","book_link":"https://www.gutenberg.org/ebooks/45186","download_count":"33 downloads","image_link":"https://www.gutenberg.org/cache/epub/45186/pg45186.cover.small.jpg","title":"Ylpeys ja ennakkoluulo (Finnish)"}]]
```
The returned result above is a Response object with the application/json mimetype set. <br>
The first item is either a link to an additional page of results or a "No additional pages." statement. <br>
Every item thereafter is a book entry in the format of a JSON object with the following information: <br>
`author` - the author(s) of the work. (Note: can return null) <br>
`book_link`- the link to the book's download and information page. <br>
`download_count`- the number of times the work was downloaded from Project Gutenberg in the last 30 days. (Note: can return null) <br>
`image_link`- the link to the image file of the book cover. (Note: can return null) <br>
`title` - the title of the work. <br>

API calls for `bookLink` also return a Response object with the application/json mimetype set in the below format:
```
{"book_files":[{"Read this book online: HTML":"https://www.gutenberg.org/ebooks/1260/files/1260/1260-h/1260-h.htm"},{"EPUB (with images)":"https://www.gutenberg.org/ebooks/1260/ebooks/1260.epub.images"},{"EPUB (no images)":"https://www.gutenberg.org/ebooks/1260/ebooks/1260.epub.noimages"},{"Kindle (with images)":"https://www.gutenberg.org/ebooks/1260/ebooks/1260.kindle.images"},{"Kindle (no images)":"https://www.gutenberg.org/ebooks/1260/ebooks/1260.kindle.noimages"},{"Plain Text UTF-8":"https://www.gutenberg.org/ebooks/1260/files/1260/1260-0.txt"}],"coverPicture":"https://www.gutenberg.org/cache/epub/1260/pg1260.cover.medium.jpg","records":[["Author","Bront\u00eb, Charlotte, 1816-1855","https://www.gutenberg.org/ebooks/1260/ebooks/author/408"],["Illustrator","Townsend, F. H. (Frederick Henry), 1868-1920","https://www.gutenberg.org/ebooks/1260/ebooks/author/9854"],["Title","Jane Eyre: An Autobiography"],["Language","English"],["LoC Class","PR: Language and Literatures: English literature"],["Subject","Orphans -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/99"],["Subject","England -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/1702"],["Subject","Young women -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2481"],["Subject","Love stories","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2487"],["Subject","Governesses -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2530"],["Subject","Fathers and daughters -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2531"],["Subject","Mentally ill women -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2532"],["Subject","Charity-schools -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2533"],["Subject","Married people -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2534"],["Subject","Country homes -- Fiction","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2535"],["Subject","Bildungsromans","https://www.gutenberg.org/ebooks/1260/ebooks/subject/2536"],["Category","Text"],["EBook-No.","1260"],["Release Date","Mar 1, 1998"],["Copyright Status","Public domain in the USA."],["Downloads","10743 downloads in the last 30 days."]],"similar_books":"https://www.gutenberg.org/ebooks/1260/ebooks/1260/also/"}
```
`book_files` - a list of the book format names and their associated book files to download. <br>
`cover_picture` - a link to the image of the book cover. (Note: can return null) <br>
`records` - a list of the records associated with the book (potentially includes: title, author, subject(s), and more) <br>
`similar_books` - a link to a search result of similar books. <br>
