import streamlit as st

st.title("AI Health & Fitness Planning Agent")

st.write("Enter your information below to generate a simple fitness plan.")

name = st.text_input("Name")

goal = st.selectbox(
    "Primary Goal",
    ["Lose fat", "Build muscle", "Maintain weight"]
)

training_days = st.slider("Training Days Per Week", 1, 7, 4)

diet = st.selectbox(
    "Diet Preference",
    ["No preference", "High protein", "Vegetarian", "Low carb"]
)

if st.button("Generate Plan"):

    st.subheader("Your Fitness Plan")

    st.write("Name:", name)
    st.write("Goal:", goal)
    st.write("Training days:", training_days)

    if training_days <= 3:
        st.write("Suggested workout split: Full Body Training")
    elif training_days == 4:
        st.write("Suggested workout split: Upper / Lower Split")
    else:
        st.write("Suggested workout split: Push / Pull / Legs")

    if goal == "Lose fat":
        st.write("Nutrition: Small calorie deficit with high protein.")
    elif goal == "Build muscle":
        st.write("Nutrition: Slight calorie surplus with high protein.")
    else:
        st.write("Nutrition: Maintain calories and stay consistent.")
