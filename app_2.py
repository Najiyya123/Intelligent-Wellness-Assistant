import streamlit as st
from wellness_assistant import (
    analyze_mood,
    generate_fitness_plan,
    voice_guided_meditation,
    set_reminder,
    show_progress,
    query_gemma2,
    progress,
    reminders,   # <- don’t forget to import reminders list
)

# ----------------------------
# Streamlit Page Setup
# ----------------------------
st.set_page_config(page_title="Wellness Assistant", page_icon="💬", layout="wide")
st.title("💬 Wellness Assistant Chatbot")

# Sidebar for info
st.sidebar.title("⚡ Wellness Assistant")
st.sidebar.write("Built for CodeFusion Hackathon 2025 🎉")
st.sidebar.success("Features: Mood, Fitness, Meditation, Reminders, Progress")

st.write("Your personal assistant for mood tracking, fitness, meditation, and reminders.")

# ----------------------------
# Session State (for chat history)
# ----------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ----------------------------
# Tabs for Features
# ----------------------------
tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Progress", "⏰ Reminders"])

# ----------------------------
# Chat Tab
# ----------------------------
with tab1:
    st.subheader("Chat with Assistant")

    user_input = st.text_input("Type your message here 👇", key="chat_input")

    if st.button("Send", key="chat_button") and user_input:
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

    # Display chat history
    st.subheader("Chat History")
    for role, msg in st.session_state.chat_history:
        if role == "You":
            st.markdown(f"👤 **{role}:** {msg}")
        else:
            st.markdown(f"🤖 **{role}:** {msg}")

# ----------------------------
# Progress Tab
# ----------------------------
with tab2:
    st.subheader("Your Progress Overview")
    st.metric("Mood Entries", len(progress["mood"]))
    st.metric("Fitness Plans", len(progress["fitness"]))
    st.metric("Meditations", len(progress["meditation"]))

    # Show chart
    st.bar_chart({
        "Mood": [len(progress["mood"])],
        "Fitness": [len(progress["fitness"])],
        "Meditation": [len(progress["meditation"])]
    })

# ----------------------------
# Reminders Tab
# ----------------------------
with tab3:
    st.subheader("Reminders")
    if len(reminders) > 0:
        for r in reminders:
            st.write(f"⏰ {r['text']} at {r['time']}")
    else:
        st.info("No reminders set yet. Use the chat to create one!")
