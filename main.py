import streamlit as st
from auth import get_current_user, show_login_page, sign_out
from agents.conversation_agent import process_message
from memory.memory_db import retrieve_memory
from dashboard.views import show_dashboard

st.set_page_config(page_title="myPeppy", layout="wide")

# ── Auth gate — nothing renders until the user is signed in ───────────────────
user = get_current_user()

if not user:
    show_login_page()
    st.stop()

user_id = user.id
display_name = (user.user_metadata or {}).get("full_name") or user.email or "there"

# ── App shell ─────────────────────────────────────────────────────────────────
col_title, col_user = st.columns([5, 1])
with col_title:
    st.title("🤖 myPeppy")
with col_user:
    st.markdown(f"<div style='text-align:right;padding-top:14px'>👤 {display_name}</div>",
                unsafe_allow_html=True)
    if st.button("Sign out", use_container_width=True):
        sign_out()

tab1, tab2, tab3 = st.tabs(["🧠 Chat", "🗂 Memory", "📊 Dashboard"])


# ── CHAT ──────────────────────────────────────────────────────────────────────
with tab1:

    if "history" not in st.session_state:
        st.session_state.history = []

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(f"Talk to Peppy, {display_name.split()[0]}:")
        submitted = st.form_submit_button("Send", use_container_width=True)

    if submitted and user_input:
        with st.spinner("Peppy is thinking…"):
            response = process_message(user_input, user_id=user_id)
        st.session_state.history.append(("You", user_input))
        st.session_state.history.append(("Peppy", response))

    for speaker, message in reversed(st.session_state.history):
        if speaker == "You":
            st.write(f"**🧑 You:** {message}")
        else:
            st.write(f"**🤖 Peppy:** {message}")


# ── MEMORY ────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Your Stored Memories")
    query = st.text_input("Search your memories:")

    if query:
        try:
            results = retrieve_memory(query, user_id=user_id)
            if results:
                for mem in results:
                    st.write(f"• {mem}")
            else:
                st.info("No memories found for that query.")
        except Exception as e:
            st.error(f"Memory error: {e}")


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
with tab3:
    show_dashboard(user_id=user_id)
