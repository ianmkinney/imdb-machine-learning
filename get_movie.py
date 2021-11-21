import requests
import json
import pandas as pd
import os

actor_data = pd.read_csv("static/data/actors.csv")
director_data = pd.read_csv("static/data/directors.csv")
writer_data = pd.read_csv("static/data/writers.csv")

api_key = os.environ['API_KEY']

headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': api_key
        }


def get_id(search_title): 

    url = "https://imdb8.p.rapidapi.com/auto-complete"

    querystring = {"q":search_title}

    response = requests.request("GET", url, headers=headers, params=querystring)

    response_json = json.loads(response.text)

    data = pd.DataFrame(response_json['d'])
    result = data.head(1)
    return result.id[0]

def add_people(values, imdb_id): 
    url = "https://imdb8.p.rapidapi.com/title/get-full-credits"

    querystring = {"tconst":imdb_id}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)

    values['actor_1'] = response_json['cast'][0]['name']
    values['actor_2'] = response_json['cast'][1]['name']
    values['director'] = response_json['crew']['director'][0]['name']
    values['writer'] = response_json['crew']['writer'][0]['name']

    return values

def add_money(values, imdb_id):

    url = "https://imdb8.p.rapidapi.com/title/get-business"

    querystring = {"tconst":"tt0796366"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)
    budget = response_json['resource']['budget']['amount']
    gross = response_json['resource']['gross']['aggregations'][0]['total']['amount']
    values['budget'] = budget
    values['income'] = gross
    return values


def get_meta_data(query):

    url = "https://imdb8.p.rapidapi.com/title/get-meta-data"

    imdb_id = get_id(query)

    querystring = {"ids":imdb_id,"region":"US"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    response_json = json.loads(response.text)

    values = dict()
    title = response_json[imdb_id]['title']['title']
    values['title'] = title
    image_url = response_json[imdb_id]['title']['image']['url']
    values['image_url'] = image_url
    duration = response_json[imdb_id]['title']['runningTimeInMinutes']
    values['duration'] = duration
    year = response_json[imdb_id]['title']['year']
    values['year'] = year
    rating = response_json[imdb_id]['ratings']['rating']
    values['rating'] = rating
    ratingCount = response_json[imdb_id]['ratings']['ratingCount']
    values['ratingCount'] = ratingCount
    genres = ""
    for genre in response_json[imdb_id]['genres']:
        genres = genres + genre + ", "
    genres = genres.rstrip(", ")
    values['genres'] = genres

    values = add_people(values, imdb_id)
    values = add_money(values, imdb_id)
    return values

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

learning_df = pd.read_csv("data/learning_sample.csv")

model = LinearRegression()

y=learning_df['avg_vote']
X=learning_df[['year', 'lead_number', 'support_number', 'director_number', 'writer_number', 'budget', 'duration', '0_Action', '0_Adventure', '0_Animation',
       '0_Biography', '0_Comedy', '0_Crime', '0_Drama', '0_Family',
       '0_Fantasy', '0_History', '0_Horror', '0_Music', '0_Musical',
       '0_Mystery', '0_News', '0_Romance', '0_Sci-Fi', '0_Sport', '0_Thriller',
       '0_War', '0_Western']]

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_train_scaled

X_test_scaled = scaler.transform(X_test)
X_test_scaled

model.fit(X_train, y_train)

def add_prediction(values):

    # Prepare genre number array
    genre_string = "Action, Adventure, Animation, Biography, Comedy, Crime, Drama, Family, Fantasy, History, Horror, Music, Musical, Mystery, News, Romance, Sci-Fi, Sport, Thriller, War, Western"
    genre_list = genre_string.split(", ")
    value_list = []
    for genre in genre_list: 
        if genre in values['genres']:
            value_list.append(1)
        else:
            value_list.append(0)

    # Extract actor numbers
    actor_1_number = actor_data[actor_data['actor_name'] == values['actor_1']]
    actor_1_number = actor_1_number['actor_number'].values[0]
    actor_2_number = actor_data[actor_data['actor_name'] == values['actor_1']]
    actor_2_number = actor_2_number['actor_number'].values[0]

    # Extract director number
    director_number = director_data[director_data['lead_director'] == values['director']]
    director_number = director_number['director_number'].values[0]

    # Extract Writer Number
    writer_number = writer_data[writer_data['lead_writer'] == values['writer']]
    writer_number = writer_number['writer_number'].values[0]

    movie_x = [[values['year'], actor_1_number, actor_2_number, director_number, writer_number, values['budget'], values['duration'], 
    value_list[0], value_list[1], value_list[2], value_list[3], value_list[4], value_list[5], value_list[6], value_list[7], value_list[8],
    value_list[9], value_list[10], value_list[11], value_list[12], value_list[13], value_list[14], value_list[15], value_list[16], value_list[17], 
    value_list[18], value_list[19], value_list[20]]]

    values['predicted_rating'] = model.predict(movie_x)[0].round(1)

    return values
