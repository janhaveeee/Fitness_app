import streamlit as st

st.set_page_config(
    page_title="Posture Analysis",
    page_icon="🎥",
)

st.title("🎥 Posture Analysis")
st.write("Upload an exercise video (e.g., squat) to get angle-based feedback on your form.")

if st.session_state.get('user_profile'):
    st.write(f"Hello, {st.session_state['user_profile']['name']}! Let's check your form.")

    if st.session_state.get('is_pro_user', False):
        uploaded_video = st.file_uploader("Upload your exercise video", type=["mp4", "mov", "avi"])

        if uploaded_video is not None:
            st.video(uploaded_video) # Display the uploaded video
            st.success("Video uploaded! Processing for form analysis...")

            # Here you would pass the video to your pose_analysis.py script
            # This would likely involve saving the video temporarily and then processing it.
            # from utils.pose_analysis import analyze_form
            # feedback = analyze_form(uploaded_video)
            # st.subheader("Form Feedback:")
            # st.write(feedback)
            st.write("*(Angle-based feedback and improvement tips will appear here after analysis)*")
        else:
            st.info("Please upload a video to get form feedback.")
    else:
        st.warning("Full video form feedback is a **Pro Tier** feature. Upgrade to unlock!")
else:
    st.warning("Please set up your profile on the Home page to use the Posture Analysis.")