from flask import Flask, request
from flask.templating import render_template
import get_movie

app = Flask(__name__, template_folder='templates')

homepage_movies = "Dune, Shang Chi, 13 Minutes, tick,tick...BOOM, Home sweet alone, Free Guy"
movies_list = homepage_movies.split(", ")
movies = []
for movie in movies_list:
    movies.append(get_movie.get_movie_data(movie))

@app.route("/")
def home():

    return render_template("homepage.html", movies=movies)

@app.route("/mock/", methods=['post', 'get'])
def mock():
    movie = dict()
    if request.method == 'POST':
        movie['title'] = "Loading..."
        movie['rating'] = "Loading..."
        movie['predicted_rating'] = "Loading..."
        movie['image_url'] = ""
        title = request.form.get('title')
        movie = get_movie.get_movie_data(title)

    return render_template("mock_prediction.html", movie=movie)

@app.route("/visuals")
def visuals():
    return render_template("visualizations.html")



if __name__ == '__main__':
    app.run(threaded=True, port=5000)