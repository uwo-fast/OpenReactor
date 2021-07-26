# To run this server use
"""bash
export FLASK_APP=hello
flask run
"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"