import string
from flask import Flask, url_for, jsonify
from datetime import datetime
from marmiton import Marmiton
from urllib import request
import random

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify(status='ok',message='Hi there')

@app.route('/recipes/search<string:keywords>/<int:limit>/<int:offset>')
def recipes(keywords, offset, limit):
	keywords = keywords.replace('-', ' ')
	query_opt = {
		"aqt": keywords
	}
	query_search = Marmiton.search(query_opt)
	final = dict()
	x = 0
	if offset < len(query_search) and offset >= 0:
		x = offset
	if limit > len(query_search) or limit < 0:
		limit = len(query_search)
	while x < limit:
		final[x] = query_search[x]['image']
		x += 1
	return jsonify(final)

@app.route('/recipes/search<string:keywords>/<int:limit>/<int:offset>?download')
def recipes_dl(keywords, offset, limit):
	keywords = keywords.replace('-', ' ')
	query_opt = {
		"aqt": keywords
	}
	query_search = Marmiton.search(query_opt)
	final = dict()
	x = 0
	if offset < len(query_search) and offset >= 0:
		x = offset
	if limit > len(query_search) or limit < 0:
		limit = len(query_search)
	while x < limit:
		final[x] = query_search[x]['image']
		request.urlretrieve(final[x], './test' + str(x) + '.jpg')
		x += 1
	return jsonify(final)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
