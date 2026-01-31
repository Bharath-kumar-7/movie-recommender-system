import streamlit as st
import pickle
import pandas as pd
import requests

import os
import gdown

if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1ym0NeU0M8vnPMJqHem2gRqZ-Mbl_Zrcz", "similarity.pkl", quiet=False)

if not os.path.exists("movie_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=1IrO8LoNs71PBup3NXoyV1RYHXM-Z7Hyq", "movie_dict.pkl", quiet=False)


def fetch_poster(movie_id):
    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3f6556440913c2186095fa8ffc1cef83&language=en-US')
    data = res.json()
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity =pickle.load(open('similarity.pkl', 'rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to recommend',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movie_names,recommended_movie_posters = recommended(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


