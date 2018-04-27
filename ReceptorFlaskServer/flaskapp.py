from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/api/', methods=['POST'])
def findregions():
    js = request.get_json()
    print(js)
    return json.dumps({ 'Date' : '12/03/45', 'Amount' : '12.65' })

