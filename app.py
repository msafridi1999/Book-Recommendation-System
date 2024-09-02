import streamlit as st
import pickle
import numpy as np

# Load the pickled data
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

# Streamlit App
st.set_page_config(page_title="Book Recommender System", layout="wide")

# Navbar equivalent
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Recommend"])

if page == "Home":
    st.title("Top 50 Books")
    # Display the top 50 books
    for i in range(len(popular_df)):
        st.image(popular_df['Image-URL-M'].values[i], width=150)
        st.subheader(popular_df['Book-Title'].values[i])
        st.text(f"Author: {popular_df['Book-Author'].values[i]}")
        st.text(f"Votes: {popular_df['num_ratings'].values[i]}")
        st.text(f"Rating: {popular_df['avg_rating'].values[i]}")
        st.write("---")

elif page == "Recommend":
    st.title("Recommend Books")
    user_input = st.text_input("Enter a book name")

    if st.button("Recommend"):
        try:
            index = np.where(pt.index == user_input)[0][0]
            similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

            st.write("Books recommended for you:")
            for i in similar_items:
                temp_df = books[books['Book-Title'] == pt.index[i[0]]]
                book_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
                author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
                image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

                st.image(image, width=150)
                st.subheader(book_title)
                st.text(f"Author: {author}")
                st.write("---")
        except:
            st.error("Book not found. Please try another one.")
