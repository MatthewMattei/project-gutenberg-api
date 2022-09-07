from project_gutenberg_api import pgAPI
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

#TODO: determine how to deal with weird characters like hyphen --> \u
#Maybe also get rid of self/pgAPI requirement in function calls?

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
            url = pgAPI.createURL(pgAPI, form_data["givenData"])
            json_arr = pgAPI.quickSearch(pgAPI, url)
            return jsonify(json_arr)
        else:
            return jsonify(pgAPI.accessBook(pgAPI, form_data["givenData"]))

if __name__ == "__main__":
    app.run(debug = True)