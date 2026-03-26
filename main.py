import streamlit as st
from agents.conversation_agent import process_message
from memory.memory_db import retrieve_memory
from dashboard.views import show_dashboard

st.set_page_config(page_title="AI Life Companion", layout="wide")
st.title("🤖 AI Life Companion")

tab1, tab2, tab3 = st.tabs(["🧠 Chat", "🗂 Memory", "📊 Dashboard"])


# ──────────────────────────────────────────────────────────────────────────────
# CHAT
# ──────────────────────────────────────────────────────────────────────────────
with tab1:

    if "history" not in st.session_state:
        st.session_state.history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Talk to your AI:")
        col_send, col_voice = st.columns([4, 1])

        with col_send:
            submitted = st.form_submit_button("Send", use_container_width=True)

        with col_voice:
            voice_clicked = st.form_submit_button("🎙 Voice", use_container_width=True)

    # Voice input — lazy-import so startup stays fast
    if voice_clicked:
        try:
            from agents.voice_agent import record_voice
            with st.spinner("Listening for 5 seconds…"):
                user_input = record_voice(seconds=5)
            st.info(f"Heard: {user_input}")
            submitted = True          # fall through to the normal send path
        except RuntimeError as e:
            st.error(f"Voice error: {e}")
            submitted = False

    if submitted and user_input:
        with st.spinner("Thinking…"):
            response = process_message(user_input)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Advisor", response))

    for speaker, message in reversed(st.session_state.history):
        if speaker == "You":
            st.write(f"**🧑 You:** {message}")
        else:
            st.write(f"**🤖 Advisor:** {message}")


# ──────────────────────────────────────────────────────────────────────────────
# MEMORY
# ──────────────────────────────────────────────────────────────────────────────
with tab2:

    st.subheader("Stored Memories")
    query = st.text_input("Search memories:")

    if query:
        try:
            results = retrieve_memory(query)
            if results:
                for mem in results:
                    st.write(f"• {mem}")
            else:
                st.info("No memories found for that query.")
        except Exception as e:
            st.error(f"Memory error: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    show_dashboard()