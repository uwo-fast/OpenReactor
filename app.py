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

    title1 = "Numbers over time"
    xLabel1 = "Time"
    yLabel1 = "Number"

    data1 = [
        (1, 56),
        (2, 45),
        (3, 47),
        (4, 95),
        (5, 87),
        (6, 81),
        (7, 75)
    ]

    time1 = [row[0] for row in data1]
    values1 = [row[1] for row in data1]

    title2 = "Numbers over time"
    xLabel2 = "Time"
    yLabel2 = "Number"

    data2 = [
        (1, 54),
        (2, 46),
        (3, 48),
        (4, 93),
        (5, 84),
        (6, 87),
        (7, 78)
    ]

    time2 = [row[0] for row in data2]
    values2 = [row[1] for row in data2]

    return render_template("graphs.html", time=time2, values=values2, title=title2)


# About page for project
@app.route("/about")
def about():
    return render_template("about.html")