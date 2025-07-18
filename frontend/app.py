import streamlit as st
import os

import sys

# Make sure you can import from backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from database import users_collection


# Set page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="FitAI App",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session State Initialization ---
if 'user_profile' not in st.session_state:
    st.session_state['user_profile'] = {}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False # For future authentication
if 'is_pro_user' not in st.session_state:
    st.session_state['is_pro_user'] = False # For monetization tier


# --- Header and Welcome ---
st.title("Welcome to FitAI! 🚀")
st.write("Your personalized AI-powered fitness and nutrition companion.")

st.markdown("---")

# --- User Profile Section ---
st.header("🧍‍♂️ Personalized Dashboard")

if not st.session_state['user_profile']:
    st.subheader("Set Up Your Profile (First Time User)")
    with st.expander("Click to set up your profile"):
        with st.form("user_profile_form"):
            name = st.text_input("Name")
            age = st.number_input("Age", min_value=18, max_value=100, value=25)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])

            submitted = st.form_submit_button("Save Profile")
            if submitted:
                profile_data = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "weight": weight,
                    "height": height,
                    "activity_level": activity_level
                }

                st.session_state['user_profile'] = profile_data

                # Save to MongoDB
                users_collection.insert_one(profile_data)

                st.success("Profile saved successfully! You can now explore your personalized modules.")
                st.rerun()

            # Rerun to update dashboard view
else:
    st.subheader(f"Welcome back, {st.session_state['user_profile'].get('name', 'User')}!")
    st.write("Here's a quick overview of your modules and progress:")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Weight", f"{st.session_state['user_profile'].get('weight', 'N/A')} kg")
    with col2:
        st.metric("Age", f"{st.session_state['user_profile'].get('age', 'N/A')} years")
    with col3:
        st.metric("Height", f"{st.session_state['user_profile'].get('height', 'N/A')} cm")

    st.write("""
    **Your Personalized Modules:**
    - **Workout Generator:** Create custom workout plans.
    - **Meal Planner:** Plan your daily meals and track macros.
    - **Habit Tracker:** Log your daily habits and see progress forecasts.
    - **Posture Analysis:** Get feedback on your exercise form.
    - **Log Analyzer:** Analyze your workout history.
    - **Weekly Summary:** Get auto-generated progress reports and tips.
    """)

    st.info("Use the sidebar to navigate to different sections of the app.")

# --- Monetization Plan (Display only, actual logic would be in auth system) ---
st.markdown("---")
st.header("💸 Monetization Tiers")

col_free, col_pro = st.columns(2)

with col_free:
    st.subheader("Free Tier")
    st.write("""
    * 3 workout + meal plans
    * Manual tracking for water, sleep, steps, mood
    """)
    if st.session_state['is_pro_user']:
        st.success("You are currently a Pro user!")
    else:
        st.info("You are currently on the Free Tier.")

with col_pro:
    st.subheader("Pro Tier (SaaS)")
    st.write("""
    * **Full video form feedback** (Posture Analysis)
    * **GPT-based workout + meal generation** (Workout Generator, Meal Planner)
    * **Weekly personalized reports** (Weekly Summary)
    * Downloadable PDFs of plans
    * Cloud data saving (requires Firebase/Supabase integration)
    """)
    st.button("Upgrade to Pro!") # This would link to a payment/subscription flow