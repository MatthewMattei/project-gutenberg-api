from project_gutenberg_api import pgAPI
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

#Default route to open API Testing page
@app.route('/')
def welcome():
    return render_template("index.html")

#Calls to access API functionality either through the API Testing page
@app.route('/api', methods = ["POST", "GET"])
#or through a direct access url call.
@app.route("/api/<string:dataType>/<path:givenData>")
def api(dataType = None, givenData = None):
    #error_message is stored here to ensure that it can be passed as a parameter in jsonify() correctly.
    error_message = jsonify("Sorry, there was an error. Please check the format of the data you entered and try again.")
    api = pgAPI()
    #Since the <path> url variable won't take the whole url in a direct access call, since it reads parameters in the search results url as purposeful and separate from the url string,
    #the url is taken in pieces and stitched back together here.
    if dataType == "searchLink":
        remainingLink = givenData
        term = request.args.get("query")
        index = request.args.get("start_index")
        if index == None:
            index = 1
        givenData = api.reconstructSearchURL(remainingLink, term, index)
    #This try/except enters the form data into the variables, if the data was entered through the testing page.
    try:
        form_data = request.form
        dataType = form_data["inputTypeRadio"]
        givenData = form_data["givenData"]
    except:
        pass
    #Here, the pgAPI() functions are used, then the data is returned as a Response object with the application/json mimetype using jsonify().
    if dataType == "searchTerm":
        try:
            url = api.createURL(givenData)
            json_arr = api.quickSearch(url)
            return jsonify(json_arr)
        except:
            return error_message
    elif dataType == "searchLink":
        try:
            json_arr = api.quickSearch(givenData)
            return jsonify(json_arr)
        except:
            return error_message
    else:
        try:
            return jsonify(api.accessBook(givenData))
        except:
            return error_message

#Call to run app.
if __name__ == "__main__":
    app.run(debug = True)