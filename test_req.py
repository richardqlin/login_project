
import requests
from flask import Flask
app = Flask(__name__)

@app.route('/url')
def get_data():
    return requests.get('https://arcane-tor-21692.herokuapp.com/get').content
'''
import requests,json
payload = {'key1': 'value1', 'key2': 'value2'}
r=requests.get('https://arcane-tor-21692.herokuapp.com/get',params=payload)

print r.url
'''

if __name__ == '__main__':
	app.run(debug=True)