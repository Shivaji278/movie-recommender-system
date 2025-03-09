import streamlit as st
import pickle
import pandas as pd
import requests



def fetch_poster (title):
    API_KEY = "1d2682c8"
    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data ["Poster"]

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(title))
    return  recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')
selected_movie_name = st.selectbox('How would you like to be contacted?',movies['title'].values)

if st.button('Recommend'):
     names, posters = recommend (selected_movie_name)
     cols = st.columns(5)
     for col, name, poster in zip(cols, names, posters):
      with col:
         st.text(name)
         st.image(poster)
