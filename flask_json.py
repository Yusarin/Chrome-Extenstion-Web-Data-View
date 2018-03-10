import requests
import json
from flask import request, Flask,render_template,json
from html.parser import HTMLParser
from lxml import etree

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('/chrome-extension/webSEQUEL.html')

# @app.route('/hello')
# def json_parse():
# 	start_url = "https://www.google.com/"
# 	r = requests.get(start_url, auth=('user', 'pass'))
# 	root = etree.fromstring(r.text)
# 	print root
# 	return r.text 


@app.route('/GetandParse', methods = ['POST'])
def GetandParse():
	url = request.form['url']
	query = request.form['query']
	
	if url and query:
		return jsonify({'return_url' : url, 'return_query' : query})
		
	return jsonify({'error' : 'Query is missing or URL fetch failed'})
	
	
if __name__ == '__main__':
	app.run(debug=True)