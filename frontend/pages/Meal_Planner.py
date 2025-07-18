import streamlit as st
import requests

st.set_page_config(
    page_title="Meal Planner",
    page_icon="🥗",
)

st.title("🥗 Goal-Based Meal Planner")

if not st.session_state.get('user_profile'):
    st.warning("Please set up your profile on the Home page to use the Meal Planner.")
    st.stop()

user = st.session_state['user_profile']

# --- 1. BMR and Base Calorie Calculation ---
def calculate_bmr(user):
    weight = user['weight']
    height = user['height']
    age = user['age']
    gender = user['gender']
    activity = user['activity_level']

    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    multiplier = {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Extremely Active": 1.9
    }.get(activity, 1.2)

    return bmr * multiplier

base_calories = calculate_bmr(user)

# --- 2. Goal Setup ---
st.subheader("🎯 Set Your Nutrition Goal")

goal = st.selectbox("Choose your goal", ["Maintain Weight", "Lose Weight", "Gain Weight"])

if goal in ["Lose Weight", "Gain Weight"]:
    target_kg = st.number_input(f"How many kg do you want to {goal.lower()}?", min_value=0.5, max_value=20.0, step=0.5)
    weeks = st.number_input("In how many weeks?", min_value=1, max_value=52, step=1)

    total_calorie_shift = 7700 * target_kg  # 7700 kcal ≈ 1kg fat
    daily_shift = total_calorie_shift / (weeks * 7)

    if goal == "Lose Weight":
        target_calories = base_calories - daily_shift
    else:
        target_calories = base_calories + daily_shift
else:
    target_calories = base_calories

target_calories = int(target_calories)
st.success(f"🎯 Based on your goal, your daily target is **{target_calories} kcal**")

# --- 3. Plan Option ---
option = st.radio("How would you like to plan your meals?", ["Manual Entry", "Auto Plan (Goal-Based)"])

# --- 4. Manual Mode ---
if option == "Manual Entry":
    st.subheader("🔍 Enter a Dish")
    dish = st.text_input("Enter Dish Name from Dataset (e.g., 'Hot tea (Garam Chai)')")

    if st.button("Get Nutrition Info"):
        try:
            res = requests.post("http://127.0.0.1:5000/predict_meal", json={"Dish Name": dish})
            if res.status_code == 200:
                data = res.json()
                st.write("### Nutrition Info")
                for k, v in data.items():
                    st.write(f"**{k}**: {v}")
            else:
                st.error("Dish not found. Check spelling.")
        except Exception as e:
            st.error(f"Server error: {e}")

# --- 5. Auto Plan Mode ---
elif option == "Auto Plan (Goal-Based)":
    st.subheader("🍽️ Auto Diet Plan Based on Goal")
    try:
        res = requests.post("http://127.0.0.1:5000/generate_plan", json={"calories": target_calories})
        if res.status_code == 200:
            plan = res.json().get("meal_plan", [])
            total = res.json().get("totals", {})
            st.success("Meal Plan Generated!")

            for i, meal in enumerate(plan, 1):
                st.write(f"**Meal {i}**: {meal['Dish Name']}")
                st.caption(f"Calories: {meal['Calories (kcal)']} | Protein: {meal['Protein (g)']}g | Carbs: {meal['Carbohydrates (g)']}g | Fats: {meal['Fats (g)']}g")

            st.markdown("---")
            st.subheader("Daily Totals")
            st.write(f"Calories: **{round(total['Calories (kcal)'], 2)} kcal**")
            st.write(f"Protein: **{round(total['Protein (g)'], 2)} g**")
            st.write(f"Carbohydrates: **{round(total['Carbohydrates (g)'], 2)} g**")
            st.write(f"Fats: **{round(total['Fats (g)'], 2)} g**")
        else:
            st.error("Could not fetch meal plan. Try again.")
    except Exception as e:
        st.error(f"Error contacting backend: {e}")
