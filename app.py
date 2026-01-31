import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# ---------------- BACKGROUND IMAGE ---------------- #
page_bg = """
<style>
.stApp {
background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
background-size: cover;
background-position: center;
background-attachment: fixed;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ---------------- DOWNLOAD FILES ---------------- #
if not os.path.exists("similarity.pkl"):
    gdown.download("https://drive.google.com/uc?id=1ym0NeU0M8vnPMJqHem2gRqZ-Mbl_Zrcz", "similarity.pkl", quiet=False)

if not os.path.exists("movie_dict.pkl"):
    gdown.download("https://drive.google.com/uc?id=1IrO8LoNs71PBup3NXoyV1RYHXM-Z7Hyq", "movie_dict.pkl", quiet=False)

# ---------------- FETCH POSTER ---------------- #
def fetch_poster(movie_id):
    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3f6556440913c2186095fa8ffc1cef83&language=en-US')
    data = res.json()
    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ---------------- FETCH RATING ---------------- #
def fetch_rating(movie_id):
    res = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=3f6556440913c2186095fa8ffc1cef83&language=en-US')
    data = res.json()
    return data.get("vote_average", "N/A")

# ---------------- RECOMMEND FUNCTION ---------------- #
def recommended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_ratings = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_ratings.append(fetch_rating(movie_id))

    return recommended_movies, recommended_movies_posters, recommended_movies_ratings

# ---------------- LOAD DATA ---------------- #
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------- UI ---------------- #
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie to recommend',
    movies['title'].values
)

# ---------------- DISPLAY ---------------- #
if st.button('Recommend'):
    names, posters, ratings = recommended(selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            # FIXED TITLE HEIGHT FOR ALIGNMENT
            st.markdown(
                f"""
                <div style='text-align:center; color:white; height:60px; 
                            display:flex; align-items:center; justify-content:center;'>
                    <h5>{names[idx]}</h5>
                </div>
                """,
                unsafe_allow_html=True
            )

            # POSTER
            st.markdown(
                f"""
                <div style='display:flex; justify-content:center;'>
                    <img src="{posters[idx]}" height="300" 
                         style="border-radius:10px; object-fit:cover;">
                </div>
                """,
                unsafe_allow_html=True
            )

            # RATING
            st.markdown(
                f"""
                <div style='text-align:center; 
                            background-color:rgba(0,0,0,0.7);
                            padding:5px;
                            border-radius:8px;
                            color:gold;
                            font-weight:bold;
                            margin-top:5px;'>
                ⭐ Rating: {ratings[idx]}
                </div>
                """,
                unsafe_allow_html=True
            )
