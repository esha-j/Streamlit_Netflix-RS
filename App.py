# pip install streamlit
# pip install scikit-learn

#Dataset - https://www.kaggle.com/datasets/shivamb/netflix-shows



import numpy as np
import pandas as pd
import streamlit as sl
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


netflix = pd.read_csv('netflix_titles.csv')
netflix_data = netflix.copy()
df = netflix


netflix_tfid = TfidfVectorizer(stop_words='english')
netflix_data['description'] = netflix_data['description'].fillna('')
netflix_tfidf_matrix = netflix_tfid .fit_transform(netflix_data['description'])

cosine_sim = linear_kernel(netflix_tfidf_matrix, netflix_tfidf_matrix)

indices = pd.Series(netflix_data.index, index=netflix_data['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return netflix_data[['title','description']].iloc[movie_indices]

movie_list = netflix_data['title'].values



sl.title("InsMovie")
sl.markdown("Quick and easy way to decide on which movie to watch")

with sl.sidebar:
    choose = option_menu("MENU", ["Home","Recommend","Contact"],
                         icons=['house','funnel-fill','person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "black"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#02ab21"},
    }
    )
#img = Image.open('') sl.image(img)

if choose == "Home":
    col1, col2 = sl.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        sl.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Helvetica'; color: Grey;}
         </style> """, unsafe_allow_html=True)
        sl.markdown('<p class="font">Objective</p>', unsafe_allow_html=True)    
        sl.write("In moments of confusion, this app will aid you in deciding which Movie/TV Show to watch.")
        sl.write("The app recommends a show based on a previous show you have watched. Using cosine similarity function, the genre, cast and various other factors are considered and movies similar to the given movie are displayed.")
        sl.markdown('<p class="font">Cosine Similarity Function</p>', unsafe_allow_html=True)
        sl.code("similarity(A,B) = cos θ = (A.B)/(||A||||B||)")
        sl.write("Cosine similarity is beneficial for applications that utilize sparse data, such as word documents, transactions in market data, and recommendation systems because cosine similarity ignores 0-0 matches. Counting 0-0 matches in sparse data would inflate similarity scores. ")

    with col2:   
        sl.subheader('Python Libraries')         
        sl.write("1. Numpy")
        sl.write("2. Pandas")
        sl.write("3. Streamlit")
        sl.write("4. Scikit-Learn")


if choose == "Recommend":
    col1, col2 = sl.columns( [0.9, 0.1])
    with col1:               # To display the header text using css style
        sl.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Helvetica'; color: Grey;} 
        </style> """, unsafe_allow_html=True)
        selected_movie = sl.selectbox( "Type or Select your movie ", movie_list )
        if sl.button('Recommend'):
            recommended_movie_names = get_recommendations(selected_movie)
            recommended_movie_names



if choose == "Contact":
    sl.markdown(""" <style> .font {
    font-size:35px ; font-family: 'Helvetica'; color: Grey;} 
    </style> """, unsafe_allow_html=True)
    sl.markdown('<p class="font">Contact Us</p>', unsafe_allow_html=True)    
    
    with sl.form("form1",clear_on_submit=True):
        name    = sl.text_input("Name: ")
        email   = sl.text_input("Email: ")
        message = sl.text_area("Message: ")

        submit  = sl.form_submit_button("Submit")


