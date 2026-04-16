import streamlit as st
from dataclasses import dataclass

st.set_page_config(
    page_title="AI Health & Fitness Planning Agent",
    page_icon="🏋️",
    layout="centered"
)

st.title("AI Health & Fitness Planning Agent")
st.write(
    "Fill out the information below to receive a personalized workout, nutrition, cardio, and recovery recommendation."
)
st.caption("This version includes a multi-agent workflow, detailed workouts, injury-aware guidance, cardio, progression rules, and a weekly summary.")

st.markdown("---")


# -----------------------------
# Helper functions
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


def get_time_adjustment(workout_time):
    if workout_time == "20-30 minutes":
        return 4
    elif workout_time == "30-45 minutes":
        return 5
    elif workout_time == "45-60 minutes":
        return 6
    return 7


def get_experience_adjustment(experience_level):
    if experience_level == "Beginner":
        return 0.85
    elif experience_level == "Intermediate":
        return 1.0
    return 1.15


def adjust_sets_by_experience(exercise_line, experience_level):
    if "3 x" not in exercise_line and "2 x" not in exercise_line and "4 x" not in exercise_line:
        return exercise_line

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
        "knee": ["knee", "patellar", "acl", "meniscus"],
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
        guidance.append(
            "Shoulder issue detected. Reduce or avoid painful overhead pressing, deep dips, and aggressive ranges of motion."
        )
        avoid.extend(["Heavy overhead press", "Deep dips", "Upright rows if painful"])
        substitutes.extend(["Neutral grip dumbbell press", "Machine chest press", "Cable fly", "Controlled lateral raises"])

    if "knee" in injury_keywords:
        guidance.append(
            "Knee issue detected. Reduce movements that cause pain, especially deep knee bending under heavy load."
        )
        avoid.extend(["Painful deep squats", "Jumping drills if painful", "Explosive lunges if painful"])
        substitutes.extend(["Box squats", "Leg press with controlled range", "Glute bridges", "Hamstring curls"])

    if "back" in injury_keywords:
        guidance.append(
            "Back issue detected. Be careful with heavy spinal loading and focus on bracing and controlled form."
        )
        avoid.extend(["Heavy conventional deadlifts", "Loose form barbell rows", "Excessive spinal loading"])
        substitutes.extend(["Chest supported rows", "Machine rows", "Goblet squats", "Hip thrusts"])

    if "elbow" in injury_keywords:
        guidance.append(
            "Elbow issue detected. Limit movements that irritate the joint and use cable or machine options when needed."
        )
        avoid.extend(["Very heavy skull crushers", "Straight bar curls if painful"])
        substitutes.extend(["Rope pushdowns", "Hammer curls", "Machine curls"])

    if "wrist" in injury_keywords:
        guidance.append(
            "Wrist issue detected. Use neutral grip options and avoid forcing the wrist into painful positions."
        )
        avoid.extend(["Straight bar pressing if painful", "Exercises that force wrist extension"])
        substitutes.extend(["Dumbbell pressing", "Neutral grip rows", "Cable handles"])

    if "ankle" in injury_keywords:
        guidance.append(
            "Ankle or foot issue detected. Limit jumping and unstable lower body work if painful."
        )
        avoid.extend(["Jumping drills", "High impact cardio if painful"])
        substitutes.extend(["Bike", "Leg press", "Seated hamstring curl", "Stable split stance work"])

    if not guidance:
        guidance.append("No major injury keywords were detected. Train with good form, gradual progression, and proper recovery.")

    return {
        "guidance": guidance,
        "avoid": avoid,
        "substitutes": substitutes
    }


def filter_exercises_for_injuries(exercises, injury_keywords):
    filtered = []

    for ex in exercises:
        name_lower = ex.lower()

        if "shoulder" in injury_keywords:
            if "overhead" in name_lower or "upright row" in name_lower or "dip" in name_lower:
                continue

        if "knee" in injury_keywords:
            if "jump" in name_lower or "jump squat" in name_lower:
                continue

        if "back" in injury_keywords:
            if "deadlift" in name_lower or "barbell row" in name_lower:
                continue

        filtered.append(ex)

    return filtered


def goal_focus_text(goal):
    if goal == "Lose fat":
        return "The workout plan is focused on maintaining muscle, staying efficient, and supporting a calorie deficit."
    elif goal == "Build muscle":
        return "The workout plan is focused on hypertrophy, solid exercise volume, and progressive overload."
    elif goal == "Maintain weight":
        return "The workout plan is focused on balanced training, strength maintenance, and consistency."
    return "The workout plan is focused on balanced fitness, movement quality, and general health."


def get_cardio_plan(goal, activity_level, cardio_preference):
    if goal == "Lose fat":
        recommendation = "Aim for 3 to 5 cardio sessions per week for 20 to 30 minutes."
    elif goal == "Build muscle":
        recommendation = "Aim for 2 to 3 light cardio sessions per week for 15 to 20 minutes to support health and recovery."
    elif goal == "Maintain weight":
        recommendation = "Aim for 2 to 4 cardio sessions per week for 20 to 25 minutes."
    else:
        recommendation = "Aim for 3 cardio sessions per week for 20 to 30 minutes."

    if cardio_preference == "Walking":
        mode = "Brisk walking or incline treadmill"
    elif cardio_preference == "Bike":
        mode = "Stationary bike or outdoor cycling"
    elif cardio_preference == "Running":
        mode = "Easy to moderate running"
    elif cardio_preference == "No preference":
        mode = "Walking, bike, treadmill, or other low stress cardio"
    else:
        mode = "Cardio of your choice based on comfort and consistency"

    if activity_level == "Sedentary (little or no exercise)":
        extra = "Start on the lower end and build up gradually."
    else:
        extra = "Keep the intensity moderate so it supports recovery."

    return f"{recommendation} Best option: {mode}. {extra}"


def get_meal_guidance(diet, target_calories, protein_low, protein_high):
    avg_protein = round((protein_low + protein_high) / 2)

    if target_calories < 1800:
        meals_per_day = "3 meals and 1 snack"
    elif target_calories < 2500:
        meals_per_day = "3 to 4 meals per day"
    else:
        meals_per_day = "4 meals and 1 to 2 snacks"

    if diet == "High protein":
        foods = "chicken breast, Greek yogurt, eggs, tuna, lean beef, protein shakes"
    elif diet == "Vegetarian":
        foods = "Greek yogurt, eggs, tofu, tempeh, beans, lentils, protein shakes"
    elif diet == "Low carb":
        foods = "lean meats, eggs, Greek yogurt, vegetables, avocado, nuts in moderation"
    elif diet == "Budget-friendly":
        foods = "rice, oats, eggs, potatoes, chicken, canned tuna, frozen vegetables"
    else:
        foods = "lean proteins, fruit, vegetables, potatoes, rice, oats, dairy, and healthy fats"

    return {
        "meals_per_day": meals_per_day,
        "protein_target": f"Aim for about {avg_protein} grams of protein per day.",
        "food_examples": f"Good food options include {foods}."
    }


def get_recovery_guidance(training_days, goal):
    sleep_text = "Aim for about 7 to 9 hours of sleep per night."
    hydration_text = "Stay hydrated consistently throughout the day, especially around training."
    rest_text = "Take at least 1 to 2 lighter or rest days each week depending on fatigue."

    if training_days >= 5:
        volume_text = "Because training frequency is higher, keep an eye on soreness, sleep, and motivation."
    else:
        volume_text = "Your weekly training volume looks manageable if recovery habits are solid."

    if goal == "Lose fat":
        goal_text = "Since you may be in a calorie deficit, recovery may feel a little harder, so keep intensity productive but controlled."
    elif goal == "Build muscle":
        goal_text = "To support muscle gain, keep food intake, sleep, and training effort consistent."
    else:
        goal_text = "Focus on consistency, form, and steady weekly progress."

    return [sleep_text, hydration_text, rest_text, volume_text, goal_text]


def get_progression_rules(goal, experience_level):
    base_rule = "When you can complete all prescribed sets at the top of the rep range with good form, increase the weight slightly next session."

    if experience_level == "Beginner":
        exp_rule = "As a beginner, focus more on learning technique and adding reps before adding a lot of weight."
    elif experience_level == "Intermediate":
        exp_rule = "As an intermediate lifter, use small weight increases and try to improve either reps or load over time."
    else:
        exp_rule = "As an advanced lifter, progress may be slower, so track performance carefully and use small changes in load, reps, or volume."

    if goal == "Lose fat":
        goal_rule = "During fat loss, the main goal is usually maintaining strength and muscle rather than forcing rapid strength gains."
    elif goal == "Build muscle":
        goal_rule = "For muscle gain, try to gradually improve reps, load, or control over time across your main lifts."
    else:
        goal_rule = "Keep progression steady and sustainable rather than chasing big jumps."

    return [base_rule, exp_rule, goal_rule]


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
        workout_days[f"{day_labels[0]} - Upper Body"] = (push[:3] + pull[:2])[:max_exercises]
        workout_days[f"{day_labels[1]} - Lower Body"] = legs[:max_exercises]
        workout_days[f"{day_labels[2]} - Full Body"] = (push[:2] + pull[:2] + legs[:2])[:max_exercises]

    elif training_days == 4:
        workout_days[f"{day_labels[0]} - Upper Body"] = (push[:3] + pull[:2])[:max_exercises]
        workout_days[f"{day_labels[1]} - Lower Body"] = legs[:max_exercises]
        workout_days[f"{day_labels[2]} - Upper Body"] = (pull[:3] + push[:2])[:max_exercises]
        workout_days[f"{day_labels[3]} - Lower Body"] = legs[:max_exercises]

    elif training_days == 5:
        workout_days[f"{day_labels[0]} - Push"] = push[:max_exercises]
        workout_days[f"{day_labels[1]} - Pull"] = pull[:max_exercises]
        workout_days[f"{day_labels[2]} - Legs"] = legs[:max_exercises]
        workout_days[f"{day_labels[3]} - Upper"] = (push[:2] + pull[:3])[:max_exercises]
        workout_days[f"{day_labels[4]} - Lower"] = legs[:max_exercises]

    else:
        workout_days[f"{day_labels[0]} - Push"] = push[:max_exercises]
        workout_days[f"{day_labels[1]} - Pull"] = pull[:max_exercises]
        workout_days[f"{day_labels[2]} - Legs"] = legs[:max_exercises]
        workout_days[f"{day_labels[3]} - Push"] = push[:max_exercises]
        workout_days[f"{day_labels[4]} - Pull"] = pull[:max_exercises]
        workout_days[f"{day_labels[5]} - Legs"] = legs[:max_exercises]

    return workout_days


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
    experience_level: str
    preferred_focus: str
    cardio_preference: str
    selected_days: list


class PlannerAgent:
    def run(self, profile: UserProfile):
        tasks = [
            "calculate_bmr",
            "calculate_tdee",
            "set_calorie_target",
            "set_protein_target",
            "choose_workout_split",
            "generate_specific_workout_plan",
            "generate_goal_based_guidance",
            "generate_nutrition_guidance",
            "generate_cardio_recommendation",
            "analyze_injury_keywords",
            "generate_recovery_guidance",
            "generate_progression_rules",
            "perform_safety_check"
        ]

        risk_flags = []
        injury_keywords = detect_injury_keywords(profile.injuries)

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
            "injury_keywords": injury_keywords,
            "input_summary": {
                "goal": profile.goal,
                "activity_level": profile.activity_level,
                "training_days": profile.training_days,
                "diet": profile.diet,
                "equipment": profile.equipment,
                "experience_level": profile.experience_level,
                "preferred_focus": profile.preferred_focus
            }
        }


class AnalysisAgent:
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

        if profile.training_days <= 3:
            training_guidance = "Focus on consistency, compound lifts, and steady progression each week."
        elif profile.training_days == 4:
            training_guidance = "An upper and lower structure gives a strong balance of frequency and recovery."
        else:
            training_guidance = "Higher frequency can work well if sleep, recovery, and exercise quality stay strong."

        if profile.workout_time == "20-30 minutes":
            training_guidance += " Keep workouts focused on the main lifts and avoid too much extra volume."
        elif profile.workout_time == "30-45 minutes":
            training_guidance += " You have enough time for your main lifts plus a few accessories."
        elif profile.workout_time == "45-60 minutes":
            training_guidance += " This is a strong time range for a balanced session."
        else:
            training_guidance += " Be careful not to add junk volume just because you have more time."

        if profile.experience_level == "Beginner":
            training_guidance += " Because you selected beginner, the program keeps things simpler and more manageable."
        elif profile.experience_level == "Advanced":
            training_guidance += " Because you selected advanced, the program allows a bit more training volume."

        if profile.diet == "High protein":
            nutrition_guidance = "Build each meal around a lean protein source and try to spread protein across the day."
        elif profile.diet == "Vegetarian":
            nutrition_guidance = "Use foods like Greek yogurt, eggs, tofu, tempeh, beans, lentils, and protein shakes."
        elif profile.diet == "Low carb":
            nutrition_guidance = "Keep carbs lower and prioritize protein, vegetables, and healthy fats."
        elif profile.diet == "Budget-friendly":
            nutrition_guidance = "Focus on lower cost staples like oats, rice, potatoes, eggs, tuna, frozen vegetables, and chicken."
        else:
            nutrition_guidance = "Choose mostly whole foods that match your calorie target and that you can stay consistent with."

        injury_keywords = plan.get("injury_keywords", [])
        injury_info = get_injury_guidance(injury_keywords)

        detailed_workout = build_workout_plan(
            profile.training_days,
            profile.equipment,
            profile.workout_time,
            injury_keywords,
            profile.experience_level,
            profile.goal,
            profile.preferred_focus,
            profile.selected_days
        )

        cardio_plan = get_cardio_plan(profile.goal, profile.activity_level, profile.cardio_preference)
        meal_guidance = get_meal_guidance(profile.diet, round(target_calories), round(protein_low), round(protein_high))
        recovery_guidance = get_recovery_guidance(profile.training_days, profile.goal)
        progression_rules = get_progression_rules(profile.goal, profile.experience_level)
        goal_emphasis = goal_focus_text(profile.goal)

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
            "nutrition_guidance": nutrition_guidance,
            "goal_emphasis": goal_emphasis,
            "injury_info": injury_info,
            "detailed_workout": detailed_workout,
            "cardio_plan": cardio_plan,
            "meal_guidance": meal_guidance,
            "recovery_guidance": recovery_guidance,
            "progression_rules": progression_rules
        }


class VerifierAgent:
    def run(self, profile: UserProfile, plan: dict, analysis: dict):
        warnings = []

        if analysis["target_calories"] < 1200:
            warnings.append(
                "Suggested calories were very low, so this result should be treated cautiously."
            )

        if "injury_or_limitation_present" in plan["risk_flags"]:
            warnings.append(
                "Your workout was adjusted in a general way based on the injury keywords entered. Avoid painful movements and consider a medical professional if needed."
            )

        if "high_training_frequency" in plan["risk_flags"]:
            warnings.append(
                "High weekly training frequency means recovery, sleep, and exercise quality need close attention."
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
# Streamlit form
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

    st.subheader("Training Schedule")
    selected_days = st.multiselect(
        "Preferred Training Days",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        default=["Monday", "Tuesday", "Thursday", "Friday"]
    )

    st.subheader("Limitations")
    injuries = st.text_area("Injuries / Limitations", placeholder="Example: shoulder pain, knee pain, lower back issue")
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
    st.subheader("Your Personalized Results")

    if name.strip():
        st.write(f"**Name:** {name}")

    st.write(f"**Goal:** {goal}")
    st.write(f"**Suggested Workout Split:** {analysis['workout_split']}")
    st.write(f"**Workout Time:** {workout_time}")
    st.write(f"**Equipment Access:** {equipment}")
    st.write(f"**Training Experience:** {experience_level}")
    st.write(f"**Preferred Focus:** {preferred_focus}")

    st.markdown("### Goal Based Training Focus")
    st.write(analysis["goal_emphasis"])

    st.markdown("### Calorie Estimates")
    st.write(f"**Estimated BMR:** {analysis['bmr']} calories/day")
    st.write(f"**Estimated Maintenance Calories (TDEE):** {analysis['tdee']} calories/day")
    st.write(f"**Suggested Daily Calories for Your Goal:** {analysis['target_calories']} calories/day")
    st.caption(analysis["calorie_note"])

    st.markdown("### Protein Recommendation")
    st.write(f"Suggested protein intake: **{analysis['protein_low']} to {analysis['protein_high']} grams/day**")

    st.markdown("### Training Recommendation")
    st.write(analysis["training_guidance"])

    st.markdown("### Detailed Workout Plan")
    for day, exercises in analysis["detailed_workout"].items():
        st.markdown(f"**{day}**")
        for ex in exercises:
            st.write(f"- {ex}")

    st.markdown("### Cardio Recommendation")
    st.write(analysis["cardio_plan"])

    st.markdown("### Nutrition Guidance")
    st.write(analysis["nutrition_guidance"])

    st.markdown("### Meal Guidance")
    st.write(f"**Suggested Meal Structure:** {analysis['meal_guidance']['meals_per_day']}")
    st.write(f"**Protein Target:** {analysis['meal_guidance']['protein_target']}")
    st.write(f"**Food Examples:** {analysis['meal_guidance']['food_examples']}")

    st.markdown("### Injury and Limitation Guidance")
    for item in analysis["injury_info"]["guidance"]:
        st.write(f"- {item}")

    if analysis["injury_info"]["avoid"]:
        st.markdown("**Movements to Be Careful With**")
        for item in analysis["injury_info"]["avoid"]:
            st.write(f"- {item}")

    if analysis["injury_info"]["substitutes"]:
        st.markdown("**Potential Better Substitutes**")
        for item in analysis["injury_info"]["substitutes"]:
            st.write(f"- {item}")

    st.markdown("### Progression Rules")
    for rule in analysis["progression_rules"]:
        st.write(f"- {rule}")

    st.markdown("### Recovery Guidance")
    for item in analysis["recovery_guidance"]:
        st.write(f"- {item}")

    st.markdown("### Weekly Summary")
    st.info(
        f"Workout Split: {analysis['workout_split']} | "
        f"Calories: {analysis['target_calories']} per day | "
        f"Protein: {analysis['protein_low']} to {analysis['protein_high']} grams per day"
    )

    st.markdown("### Recovery and Safety")
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
