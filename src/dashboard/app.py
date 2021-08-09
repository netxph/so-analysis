from flask import Flask, render_template
from api import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')