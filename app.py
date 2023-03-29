from flask import Flask, render_templates
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
