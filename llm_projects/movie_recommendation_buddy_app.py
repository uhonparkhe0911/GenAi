import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.title("🎬 Movie Recommender")
st.write("Tell me what kind of movies you like, and I'll recommend some!")

user_input = st.text_input("What kind of movies do you enjoy?")

if st.button("Recommend Movies"):
    if user_input:
        with st.spinner("Finding movies for you..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a movie recommendation expert. Recommend 5 movies based on the user's preferences. Give each movie's title, release year, genre, and a short explanation of why they might enjoy it."
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=0.7
            )

            st.subheader("🍿 Your Movie Recommendations")
            st.write(response.choices[0].message.content)
    else:
        st.warning("Please describe your movie preferences!")