import string
import flask
from flask import Flask, url_for, jsonify
from datetime import datetime
from marmiton import Marmiton
from urllib import request, parse
import zipfile

app = Flask(__name__)

@app.route('/')
def index():
	return jsonify(status='ok',message='Hi there')

@app.route('/recipes/search<string:keywords>/<int:limit>/<int:offset>', methods=['post', 'get'])
def recipes_dl(keywords, offset, limit, dl=None):
	keywords = keywords.replace('-', ' ')
	query_opt = {
		"aqt": keywords
	}
	dl = True if (flask.request.args.get('download') == '') else False
	query_search = Marmiton.search(query_opt)
	final = dict()
	x = 0
	if offset < len(query_search) and offset >= 0:
		x = offset
	if limit > len(query_search) or limit <= 0:
		limit = len(query_search)
	if (dl == True):
		z = zipfile.ZipFile('./Flask-archives.zip', 'w')
	while x < limit:
		final[x] = query_search[x]['image']
		name = '/tmp/recipe' + str(x) + '.jpg'
		if (dl == True):
			request.urlretrieve(final[x], name)
			z.write(name)
		x += 1
	if (dl == True):
		z.close()
	return jsonify(final)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
