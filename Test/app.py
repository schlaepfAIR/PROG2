import os
from flask import Flask, render_template, abort, url_for
import json
import html

app = Flask(__name__)

# read file
with open('personal1.json', 'r') as myfile:
    data = myfile.read()

@app.route("/")
def index():
    return render_template('index.html', title="page", jsonfile=json.dumps(data))

if __name__ == '__main__':
    app.run(host='localhost', debug=True)