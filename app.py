import streamlit as st
from dataclasses import dataclass
import random

# -------------------------------------------------
# Page setup
# -------------------------------------------------
st.set_page_config(
    page_title="AI Health & Fitness Planning Agent",
    page_icon="🏋️",
    layout="wide"
)

# -------------------------------------------------
# Custom UI styling
# -------------------------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f8fbff;
        color: #111827;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4, h5, h6, p, label {
        color: #111827 !important;
    }

    .hero-box {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #60a5fa 100%);
        padding: 2rem;
        border-radius: 24px;
        color: white;
        margin-bottom: 1.25rem;
        box-shadow: 0 10px 28px rgba(0,0,0,0.14);
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: white !important;
        margin-bottom: 0.4rem;
    }

    .hero-sub {
        font-size: 1rem;
        line-height: 1.6;
        color: #e5efff !important;
    }

    .hero-joke {
        margin-top: 0.9rem;
        font-size: 0.95rem;
        color: #dbeafe !important;
        font-style: italic;
    }

    .section-card {
        background: white;
        border: 1px solid #dbeafe;
        border-left: 6px solid #2563eb;
        border-radius: 20px;
        padding: 1.2rem 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.08);
    }

    .soft-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 0.85rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }

    .pill {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8 !important;
        border: 1px solid #bfdbfe;
        border-radius: 999px;
        padding: 0.38rem 0.78rem;
        font-size: 0.88rem;
        font-weight: 600;
        margin-right: 0.45rem;
        margin-bottom: 0.45rem;
    }

    .workout-day {
        background: #f8fbff;
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    .workout-day-title {
        font-size: 1.08rem;
        font-weight: 800;
        color: #1d4ed8 !important;
        margin-bottom: 0.75rem;
    }

    .exercise-item {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.7rem 0.9rem;
        margin-bottom: 0.5rem;
        color: #111827 !important;
    }

    .summary-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        color: white;
        border-radius: 20px;
        padding: 1.2rem;
        margin-top: 0.75rem;
        box-shadow: 0 8px 22px rgba(0,0,0,0.12);
    }

    .summary-box * {
        color: white !important;
    }

    .footer-note {
        text-align: center;
        color: #4b5563 !important;
        font-size: 0.92rem;
        margin-top: 1.25rem;
    }

    .result-intro {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e3a8a !important;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #dbeafe;
        border-radius: 18px;
        padding: 0.9rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.07);
    }

    div[data-testid="stMetricLabel"] {
        color: #374151 !important;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-weight: 800;
    }

    .stButton > button, .stFormSubmitButton > button {
        background: linear-gradient(135deg, #1d4ed8 0%, #3b82f6 100%);
        color: white;
        font-weight: 700;
        border: none;
        border-radius: 14px;
        padding: 0.75rem 1.2rem;
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.18);
    }

    .stTextInput input, .stNumberInput input, textarea {
        border-radius: 12px !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Friendly helper text
# -------------------------------------------------
def get_fun_greeting():
    greetings = [
        "Hi, welcome back.",
        "Hi, ready to build your plan?",
        "Hi, let’s put together something solid for you.",
        "Hi, let’s make fitness planning a little easier today."
    ]
    return random.choice(greetings)


def get_fun_joke():
    jokes = [
        "I promise this plan is more organized than most notes app workouts.",
        "No random Monday chest day chaos here.",
        "Built with less guessing and fewer chicken and broccoli stereotypes.",
        "Think of this as your gym buddy, just without stealing your bench.",
        "This app will not tell you to max out every day, so we are already ahead."
    ]
    return random.choice(jokes)


def get_goal_motivation(goal):
    if goal == "Lose fat":
        return "Small consistent wins matter more than trying to be perfect."
    elif goal == "Build muscle":
        return "Eat, recover, train hard, repeat. Boring works."
    elif goal == "Maintain weight":
        return "Consistency is the whole game when the goal is maintenance."
    return "A balanced plan you can actually stick to usually beats an extreme one."


def get_results_intro(name, goal):
    person = name.strip() if name.strip() else "there"

    intros = {
        "Lose fat": f"Nice, {person}. Here’s a plan focused on keeping things efficient while supporting fat loss.",
        "Build muscle": f"Nice, {person}. Here’s a plan focused on training quality, recovery, and muscle gain.",
        "Maintain weight": f"Nice, {person}. Here’s a balanced plan to help you stay consistent and maintain progress.",
        "Improve general fitness": f"Nice, {person}. Here’s a balanced plan to help improve overall fitness without overcomplicating it."
    }
    return intros.get(goal, f"Nice, {person}. Here’s your personalized plan.")


# -------------------------------------------------
# Helpers
# -------------------------------------------------
def calculate_bmr(weight_lbs, height_ft, height_in, age, sex):
    weight_kg = weight_lbs * 0.453592
    total_inches = (height_ft * 12) + height_in
    height_cm = total_inches * 2.54

    if sex == "Male":
        return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
    return (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161


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
    return "Push / Pull / Legs Split"


def get_time_adjustment(workout_time):
    if workout_time == "20-30 minutes":
        return 4
    elif workout_time == "30-45 minutes":
        return 5
    elif workout_time == "45-60 minutes":
        return 6
    return 7


def adjust_sets_by_experience(exercise_line, experience_level):
    if experience_level == "Beginner":
        return exercise_line.replace("4 x", "3 x").replace("3 x", "2 x")
    elif experience_level == "Advanced":
        if "2 x" in exercise_line:
            return exercise_line.replace("2 x", "3 x")
        elif "3 x" in exercise_line:
            return exercise_line.replace("3 x", "4 x")
    return exercise_line


def detect_injury_keywords(injuries_text):
    text = injuries_text.lower().strip()
    found = []

    keyword_map = {
        "shoulder": ["shoulder", "rotator cuff", "impingement"],
        "knee": ["knee", "acl", "meniscus", "patellar"],
        "back": ["back", "lower back", "upper back", "spine", "disc"],
        "elbow": ["elbow", "tennis elbow", "golfer's elbow"],
        "wrist": ["wrist", "carpal"],
        "ankle": ["ankle", "achilles", "foot"]
    }

    for injury_type, keywords in keyword_map.items():
        for keyword in keywords:
            if keyword in text:
                found.append(injury_type)
                break

    return found


def get_injury_guidance(injury_keywords):
    guidance = []
    avoid = []
    substitutes = []

    if "shoulder" in injury_keywords:
        guidance.append("Shoulder issue detected. Reduce or avoid painful overhead pressing and aggressive ranges of motion.")
        avoid.extend(["Heavy overhead press", "Deep dips", "Upright rows if painful"])
        substitutes.extend(["Neutral grip dumbbell press", "Machine chest press", "Cable fly", "Controlled lateral raises"])

    if "knee" in injury_keywords:
        guidance.append("Knee issue detected. Reduce deep painful knee flexion under heavy load.")
        avoid.extend(["Painful deep squats", "Jumping drills if painful", "Explosive lunges if painful"])
        substitutes.extend(["Box squats", "Leg press with controlled range", "Glute bridges", "Hamstring curls"])

    if "back" in injury_keywords:
        guidance.append("Back issue detected. Be careful with heavy spinal loading and prioritize bracing.")
        avoid.extend(["Heavy conventional deadlifts", "Loose form barbell rows", "Excessive spinal loading"])
        substitutes.extend(["Chest supported rows", "Machine rows", "Goblet squats", "Hip thrusts"])

    if "elbow" in injury_keywords:
        guidance.append("Elbow issue detected. Limit irritating tricep and curl variations when needed.")
        avoid.extend(["Very heavy skull crushers", "Straight bar curls if painful"])
        substitutes.extend(["Rope pushdowns", "Hammer curls", "Machine curls"])

    if "wrist" in injury_keywords:
        guidance.append("Wrist issue detected. Use neutral grip movements and avoid painful wrist angles.")
        avoid.extend(["Straight bar pressing if painful", "Exercises forcing wrist extension"])
        substitutes.extend(["Dumbbell pressing", "Neutral grip rows", "Cable handles"])

    if "ankle" in injury_keywords:
        guidance.append("Ankle or foot issue detected. Limit jumping and unstable lower body work if painful.")
        avoid.extend(["Jumping drills", "High impact cardio if painful"])
        substitutes.extend(["Bike", "Leg press", "Seated hamstring curls", "Stable split stance work"])

    if not guidance:
        guidance.append("No major injury keywords were detected. Train with good form, gradual progression, and proper recovery.")

    return {"guidance": guidance, "avoid": avoid, "substitutes": substitutes}


def filter_exercises_for_injuries(exercises, injury_keywords):
    filtered = []

    for ex in exercises:
        name_lower = ex.lower()

        if "shoulder" in injury_keywords and ("overhead" in name_lower or "upright row" in name_lower or "dip" in name_lower):
            continue
        if "knee" in injury_keywords and ("jump" in name_lower):
            continue
        if "back" in injury_keywords and ("deadlift" in name_lower or "barbell row" in name_lower):
            continue

        filtered.append(ex)

    return filtered


def goal_focus_text(goal):
    if goal == "Lose fat":
        return "This plan focuses on maintaining muscle, keeping training efficient, and supporting a calorie deficit."
    elif goal == "Build muscle":
        return "This plan focuses on hypertrophy, quality training volume, and progressive overload."
    elif goal == "Maintain weight":
        return "This plan focuses on balanced training, strength maintenance, and consistency."
    return "This plan focuses on balanced fitness, movement quality, and general health."


def get_cardio_plan(goal, activity_level, cardio_preference):
    if goal == "Lose fat":
        base = "Aim for 3 to 5 cardio sessions per week for 20 to 30 minutes."
    elif goal == "Build muscle":
        base = "Aim for 2 to 3 light cardio sessions per week for 15 to 20 minutes."
    elif goal == "Maintain weight":
        base = "Aim for 2 to 4 cardio sessions per week for 20 to 25 minutes."
    else:
        base = "Aim for 3 cardio sessions per week for 20 to 30 minutes."

    if cardio_preference == "Walking":
        mode = "Best option: brisk walking or incline treadmill."
    elif cardio_preference == "Bike":
        mode = "Best option: stationary bike or outdoor cycling."
    elif cardio_preference == "Running":
        mode = "Best option: easy to moderate running."
    elif cardio_preference == "Other":
        mode = "Best option: choose a comfortable form of cardio you can stick with."
    else:
        mode = "Best option: walking, bike, treadmill, or another low stress cardio option."

    extra = "Start on the lower end and build up gradually." if activity_level == "Sedentary (little or no exercise)" else "Keep the intensity moderate so it supports recovery."
    return f"{base} {mode} {extra}"


def get_meal_guidance(diet, protein_low, protein_high, target_calories):
    avg_protein = round((protein_low + protein_high) / 2)

    if target_calories < 1800:
        meal_structure = "3 meals and 1 snack"
    elif target_calories < 2500:
        meal_structure = "3 to 4 meals per day"
    else:
        meal_structure = "4 meals and 1 to 2 snacks"

    if diet == "High protein":
        foods = "chicken breast, Greek yogurt, eggs, tuna, lean beef, protein shakes"
    elif diet == "Vegetarian":
        foods = "Greek yogurt, eggs, tofu, tempeh, beans, lentils, protein shakes"
    elif diet == "Low carb":
        foods = "lean meats, eggs, Greek yogurt, vegetables, avocado, and nuts in moderation"
    elif diet == "Budget-friendly":
        foods = "rice, oats, potatoes, eggs, chicken, canned tuna, and frozen vegetables"
    else:
        foods = "lean proteins, fruit, vegetables, potatoes, rice, oats, dairy, and healthy fats"

    return {
        "meals_per_day": meal_structure,
        "protein_target": f"Aim for about {avg_protein} grams of protein per day.",
        "food_examples": f"Good food options include {foods}."
    }


def get_recovery_guidance(training_days, goal):
    tips = [
        "Aim for about 7 to 9 hours of sleep per night.",
        "Stay hydrated consistently throughout the day.",
        "Take at least 1 to 2 lighter or rest days each week depending on fatigue."
    ]

    if training_days >= 5:
        tips.append("Because training frequency is higher, watch soreness, sleep, and motivation closely.")
    else:
        tips.append("Your weekly training volume looks manageable if recovery habits stay solid.")

    if goal == "Lose fat":
        tips.append("Since you may be in a calorie deficit, recovery may be a little harder, so keep training productive but controlled.")
    elif goal == "Build muscle":
        tips.append("To support muscle gain, keep food intake, sleep, and training effort consistent.")
    else:
        tips.append("Focus on consistency, form, and sustainable weekly progress.")

    return tips


def get_progression_rules(goal, experience_level):
    rules = [
        "When you complete all sets at the top of the rep range with good form, increase the weight slightly next session."
    ]

    if experience_level == "Beginner":
        rules.append("As a beginner, focus on learning technique and adding reps before adding a lot of weight.")
    elif experience_level == "Intermediate":
        rules.append("As an intermediate lifter, use small weight increases and improve either reps or load over time.")
    else:
        rules.append("As an advanced lifter, progress may be slower, so use small changes in load, reps, or volume.")

    if goal == "Lose fat":
        rules.append("During fat loss, focus on maintaining strength and muscle rather than chasing aggressive strength gains.")
    elif goal == "Build muscle":
        rules.append("For muscle gain, try to gradually improve reps, load, or control over time across your main lifts.")
    else:
        rules.append("Keep progression steady and sustainable rather than forcing big jumps.")

    return rules


def get_day_labels(selected_days, training_days):
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    actual_days = [day for day in ordered_days if day in selected_days]

    if len(actual_days) >= training_days:
        return actual_days[:training_days]
    return ordered_days[:training_days]


def build_workout_plan(training_days, equipment, workout_time, injury_keywords, experience_level, goal, preferred_focus, selected_days):
    max_exercises = get_time_adjustment(workout_time)

    gym_push = [
        "Barbell Bench Press 3 x 8-10",
        "Incline Dumbbell Press 3 x 8-10",
        "Machine Chest Press 3 x 10-12",
        "Cable Fly 2 x 12-15",
        "Seated Dumbbell Shoulder Press 3 x 8-10",
        "Lateral Raise 3 x 12-15",
        "Rope Tricep Pushdown 3 x 10-12"
    ]

    gym_pull = [
        "Lat Pulldown 3 x 8-10",
        "Chest Supported Row 3 x 8-10",
        "Seated Cable Row 3 x 10-12",
        "Rear Delt Fly 3 x 12-15",
        "Face Pull 2 x 15",
        "EZ Bar Curl 3 x 10-12",
        "Hammer Curl 2 x 12"
    ]

    gym_legs = [
        "Barbell Squat 3 x 6-8",
        "Leg Press 3 x 10",
        "Romanian Deadlift 3 x 8-10",
        "Walking Lunges 2 x 10 each leg",
        "Leg Curl 3 x 12",
        "Leg Extension 2 x 12-15",
        "Standing Calf Raise 3 x 15"
    ]

    dumbbell_push = [
        "Dumbbell Bench Press 3 x 8-10",
        "Incline Dumbbell Press 3 x 8-10",
        "Floor Press 3 x 10",
        "Seated Dumbbell Shoulder Press 3 x 8-10",
        "Lateral Raise 3 x 12-15",
        "Overhead Dumbbell Tricep Extension 3 x 10-12"
    ]

    dumbbell_pull = [
        "One Arm Dumbbell Row 3 x 10 each side",
        "Chest Supported Dumbbell Row 3 x 10",
        "Rear Delt Raise 3 x 12-15",
        "Hammer Curl 3 x 10-12",
        "Alternating Dumbbell Curl 2 x 12"
    ]

    dumbbell_legs = [
        "Goblet Squat 3 x 10",
        "Dumbbell Romanian Deadlift 3 x 10",
        "Bulgarian Split Squat 3 x 8 each leg",
        "Reverse Lunge 2 x 10 each leg",
        "Dumbbell Calf Raise 3 x 15"
    ]

    bodyweight_full = [
        "Push Ups 3 x 10-15",
        "Bodyweight Squats 3 x 15",
        "Glute Bridges 3 x 15",
        "Walking Lunges 2 x 10 each leg",
        "Pike Push Ups 3 x 8-10",
        "Plank 3 x 30-45 seconds"
    ]

    if equipment in ["Full gym", "Home gym"]:
        push = filter_exercises_for_injuries(gym_push, injury_keywords)
        pull = filter_exercises_for_injuries(gym_pull, injury_keywords)
        legs = filter_exercises_for_injuries(gym_legs, injury_keywords)
    elif equipment == "Dumbbells only":
        push = filter_exercises_for_injuries(dumbbell_push, injury_keywords)
        pull = filter_exercises_for_injuries(dumbbell_pull, injury_keywords)
        legs = filter_exercises_for_injuries(dumbbell_legs, injury_keywords)
    else:
        push = filter_exercises_for_injuries(bodyweight_full, injury_keywords)
        pull = filter_exercises_for_injuries(bodyweight_full, injury_keywords)
        legs = filter_exercises_for_injuries(bodyweight_full, injury_keywords)

    if goal == "Build muscle":
        max_exercises = min(max_exercises + 1, 7)
    elif goal == "Lose fat":
        max_exercises = max(4, max_exercises - 1)

    if preferred_focus == "Chest":
        push = [push[0], push[1]] + push
    elif preferred_focus == "Back":
        pull = [pull[0], pull[1]] + pull
    elif preferred_focus == "Legs":
        legs = [legs[0], legs[1]] + legs
    elif preferred_focus == "Shoulders":
        push = [ex for ex in push if "Shoulder" in ex or "Lateral" in ex] + push
    elif preferred_focus == "Arms":
        push = [ex for ex in push if "Tricep" in ex] + push
        pull = [ex for ex in pull if "Curl" in ex] + pull

    push = [adjust_sets_by_experience(ex, experience_level) for ex in push]
    pull = [adjust_sets_by_experience(ex, experience_level) for ex in pull]
    legs = [adjust_sets_by_experience(ex, experience_level) for ex in legs]

    workout_days = {}
    day_labels = get_day_labels(selected_days, training_days)

    if training_days <= 2:
        full_body = (push[:2] + pull[:2] + legs[:2])[:max_exercises]
        workout_days[f"{day_labels[0]} - Full Body"] = full_body
        if training_days == 2:
            workout_days[f"{day_labels[1]} - Full Body"] = full_body

    elif training_days == 3:
        workout_days[f"{day_labels[0]} - Upper Body 🏋️"] = (push[:3] + pull[:2])[:max_exercises]
        workout_days[f"{day_labels[1]} - Lower Body"] = legs[:max_exercises]
        workout_days[f"{day_labels[2]} - Full Body"] = (push[:2] + pull[:2] + legs[:2])[:max_exercises]

    elif training_days == 4:
        workout_days[f"{day_labels[0]} - Upper Body 🏋️"] = (push[:3] + pull[:2])[:max_exercises]
        workout_days[f"{day_labels[1]} - Lower Body"] = legs[:max_exercises]
        workout_days[f"{day_labels[2]} - Upper Body 🏋️"] = (pull[:3] + push[:2])[:max_exercises]
        workout_days[f"{day_labels[3]} - Lower Body"] = legs[:max_exercises]

    elif training_days == 5:
        workout_days[f"{day_labels[0]} - Push 🏋️"] = push[:max_exercises]
        workout_days[f"{day_labels[1]} - Pull 🏋️"] = pull[:max_exercises]
        workout_days[f"{day_labels[2]} - Legs"] = legs[:max_exercises]
        workout_days[f"{day_labels[3]} - Upper 🏋️"] = (push[:2] + pull[:3])[:max_exercises]
        workout_days[f"{day_labels[4]} - Lower Body"] = legs[:max_exercises]

    else:
        workout_days[f"{day_labels[0]} - Push 🏋️"] = push[:max_exercises]
        workout_days[f"{day_labels[1]} - Pull 🏋️"] = pull[:max_exercises]
        workout_days[f"{day_labels[2]} - Legs"] = legs[:max_exercises]
        workout_days[f"{day_labels[3]} - Push 🏋️"] = push[:max_exercises]
        workout_days[f"{day_labels[4]} - Pull 🏋️"] = pull[:max_exercises]
        workout_days[f"{day_labels[5]} - Legs"] = legs[:max_exercises]

    return workout_days


# -------------------------------------------------
# Multi-agent classes
# -------------------------------------------------
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
    experience_level: str
    preferred_focus: str
    cardio_preference: str
    selected_days: list


class PlannerAgent:
    def run(self, profile: UserProfile):
        injury_keywords = detect_injury_keywords(profile.injuries)
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
            "risk_flags": risk_flags,
            "injury_keywords": injury_keywords
        }


class AnalysisAgent:
    def run(self, profile: UserProfile, plan: dict):
        bmr = calculate_bmr(profile.weight_lbs, profile.height_ft, profile.height_in, profile.age, profile.sex)
        tdee = bmr * activity_multiplier(profile.activity_level)

        if profile.goal == "Lose fat":
            target_calories = tdee - 500
            calorie_note = "A moderate calorie deficit was applied for fat loss."
        elif profile.goal == "Build muscle":
            target_calories = tdee + 250
            calorie_note = "A small calorie surplus was applied for muscle gain."
        else:
            target_calories = tdee
            calorie_note = "Maintenance calories were used as the starting point."

        protein_low = round(profile.weight_lbs * 0.7)
        protein_high = round(profile.weight_lbs * 1.0)

        training_guidance = goal_focus_text(profile.goal)
        cardio_plan = get_cardio_plan(profile.goal, profile.activity_level, profile.cardio_preference)
        meal_guidance = get_meal_guidance(profile.diet, protein_low, protein_high, round(target_calories))
        recovery_guidance = get_recovery_guidance(profile.training_days, profile.goal)
        progression_rules = get_progression_rules(profile.goal, profile.experience_level)
        injury_info = get_injury_guidance(plan["injury_keywords"])

        detailed_workout = build_workout_plan(
            profile.training_days,
            profile.equipment,
            profile.workout_time,
            plan["injury_keywords"],
            profile.experience_level,
            profile.goal,
            profile.preferred_focus,
            profile.selected_days
        )

        nutrition_guidance = {
            "No preference": "Choose mostly whole foods that match your calories and protein target.",
            "High protein": "Build each meal around a strong lean protein source.",
            "Vegetarian": "Use Greek yogurt, eggs, tofu, tempeh, beans, lentils, and shakes.",
            "Low carb": "Prioritize protein, vegetables, and healthy fats while keeping carbs lower.",
            "Budget-friendly": "Use oats, rice, potatoes, eggs, canned tuna, chicken, and frozen vegetables."
        }.get(profile.diet, "Choose foods you can stay consistent with.")

        return {
            "agent": "AnalysisAgent",
            "status": "completed",
            "bmr": round(bmr),
            "tdee": round(tdee),
            "target_calories": round(target_calories),
            "calorie_note": calorie_note,
            "protein_low": protein_low,
            "protein_high": protein_high,
            "workout_split": workout_split(profile.training_days),
            "training_guidance": training_guidance,
            "nutrition_guidance": nutrition_guidance,
            "cardio_plan": cardio_plan,
            "meal_guidance": meal_guidance,
            "recovery_guidance": recovery_guidance,
            "progression_rules": progression_rules,
            "injury_info": injury_info,
            "detailed_workout": detailed_workout
        }


class VerifierAgent:
    def run(self, profile: UserProfile, plan: dict, analysis: dict):
        warnings = []

        if analysis["target_calories"] < 1200:
            warnings.append("Suggested calories are very low, so this result should be treated cautiously.")
        if "injury_or_limitation_present" in plan["risk_flags"]:
            warnings.append("The workout was adjusted in a general way based on your injury keywords. Avoid painful movements.")
        if "high_training_frequency" in plan["risk_flags"]:
            warnings.append("High weekly training frequency means recovery, sleep, and exercise quality need close attention.")

        final_summary = (
            f"Estimated BMR: {analysis['bmr']} calories/day. "
            f"Estimated TDEE: {analysis['tdee']} calories/day. "
            f"Suggested daily calories: {analysis['target_calories']}. "
            f"Suggested protein: {analysis['protein_low']} to {analysis['protein_high']} grams per day."
        )

        return {
            "agent": "VerifierAgent",
            "status": "completed",
            "warnings": warnings,
            "final_summary": final_summary
        }


class ControllerAgent:
    def __init__(self):
        self.planner = PlannerAgent()
        self.analyzer = AnalysisAgent()
        self.verifier = VerifierAgent()

    def run(self, profile: UserProfile):
        plan = self.planner.run(profile)
        analysis = self.analyzer.run(profile, plan)
        verification = self.verifier.run(profile, plan, analysis)
        return {"plan": plan, "analysis": analysis, "verification": verification}


# -------------------------------------------------
# Hero
# -------------------------------------------------
hero_greeting = get_fun_greeting()
hero_joke = get_fun_joke()

st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">🏋️ AI Health & Fitness Planning Agent</div>
    <div class="hero-sub">
        {hero_greeting} Build a personalized workout, calorie, cardio, nutrition, and recovery plan
        with a cleaner interface and a multi-agent fitness workflow.
    </div>
    <div class="hero-joke">{hero_joke}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Form
# -------------------------------------------------
with st.form("fitness_form"):
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("👤 Personal Information")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=13, max_value=80, value=21, step=1)
        sex = st.selectbox("Sex", ["Male", "Female"])

        st.subheader("📏 Body Information")
        weight_lbs = st.number_input("Weight (lbs)", min_value=80.0, max_value=500.0, value=180.0, step=1.0)
        h1, h2 = st.columns(2)
        with h1:
            height_ft = st.number_input("Height - Feet", min_value=3, max_value=8, value=6, step=1)
        with h2:
            height_in = st.number_input("Height - Inches", min_value=0, max_value=11, value=0, step=1)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🎯 Goals and Activity")
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
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏋️ Workout Preferences")
        equipment = st.selectbox(
            "Equipment Access",
            ["Full gym", "Home gym", "Dumbbells only", "Bodyweight only"]
        )
        diet = st.selectbox(
            "Diet Preference",
            ["No preference", "High protein", "Vegetarian", "Low carb", "Budget-friendly"]
        )
        experience_level = st.selectbox(
            "Training Experience",
            ["Beginner", "Intermediate", "Advanced"]
        )
        preferred_focus = st.selectbox(
            "Preferred Muscle Focus",
            ["No preference", "Chest", "Back", "Legs", "Shoulders", "Arms"]
        )
        cardio_preference = st.selectbox(
            "Preferred Cardio",
            ["No preference", "Walking", "Bike", "Running", "Other"]
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🗓️ Training Schedule")
        selected_days = st.multiselect(
            "Preferred Training Days",
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            default=["Monday", "Tuesday", "Thursday", "Friday"]
        )

        st.subheader("🩺 Limitations")
        injuries = st.text_area("Injuries / Limitations", placeholder="Example: shoulder pain, knee pain, lower back issue")
        notes = st.text_area("Anything else we should know?", placeholder="Optional")
        st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.form_submit_button("Generate My Plan")


# -------------------------------------------------
# Results
# -------------------------------------------------
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
        notes=notes,
        experience_level=experience_level,
        preferred_focus=preferred_focus,
        cardio_preference=cardio_preference,
        selected_days=selected_days
    )

    controller = ControllerAgent()
    result = controller.run(profile)

    plan = result["plan"]
    analysis = result["analysis"]
    verification = result["verification"]

    st.markdown("---")

    display_name = name.strip() if name.strip() else "User"
    intro_text = get_results_intro(name, goal)
    motivation_text = get_goal_motivation(goal)

    st.markdown(f"""
    <div class="result-intro">
        {intro_text} {motivation_text}
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="section-card">
        <h2 style="margin-bottom:0.5rem;">Personalized Plan for {display_name}</h2>
        <span class="pill">Goal: {goal}</span>
        <span class="pill">Split: {analysis['workout_split']}</span>
        <span class="pill">Days: {training_days}</span>
        <span class="pill">Experience: {experience_level}</span>
        <span class="pill">Equipment: {equipment}</span>
        <span class="pill">Focus: {preferred_focus}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("📊 Key Numbers")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("BMR", f"{analysis['bmr']}")
    with c2:
        st.metric("TDEE", f"{analysis['tdee']}")
    with c3:
        st.metric("Target Calories", f"{analysis['target_calories']}")
    with c4:
        st.metric("Protein", f"{analysis['protein_low']}–{analysis['protein_high']}g")
    st.caption(analysis["calorie_note"])
    st.markdown('</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🏋️ Training Focus")
        st.write(analysis["training_guidance"])

        st.subheader("❤️ Cardio Recommendation")
        st.write(analysis["cardio_plan"])

        st.subheader("📈 Progression Rules")
        for rule in analysis["progression_rules"]:
            st.write(f"• {rule}")
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("🍽️ Nutrition and Meals")
        st.write(analysis["nutrition_guidance"])
        st.write(f"**Meal Structure:** {analysis['meal_guidance']['meals_per_day']}")
        st.write(f"**Protein Target:** {analysis['meal_guidance']['protein_target']}")
        st.write(f"**Food Examples:** {analysis['meal_guidance']['food_examples']}")

        st.subheader("💤 Recovery Guidance")
        for item in analysis["recovery_guidance"]:
            st.write(f"• {item}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🗓️ Detailed Workout Plan")
    for day, exercises in analysis["detailed_workout"].items():
        st.markdown(f'<div class="workout-day"><div class="workout-day-title">{day}</div>', unsafe_allow_html=True)
        for ex in exercises:
            st.markdown(f'<div class="exercise-item">{ex}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("🩺 Injury and Limitation Guidance")
    for item in analysis["injury_info"]["guidance"]:
        st.write(f"• {item}")

    if analysis["injury_info"]["avoid"]:
        st.markdown("**Movements to Be Careful With**")
        for item in analysis["injury_info"]["avoid"]:
            st.write(f"• {item}")

    if analysis["injury_info"]["substitutes"]:
        st.markdown("**Potential Better Substitutes**")
        for item in analysis["injury_info"]["substitutes"]:
            st.write(f"• {item}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-box">
        <h3>Weekly Summary</h3>
        <p><strong>Workout Split:</strong> {analysis['workout_split']}</p>
        <p><strong>Calories:</strong> {analysis['target_calories']} per day</p>
        <p><strong>Protein:</strong> {analysis['protein_low']} to {analysis['protein_high']} grams per day</p>
        <p><strong>Final Summary:</strong> {verification['final_summary']}</p>
    </div>
    """, unsafe_allow_html=True)

    if verification["warnings"]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("⚠️ Recovery and Safety")
        for warning in verification["warnings"]:
            st.warning(warning)
        st.markdown('</div>', unsafe_allow_html=True)

    if notes.strip():
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.subheader("📝 Additional Notes")
        st.write(notes)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("Show Multi-Agent Workflow Details"):
        st.markdown("**Planner Agent Output**")
        st.json(plan)
        st.markdown("**Analysis Agent Output**")
        st.json(analysis)
        st.markdown("**Verifier Agent Output**")
        st.json(verification)

    st.markdown(
        '<div class="footer-note">This tool provides general wellness guidance only and is not medical advice.</div>',
        unsafe_allow_html=True
    )
