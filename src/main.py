from flask import Flask, render_template
from lc3 import LC
import jinja2

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('index.html')


app.run(host = '0.0.0.0', port = 80)


    
