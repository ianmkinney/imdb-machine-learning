from flask import Flask, request
from flask.templating import render_template
import get_movie
import pandas as pd

app = Flask(__name__, template_folder='templates')

movies = pd.read_csv("static/data/homescreen_movies.csv")

@app.route("/")
def home():

    return render_template("homepage.html", movies=movies)

@app.route("/predict/", methods=['post', 'get'])
def predict():
    movie = dict()
    if request.method == 'POST':
        movie['title'] = "Loading..."
        movie['rating'] = "Loading..."
        movie['predicted_rating'] = "Loading..."
        movie['income'] = "Loading..."
        movie['image_url'] = ""
        title = request.form.get('title')
        if(title == ""):
            message="Title field can not be left blank!"
            return render_template("predict_movie.html", message=message)
        movie = get_movie.get_movie_data(title)

    return render_template("predict_movie.html", movie=movie)

@app.route("/visuals")
def visuals():
    return render_template("visualizations.html")



if __name__ == '__main__':
    app.run(threaded=True, port=5000)