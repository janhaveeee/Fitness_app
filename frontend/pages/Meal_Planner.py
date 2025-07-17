import streamlit as st

st.set_page_config(
    page_title="Meal Planner",
    page_icon="🥗",
)

st.title("🥗 Meal Planner")
st.write("Plan your meals and track calories/macros.")

if st.session_state.get('user_profile'):
    st.write(f"Hello, {st.session_state['user_profile']['name']}! Let's plan your meals.")

    meal_option = st.radio("Choose an option:", ("Enter Meals Manually", "Auto-Generate Meals (Pro)"))

    if meal_option == "Enter Meals Manually":
        st.subheader("Manual Meal Entry")
        with st.form("manual_meal_form"):
            meal_name = st.text_input("Meal Name (e.g., Breakfast)")
            food_items = st.text_area("Food Items (comma-separated, e.g., '2 eggs, 1 toast, 50g avocado')")
            submit_manual = st.form_submit_button("Add Meal")

            if submit_manual:
                st.success(f"Added: {meal_name} - {food_items}. (Calorie/macro calculation would go here)")
                # Call a utility function to calculate macros from food_items
                st.write("*(Calories/Macros and tips will appear here)*")

    elif meal_option == "Auto-Generate Meals (Pro)":
        if st.session_state.get('is_pro_user', False):
            st.subheader("Auto-Generate Meals (Pro Feature)")
            dietary_pref = st.multiselect("Dietary Preferences", ["Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo"])
            num_days = st.slider("Number of Days to Plan For", min_value=1, max_value=7, value=1)
            generate_auto = st.button("Generate Meal Plan")

            if generate_auto:
                st.info(f"Generating {num_days}-day meal plan with {', '.join(dietary_pref)} preferences...")
                st.write("*(GPT-based meal plan with calories/macros will appear here)*")
                # Call your meal_api.py for generation
        else:
            st.warning("Auto-generating meals is a Pro Tier feature. Upgrade to unlock!")
            st.info("You can still use the 'Enter Meals Manually' option on the free tier.")
else:
    st.warning("Please set up your profile on the Home page to use the Meal Planner.")