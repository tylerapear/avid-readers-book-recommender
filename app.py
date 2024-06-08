import pickle
import streamlit as st
import numpy as np
#import os
#import pkg_resources


st.header("Avid Readers Book Reccomender")

# Get the path to the artifacts directory within the package
#artifacts_dir = pkg_resources.resource_filename(__name__, 'artifacts')

# Paths to the files in the artifacts directory
#model_path = os.path.join(artifacts_dir, 'model.pkl')
#books_name_path = os.path.join(artifacts_dir, 'books_name.pkl')
#final_rating_path = os.path.join(artifacts_dir, 'final_rating.pkl')
#book_pivot_path = os.path.join(artifacts_dir, 'book_pivot.pkl')

model = pickle.load(open('artifacts/model.pkl', 'rb'))
books_name = pickle.load(open('artifacts/books_name.pkl', 'rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl', 'rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl', 'rb'))

#try:
 #   with open(model_path, 'rb') as file:
  #      model = pickle.load(file)
   # with open(books_name_path, 'rb') as file:
   #     books_name = pickle.load(file)
   # with open(final_rating_path, 'rb') as file:
   #     final_rating = pickle.load(file)
   # with open(book_pivot_path, 'rb') as file:
   #     book_pivot = pickle.load(file)

#except Exception as e:
 #   print("An error occured: ", e)
  #  input("Press Enter to exit...")


#Get Paths to Data Visualization Images
authors_img_path = 'artifacts/img/authors.png'
book_popularity_img_path = 'artifacts/img/book_popularity.png'
publishers_img_path = 'artifacts/img/publishers.png'


with open(authors_img_path, 'rb') as f:
    authors_img = f.read()
with open(book_popularity_img_path, 'rb') as f:
    book_popularity_img = f.read()
with open(publishers_img_path, 'rb') as f:
    publishers_img = f.read()

def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            book_list.append(j)

    print(distance)

    return(book_list, distance, poster_url)

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        id = np.where(final_rating['Book-Title'] == name)[0][0]
        ids_index.append(id)

    for idx in ids_index:
        url = final_rating.iloc[idx]['Image-URL-L']
        poster_url.append(url)

    return poster_url


selected_book = st.selectbox(
    "Tell us the name of a book you like:",
    books_name
)

if st.button('Show Recommendation'):
    recommendation_books, distances, poster_url = recommend_books(selected_book)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendation_books[1])
        st.text(f'Distance: {distances[0][1]:.2f}')
        st.image(poster_url[1])

    with col2:
        st.text(recommendation_books[2])
        st.text(f'Distance: {distances[0][2]:.2f}')
        st.image(poster_url[2])

    with col3:
        st.text(recommendation_books[3])
        st.text(f'Distance: {distances[0][3]:.2f}')
        st.image(poster_url[3])

    with col4:
        st.text(recommendation_books[4])
        st.text(f'Distance: {distances[0][4]:.2f}')
        st.image(poster_url[4])

    with col5:
        st.text(recommendation_books[5])
        st.text(f'Distance: {distances[0][5]:.2f}')
        st.image(poster_url[5])

st.header("Understanding Our Data:")

st.image (book_popularity_img, use_column_width=True)
st.image (authors_img, use_column_width=True)
st.image (publishers_img, use_column_width=True)

