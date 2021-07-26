# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""

from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Graphs page
@app.route("/graphs")
def graphs():

    title = "Numbers over time"
    xLabel = "Time"
    yLabel = "Number"

    data = [
        (1, 56),
        (2, 45),
        (3, 47),
        (4, 95),
        (5, 87),
        (6, 81),
        (7, 75)
    ]

    time = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template("graphs.html", time=time, values=values, title=title)


# About page for project
@app.route("/about")
def about():
    return render_template("about.html")