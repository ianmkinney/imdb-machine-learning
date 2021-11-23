from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd

def imdb_linear():

    learning_df = pd.read_csv("static/data/learning_sample.csv")

    model = LinearRegression()

    y=learning_df['avg_vote']
    X=learning_df[['year', 'lead_number', 'production_number', 'director_number', 'writer_number', 'budget', 'duration', '0_Action', '0_Adventure', '0_Animation',
        '0_Biography', '0_Comedy', '0_Crime', '0_Drama', '0_Family',
        '0_Fantasy', '0_History', '0_Horror', '0_Music', '0_Musical',
        '0_Mystery', '0_News', '0_Romance', '0_Sci-Fi', '0_Sport', '0_Thriller',
        '0_War', '0_Western']]

    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

    scaler = StandardScaler().fit(X_train)
    X_train_scaled = scaler.transform(X_train)
    X_train_scaled

    model.fit(X_train, y_train)

    print(f'Training Score: {model.score(X_train, y_train)}')
    print(f'Testing Score: {model.score(X_test, y_test)}')

    return model