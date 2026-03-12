import streamlit as st

st.set_page_config(
    page_title="AI Health & Fitness Planning Agent",
    page_icon="🏋️",
    layout="centered"
)

st.title("AI Health & Fitness Planning Agent")
st.write(
    "Fill out the information below to receive a basic workout and calorie recommendation."
)

st.markdown("---")

def calculate_bmr(weight_lbs, height_ft, height_in, age, sex):
    weight_kg = weight_lbs * 0.453592
    total_inches = (height_ft * 12) + height_in
    height_cm = total_inches * 2.54

    if sex == "Male":
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

    return bmr

def activity_multiplier(activity_level):
    multipliers = {
        "Sedentary (little or no exercise)": 1.2,
        "Lightly active (1-3 days/week)": 1.375,
        "Moderately active (3-5 days/week)": 1.55,
        "Very active (6-7 days/week)": 1.725,
        "Extremely active (hard exercise + physical job)": 1.9
    }
    return multipliers[activity_level]

def workout_split(training_days):
    if training_days <= 2:
        return "Full Body Split"
    elif training_days == 3:
        return "Upper / Lower / Full Body Split"
    elif training_days == 4:
        return "Upper / Lower Split"
    elif training_days == 5:
        return "Push / Pull / Legs + Upper / Lower"
    else:
        return "Push / Pull / Legs Split"

with st.form("fitness_form"):
    st.subheader("Personal Information")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=13, max_value=80, value=21, step=1)
    sex = st.selectbox("Sex", ["Male", "Female"])

    st.subheader("Body Information")
    weight_lbs = st.number_input("Weight (lbs)", min_value=80.0, max_value=500.0, value=180.0, step=1.0)
    col1, col2 = st.columns(2)
    with col1:
        height_ft = st.number_input("Height - Feet", min_value=3, max_value=8, value=6, step=1)
    with col2:
        height_in = st.number_input("Height - Inches", min_value=0, max_value=11, value=0, step=1)

    st.subheader("Goals and Activity")
    goal = st.selectbox(
        "Primary Goal",
        ["Lose fat", "Build muscle", "Maintain weight", "Improve general fitness"]
    )
    activity_level = st.selectbox(
        "Daily Activity Level",
        [
            "Sedentary (little or no exercise)",
            "Lightly active (1-3 days/week)",
            "Moderately active (3-5 days/week)",
            "Very active (6-7 days/week)",
            "Extremely active (hard exercise + physical job)"
        ]
    )
    training_days = st.slider("Training Days Per Week", 1, 7, 4)
    workout_time = st.selectbox(
        "Time Available Per Workout",
        ["20-30 minutes", "30-45 minutes", "45-60 minutes", "60+ minutes"]
    )

    st.subheader("Preferences")
    equipment = st.selectbox(
        "Equipment Access",
        ["Full gym", "Home gym", "Dumbbells only", "Bodyweight only"]
    )
    diet = st.selectbox(
        "Diet Preference",
        ["No preference", "High protein", "Vegetarian", "Low carb", "Budget-friendly"]
    )

    st.subheader("Limitations")
    injuries = st.text_area("Injuries / Limitations", placeholder="Optional")
    notes = st.text_area("Anything else we should know?", placeholder="Optional")

    submitted = st.form_submit_button("Generate Plan")

if submitted:
    bmr = calculate_bmr(weight_lbs, height_ft, height_in, age, sex)
    tdee = bmr * activity_multiplier(activity_level)

    if goal == "Lose fat":
        target_calories = tdee - 500
        calorie_note = "A moderate deficit was applied for fat loss."
    elif goal == "Build muscle":
        target_calories = tdee + 250
        calorie_note = "A small surplus was applied for muscle gain."
    elif goal == "Maintain weight":
        target_calories = tdee
        calorie_note = "Maintenance calories were used."
    else:
        target_calories = tdee
        calorie_note = "Maintenance calories were used as a starting point."

    protein_low = weight_lbs * 0.7
    protein_high = weight_lbs * 1.0

    st.markdown("---")
    st.subheader("Your Personalized Results")

    if name.strip():
        st.write(f"**Name:** {name}")

    st.write(f"**Goal:** {goal}")
    st.write(f"**Suggested Workout Split:** {workout_split(training_days)}")
    st.write(f"**Workout Time:** {workout_time}")
    st.write(f"**Equipment Access:** {equipment}")

    st.markdown("### Calorie Estimates")
    st.write(f"**Estimated BMR:** {round(bmr)} calories/day")
    st.write(f"**Estimated Maintenance Calories (TDEE):** {round(tdee)} calories/day")
    st.write(f"**Suggested Daily Calories for Your Goal:** {round(target_calories)} calories/day")
    st.caption(calorie_note)

    st.markdown("### Protein Recommendation")
    st.write(f"Suggested protein intake: **{round(protein_low)}–{round(protein_high)} grams/day**")

    st.markdown("### Training Recommendation")
    if training_days <= 3:
        st.write("Focus on full-body training with compound movements and steady progression.")
    elif training_days == 4:
        st.write("An upper/lower split is a strong option for balancing frequency and recovery.")
    else:
        st.write("A higher-frequency split can work well if recovery, sleep, and consistency are solid.")

    st.markdown("### Nutrition Guidance")
    if diet == "High protein":
        st.write("Build each meal around a lean protein source and distribute protein evenly through the day.")
    elif diet == "Vegetarian":
        st.write("Use foods like Greek yogurt, eggs, tofu, tempeh, beans, lentils, and protein shakes.")
    elif diet == "Low carb":
        st.write("Keep carbs lower and prioritize protein, vegetables, and healthy fats.")
    elif diet == "Budget-friendly":
        st.write("Focus on lower-cost staples like rice, oats, potatoes, eggs, frozen vegetables, tuna, and chicken.")
    else:
        st.write("Choose mostly whole foods that match your calorie target and that you can stay consistent with.")

    st.markdown("### Recovery / Safety")
    if injuries.strip():
        st.warning(f"Use caution and modify exercises around these limitations: {injuries}")
    else:
        st.success("No injuries or limitations were entered.")

    if notes.strip():
        st.markdown("### Additional Notes")
        st.write(notes)

    st.markdown("---")
    st.info("This tool provides general wellness guidance only and is not medical advice.")
