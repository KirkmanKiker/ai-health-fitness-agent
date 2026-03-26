import streamlit as st
from dataclasses import dataclass

st.set_page_config(
    page_title="AI Health & Fitness Planning Agent",
    page_icon="🏋️",
    layout="centered"
)

st.title("AI Health & Fitness Planning Agent")
st.write(
    "Fill out the information below to receive a basic workout and calorie recommendation."
)
st.caption("This version now uses a multi-agent workflow for Milestone II.")

st.markdown("---")


# -----------------------------
# Original helper logic kept
# -----------------------------
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


# -----------------------------
# Multi-agent workflow classes
# -----------------------------
@dataclass
class UserProfile:
    name: str
    age: int
    sex: str
    weight_lbs: float
    height_ft: int
    height_in: int
    goal: str
    activity_level: str
    training_days: int
    workout_time: str
    equipment: str
    diet: str
    injuries: str
    notes: str


class PlannerAgent:
    """
    Agent 1:
    Takes user input and turns it into a structured plan for what the system should do.
    """

    def run(self, profile: UserProfile):
        tasks = [
            "calculate_bmr",
            "calculate_tdee",
            "set_calorie_target",
            "set_protein_target",
            "choose_workout_split",
            "generate_training_guidance",
            "generate_nutrition_guidance",
            "perform_safety_check"
        ]

        risk_flags = []
        if profile.injuries.strip():
            risk_flags.append("injury_or_limitation_present")
        if profile.training_days >= 6:
            risk_flags.append("high_training_frequency")
        if profile.age < 16:
            risk_flags.append("younger_user")

        return {
            "agent": "PlannerAgent",
            "status": "completed",
            "tasks": tasks,
            "risk_flags": risk_flags,
            "input_summary": {
                "goal": profile.goal,
                "activity_level": profile.activity_level,
                "training_days": profile.training_days,
                "diet": profile.diet,
                "equipment": profile.equipment
            }
        }


class AnalysisAgent:
    """
    Agent 2:
    Performs the actual calculations and generates the fitness recommendations.
    """

    def run(self, profile: UserProfile, plan: dict):
        bmr = calculate_bmr(
            profile.weight_lbs,
            profile.height_ft,
            profile.height_in,
            profile.age,
            profile.sex
        )

        tdee = bmr * activity_multiplier(profile.activity_level)

        if profile.goal == "Lose fat":
            target_calories = tdee - 500
            calorie_note = "A moderate deficit was applied for fat loss."
        elif profile.goal == "Build muscle":
            target_calories = tdee + 250
            calorie_note = "A small surplus was applied for muscle gain."
        elif profile.goal == "Maintain weight":
            target_calories = tdee
            calorie_note = "Maintenance calories were used."
        else:
            target_calories = tdee
            calorie_note = "Maintenance calories were used as a starting point."

        protein_low = profile.weight_lbs * 0.7
        protein_high = profile.weight_lbs * 1.0

        # Training guidance
        if profile.training_days <= 3:
            training_guidance = (
                "Focus on full-body training with compound movements and steady progression."
            )
        elif profile.training_days == 4:
            training_guidance = (
                "An upper/lower split is a strong option for balancing frequency and recovery."
            )
        else:
            training_guidance = (
                "A higher-frequency split can work well if recovery, sleep, and consistency are solid."
            )

        # Added a workout-time note so the analysis agent feels more distinct
        if profile.workout_time == "20-30 minutes":
            training_guidance += " Keep sessions short and centered around the most important lifts."
        elif profile.workout_time == "30-45 minutes":
            training_guidance += " This gives enough time for main lifts plus a small amount of accessory work."
        elif profile.workout_time == "45-60 minutes":
            training_guidance += " This is a good range for a balanced workout."
        else:
            training_guidance += " Be careful not to add extra volume that hurts recovery."

        # Nutrition guidance
        if profile.diet == "High protein":
            nutrition_guidance = (
                "Build each meal around a lean protein source and distribute protein evenly through the day."
            )
        elif profile.diet == "Vegetarian":
            nutrition_guidance = (
                "Use foods like Greek yogurt, eggs, tofu, tempeh, beans, lentils, and protein shakes."
            )
        elif profile.diet == "Low carb":
            nutrition_guidance = (
                "Keep carbs lower and prioritize protein, vegetables, and healthy fats."
            )
        elif profile.diet == "Budget-friendly":
            nutrition_guidance = (
                "Focus on lower-cost staples like rice, oats, potatoes, eggs, frozen vegetables, tuna, and chicken."
            )
        else:
            nutrition_guidance = (
                "Choose mostly whole foods that match your calorie target and that you can stay consistent with."
            )

        return {
            "agent": "AnalysisAgent",
            "status": "completed",
            "bmr": round(bmr),
            "tdee": round(tdee),
            "target_calories": round(target_calories),
            "calorie_note": calorie_note,
            "protein_low": round(protein_low),
            "protein_high": round(protein_high),
            "workout_split": workout_split(profile.training_days),
            "training_guidance": training_guidance,
            "nutrition_guidance": nutrition_guidance
        }


class VerifierAgent:
    """
    Agent 3:
    Reviews the analysis output, checks for basic issues, and adds warnings or a final summary.
    """

    def run(self, profile: UserProfile, plan: dict, analysis: dict):
        warnings = []

        if analysis["target_calories"] < 1200:
            warnings.append(
                "Suggested calories were very low, so this result should be treated cautiously."
            )

        if "injury_or_limitation_present" in plan["risk_flags"]:
            warnings.append(
                "Exercises should be modified around the injury or limitation entered."
            )

        if "high_training_frequency" in plan["risk_flags"]:
            warnings.append(
                "High weekly training frequency means recovery and sleep need close attention."
            )

        final_summary = (
            f"Your estimated BMR is {analysis['bmr']} calories/day and your estimated maintenance "
            f"calories are {analysis['tdee']} calories/day. Based on your goal of {profile.goal.lower()}, "
            f"a starting calorie target of {analysis['target_calories']} calories/day is recommended. "
            f"A good protein target is about {analysis['protein_low']} to {analysis['protein_high']} grams per day."
        )

        return {
            "agent": "VerifierAgent",
            "status": "completed",
            "warnings": warnings,
            "final_summary": final_summary
        }


class ControllerAgent:
    """
    Controller/orchestrator for the fixed pipeline:
    Planner -> Analysis -> Verifier
    """

    def __init__(self):
        self.planner = PlannerAgent()
        self.analyzer = AnalysisAgent()
        self.verifier = VerifierAgent()

    def run(self, profile: UserProfile):
        plan = self.planner.run(profile)
        analysis = self.analyzer.run(profile, plan)
        verification = self.verifier.run(profile, plan, analysis)

        return {
            "plan": plan,
            "analysis": analysis,
            "verification": verification
        }


# -----------------------------
# Your original Streamlit form
# -----------------------------
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


# -----------------------------
# Multi-agent execution
# -----------------------------
if submitted:
    profile = UserProfile(
        name=name,
        age=int(age),
        sex=sex,
        weight_lbs=float(weight_lbs),
        height_ft=int(height_ft),
        height_in=int(height_in),
        goal=goal,
        activity_level=activity_level,
        training_days=int(training_days),
        workout_time=workout_time,
        equipment=equipment,
        diet=diet,
        injuries=injuries,
        notes=notes
    )

    controller = ControllerAgent()
    result = controller.run(profile)

    plan = result["plan"]
    analysis = result["analysis"]
    verification = result["verification"]

    st.markdown("---")
    st.subheader("Your Personalized Results")

    if name.strip():
        st.write(f"**Name:** {name}")

    st.write(f"**Goal:** {goal}")
    st.write(f"**Suggested Workout Split:** {analysis['workout_split']}")
    st.write(f"**Workout Time:** {workout_time}")
    st.write(f"**Equipment Access:** {equipment}")

    st.markdown("### Calorie Estimates")
    st.write(f"**Estimated BMR:** {analysis['bmr']} calories/day")
    st.write(f"**Estimated Maintenance Calories (TDEE):** {analysis['tdee']} calories/day")
    st.write(f"**Suggested Daily Calories for Your Goal:** {analysis['target_calories']} calories/day")
    st.caption(analysis["calorie_note"])

    st.markdown("### Protein Recommendation")
    st.write(f"Suggested protein intake: **{analysis['protein_low']}–{analysis['protein_high']} grams/day**")

    st.markdown("### Training Recommendation")
    st.write(analysis["training_guidance"])

    st.markdown("### Nutrition Guidance")
    st.write(analysis["nutrition_guidance"])

    st.markdown("### Recovery / Safety")
    if verification["warnings"]:
        for warning in verification["warnings"]:
            st.warning(warning)
    else:
        st.success("No injuries or major safety flags were detected.")

    if notes.strip():
        st.markdown("### Additional Notes")
        st.write(notes)

    st.markdown("### Final Summary")
    st.info(verification["final_summary"])

    with st.expander("Show Multi-Agent Workflow Details"):
        st.markdown("**Planner Agent Output**")
        st.json(plan)

        st.markdown("**Analysis Agent Output**")
        st.json(analysis)

        st.markdown("**Verifier Agent Output**")
        st.json(verification)

    st.markdown("---")
    st.info("This tool provides general wellness guidance only and is not medical advice.")
