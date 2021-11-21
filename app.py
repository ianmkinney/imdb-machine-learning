from flask import Flask
from flask.templating import render_template
import get_movie

app = Flask(__name__)

homepage_movies = "Dune, The Junior Defenders, Tortilla Heaven"
movies_list = homepage_movies.split(", ")
movies = []
for movie in movies_list:
    movies.append(get_movie.get_movie_data(movie))

@app.route("/")
def home():

    return render_template("homepage.html", movies=movies)

@app.route("/mock")
def mock():
    return render_template("mock_prediction.html")

if __name__ == '__main__':
    app.run(threaded=True, port=5000)