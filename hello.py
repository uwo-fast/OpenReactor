# To run this server use
"""bash
export FLASK_APP=hello
flask run
"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html')