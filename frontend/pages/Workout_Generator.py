import streamlit as st

st.set_page_config(
    page_title="Workout Generator",
    page_icon="🏋️",
)

st.title("🏋️ Workout Generator")
st.write("Generate personalized workout plans based on your goals.")

if st.session_state.get('user_profile'):
    st.write(f"Hello, {st.session_state['user_profile']['name']}! Let's create your workout.")

    # Inputs for workout generation
    goal = st.selectbox("Your Fitness Goal", ["Strength", "Endurance", "Weight Loss", "Muscle Gain", "Flexibility"])
    duration = st.slider("Workout Duration (minutes)", min_value=15, max_value=120, value=45, step=5)
    equipment = st.multiselect("Available Equipment", ["None", "Dumbbells", "Barbell", "Resistance Bands", "Gym Access"])

    generate_button = st.button("Generate Workout Plan")

    if generate_button:
        st.subheader("Generated Daily Plan:")
        # Here you would call your workout_logic.py (e.g., utils.workout_logic.generate_plan)
        # For now, let's put a placeholder
        st.info(f"Generating a {duration}-minute {goal} workout with {', '.join(equipment)}...")
        st.write("*(Workout plan details will appear here)*")

        st.download_button(
            label="Download Plan as PDF",
            data="This will be your PDF content", # Replace with actual PDF generation
            file_name="workout_plan.pdf",
            mime="application/pdf",
            disabled=not st.session_state.get('is_pro_user', False), # Only for Pro users
            help="Pro feature: Download your personalized workout plan as a PDF."
        )

        if not st.session_state.get('is_pro_user', False):
            st.warning("Downloadable PDFs are a Pro Tier feature. Upgrade to unlock!")
else:
    st.warning("Please set up your profile on the Home page to use the Workout Generator.")

# Example of how you might integrate backend logic
# from utils.workout_logic import generate_workout
# if generate_button:
#    plan = generate_workout(goal, duration, equipment, st.session_state['user_profile'])
#    st.write(plan)