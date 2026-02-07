import streamlit as st
import pickle
import pandas as pd
import requests
import os

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    # params = {
    #     "api_key": "ee055a0fb589bb03d502e6b7430b1929",
    #     "language": "en-US"
    # }
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except:
        return "https://via.placeholder.com/500x750?text=Error"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for idx in movies_list:
        movie_id = movies.iloc[idx[0]].movie_id
        recommended_movies.append(movies.iloc[idx[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Choose a movie to recommend",
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
