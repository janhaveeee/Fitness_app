import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Habit Tracker",
    page_icon="📈",
)

st.title("📈 Habit Tracker")
st.write("Log your daily habits and see your progress.")

if st.session_state.get('user_profile'):
    st.write(f"Hello, {st.session_state['user_profile']['name']}! Let's track your habits.")

    st.subheader("Log Your Habits Today")
    today_date = st.date_input("Date", datetime.now())

    water_oz = st.slider("Water Intake (ml)", min_value=0, max_value=5000, value=2000, step=100)
    sleep_hours = st.slider("Sleep (hours)", min_value=0.0, max_value=12.0, value=7.0, step=0.5)
    steps = st.number_input("Steps Count", min_value=0, value=5000)
    mood = st.select_slider("Mood Today", options=["Terrible", "Bad", "Neutral", "Good", "Excellent"])

    log_button = st.button("Log Habits")

    if log_button:
        # In a real app, you'd save this to a CSV in /data or a database
        log_entry = {
            "Date": today_date.strftime("%Y-%m-%d"),
            "Water_ml": water_oz,
            "Sleep_hours": sleep_hours,
            "Steps": steps,
            "Mood": mood
        }
        st.success("Habits logged successfully! (Data would be saved here)")
        st.json(log_entry) # For demonstration

    st.subheader("Your Progress Forecast")
    st.write("*(Forecast whether you are on track based on historical data - utilizing utils/tracker_forecast.py)*")
    # This section would display charts/metrics based on historical data
    # from utils.tracker_forecast import predict_on_track
    # forecast = predict_on_track(st.session_state['user_profile']['id'])
    # st.write(forecast)

else:
    st.warning("Please set up your profile on the Home page to use the Habit Tracker.")