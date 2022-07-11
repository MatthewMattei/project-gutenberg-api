from project_gutenberg_api import pgAPI
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

@app.route('/')
def test():
    return 'Server Works!'


@app.route('/api', methods = ['POST', 'GET'])
def api():
    if request.method == "GET":
        return "Error, API accessed directly."
    if request.method == "POST":
        api = pgAPI()
        form_data = request.form