import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

st.set_page_config(
    page_title="Recipe Generator",
    page_icon="🍳",
    layout="centered"
)


def generate_recipe(ingredients, cuisine, diet):
    """
    Generate a recipe using the provided ingredients.
    """

    prompt = f"""
    Generate one good recipe using these ingredients: {', '.join(ingredients)}.

    The recipe must not exceed 100 words.

    Cuisine: {cuisine}
    Diet: {diet}

    Include a recipe name, ingredients, and short cooking instructions.
    Respect the selected dietary preference.
    """

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


st.title("🍳 AI Recipe Generator")
st.write("Enter your ingredients and discover a delicious recipe!")

with st.form("recipe_form"):
    ingredients_input = st.text_input(
        "🥕 Ingredients",
        placeholder="e.g. paneer, onion, tomato, capsicum"
    )

    cuisine = st.selectbox(
        "🌎 Choose Cuisine",
        ["Any", "Indian", "Italian", "Mexican", "Chinese", "Thai"]
    )

    diet = st.selectbox(
        "🥗 Dietary Preference",
        ["Any", "Vegetarian", "Vegan", "NonVegetarian", "Jain"]
    )

    submitted = st.form_submit_button("✨ Generate Recipe")

if submitted:
    if not api_key:
        st.error("GROQ_API_KEY not found. Please check your .env file.")

    elif not ingredients_input.strip():
        st.warning("Please enter at least one ingredient.")

    else:
        ingredients = [
            item.strip()
            for item in ingredients_input.split(",")
            if item.strip()
        ]

        try:
            with st.spinner("👨‍🍳 Creating your recipe..."):
                recipe = generate_recipe(
                    ingredients,
                    cuisine,
                    diet
                )

            st.success("Your recipe is ready!")
            st.subheader("🍽️ Your Recipe")
            st.markdown(recipe)

        except Exception as e:
            st.error(f"Unable to generate recipe: {e}")