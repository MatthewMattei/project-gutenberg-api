from project_gutenberg_api import pgAPI
from flask import Flask, jsonify, render_template, request

error_message = "Sorry, there was an error. Please check the format of the data you entered and try again."

app = Flask(__name__)

#Note, jsonify encodes some special characters

@app.route('/')
def welcome():
    return render_template("index.html")


@app.route('/api', methods = ["POST", "GET"])
@app.route("/api/<string:dataType>/<path:givenData>")
def api(dataType = None, givenData = None):
    api = pgAPI()
    if dataType == "searchLink":
        remainingLink = givenData
        term = request.args.get("query")
        index = request.args.get("start_index")
        if index == None:
            index = 1
        givenData = api.reconstructSearchURL(remainingLink, term, index)
    try:
        form_data = request.form
        dataType = form_data["inputTypeRadio"]
        givenData = form_data["givenData"]
    except:
        pass
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

if __name__ == "__main__":
    app.run(debug = True)