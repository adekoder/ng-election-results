from flask import Flask, render_template, jsonify
from scraper import result_scrapper
from scraper import get_results_data


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bot-fetch-results')
def bot_fetch_results():
    result_scrapper()
    return jsonify(status=True),200

@app.route('/results')
def get_results():
    return jsonify(
        status=True,
        data=get_results_data()
    ), 200


