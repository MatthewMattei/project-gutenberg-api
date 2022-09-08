from project_gutenberg_api import pgAPI
from flask import Flask, jsonify, render_template, request

error_message = "Sorry, there was an error. Please check the format of the data you entered and try again."

app = Flask(__name__)

#Note, jsonify encodes some special characters

@app.route('/')
def welcome():
    return render_template("index.html")


@app.route('/api', methods = ['POST', 'GET'])
def api():
    if request.method == "GET":
        return "Error, API accessed directly."
    if request.method == "POST":
        api = pgAPI()
        form_data = request.form
        if form_data["inputTypeRadio"] == "searchTerm":
            try:
                url = api.createURL(form_data["givenData"])
                json_arr = api.quickSearch(url)
                return jsonify(json_arr)
            except:
                return error_message
        elif form_data["inputTypeRadio"] == "searchLink":
            try:
                json_arr = api.quickSearch(form_data["givenData"])
                return jsonify(json_arr)
            except:
                return error_message
        else:
            try:
                return jsonify(api.accessBook(form_data["givenData"]))
            except:
                return error_message

if __name__ == "__main__":
    app.run(debug = True)