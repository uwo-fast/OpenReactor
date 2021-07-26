# To run this server use
"""bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
"""

from flask import Flask

app = Flask(__name__)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# About page for project
@app.route('/about')
def about():
    return render_template('about.html')