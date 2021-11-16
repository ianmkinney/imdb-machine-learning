from flask import Flask
from flask.templating import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/mock")
def mock():
    return render_template("mock_prediction.html")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)