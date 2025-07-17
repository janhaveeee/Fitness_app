import streamlit as st

st.set_page_config(
    page_title="Weekly Summary",
    page_icon="💬",
)

st.title("💬 Weekly Summary")
st.write("Get your auto-generated tips and progress report for the week.")

if st.session_state.get('user_profile'):
    st.write(f"Hello, {st.session_state['user_profile']['name']}! Here's your weekly report.")

    if st.session_state.get('is_pro_user', False):
        st.subheader("Your Personalized Weekly Report")
        st.write("*(This section will display a summary of your week's workouts, meals, habits, and overall progress, along with AI-generated tips.)*")
        st.write("---")
        st.subheader("Key Insights:")
        st.write("- **Workout Performance:** Analysis of your strength gains, consistency.")
        st.write("- **Nutrition Habits:** Overview of your macro intake, meal consistency.")
        st.write("- **Habit Tracking:** Trends in your water, sleep, steps, and mood.")
        st.write("- **Personalized Tips:** Suggestions for improvement based on your data (e.g., 'Increase protein intake on rest days', 'Aim for 30 more minutes of sleep').")

        st.download_button(
            label="Download Weekly Report as PDF",
            data="This will be your weekly report PDF content", # Replace with actual PDF generation
            file_name="weekly_report.pdf",
            mime="application/pdf",
            help="Download your detailed weekly progress report."
        )
    else:
        st.warning("Weekly personalized reports are a **Pro Tier** feature. Upgrade to unlock!")
else:
    st.warning("Please set up your profile on the Home page to use the Weekly Summary.")