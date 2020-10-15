from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return "Package Tracker"

@app.route('/new_package')
def new_package():
    return render_template('shipping_request.html')