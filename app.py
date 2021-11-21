from flask import Flask, request
from flask.templating import render_template
import get_movie

app = Flask(__name__, template_folder='templates')

homepage_movies = "Dune, Shang Chi, 13 Minutes"
movies_list = homepage_movies.split(", ")
movies = []
for movie in movies_list:
    movies.append(get_movie.get_movie_data(movie))

@app.route("/")
def home():

    return render_template("homepage.html", movies=movies)

@app.route("/mock/", methods=['post', 'get'])
def mock():
    movie = []
    if request.method == 'POST': 
        title = request.form.get('title')
        movie = get_movie.get_movie_data(title)

    return render_template("mock_prediction.html", movie=movie)



if __name__ == '__main__':
    app.run(threaded=True, port=5000)