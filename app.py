import streamlit as st
from wellness_assistant import (
    analyze_mood,
    generate_fitness_plan,
    voice_guided_meditation,
    set_reminder,
    show_progress,
    query_gemma2,
    progress,
)

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="Wellness Assistant", page_icon="💬", layout="wide")
st.title("💬 Wellness Assistant Chatbot")
st.write("Your personal assistant for mood tracking, fitness, meditation, and reminders.")

# ----------------------------
# Session State (for chat history)
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# User Input
# ----------------------------
user_input = st.text_input("Type your message here 👇")

if st.button("Send") and user_input:
    # Route query to the correct backend function
    if "mood" in user_input.lower():
        reply = analyze_mood(user_input)

    elif "fitness" in user_input.lower():
        reply = generate_fitness_plan(user_input)

    elif "meditate" in user_input.lower():
        reply, audio_file = voice_guided_meditation()
        # Play meditation audio
        with open(audio_file, "rb") as f:
            st.audio(f.read(), format="audio/mp3")

    elif "remind" in user_input.lower():
        reply = set_reminder("Take medicine", "8 PM")

    elif "progress" in user_input.lower():
        # Show progress chart
        labels = ["Mood", "Fitness", "Meditation"]
        values = [
            len(progress["mood"]),
            len(progress["fitness"]),
            len(progress["meditation"]),
        ]
        st.bar_chart({"Activities": values})
        reply = "📊 Here’s your progress."

    else:
        reply = query_gemma2(user_input)

    # Save chat history
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", reply))

# ----------------------------
# Display Chat History
# ----------------------------
st.subheader("Chat History")
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**👤 {role}:** {msg}")
    else:
        st.markdown(f"**🤖 {role}:** {msg}")
