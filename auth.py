import os
import streamlit as st
from supabase_client import get_supabase


def _base_url() -> str:
    """Return the app's public URL for OAuth redirects."""
    return os.environ.get("APP_URL", "https://bypeppy.streamlit.app")


def show_login_page() -> None:
    """Render the login/signup screen. Blocks the rest of the app until signed in."""
    st.set_page_config(page_title="myPeppy — Sign in", layout="centered")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🤖 Hi, I am Peppy, your AI emotional support. How can I help you today?")
        st.markdown("Sign in to save your chats, memories, and mood progress.")
        st.divider()

        # ── OAuth providers ────────────────────────────────────────────────
        supabase = get_supabase()
        redirect = f"{_base_url()}/"

        col_g, col_gh, col_fb = st.columns(3)

        with col_g:
            if st.button("🔵 Google", use_container_width=True):
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "google",
                    "options": {"redirect_to": redirect},
                })
                st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">',
                            unsafe_allow_html=True)

        with col_gh:
            if st.button("⚫ GitHub", use_container_width=True):
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "github",
                    "options": {"redirect_to": redirect},
                })
                st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">',
                            unsafe_allow_html=True)

        with col_fb:
            if st.button("🔷 Facebook", use_container_width=True):
                res = supabase.auth.sign_in_with_oauth({
                    "provider": "facebook",
                    "options": {"redirect_to": redirect},
                })
                st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">',
                            unsafe_allow_html=True)

        st.divider()

        # ── Email / password fallback ──────────────────────────────────────
        st.markdown("**Or use email**")
        mode = st.radio("", ["Sign in", "Create account"], horizontal=True, label_visibility="collapsed")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if mode == "Sign in":
            if st.button("Sign in", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = res.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Sign-in failed: {e}")
        else:
            if st.button("Create account", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": email, "password": password})
                    st.success("Account created! Check your email to confirm, then sign in.")
                except Exception as e:
                    st.error(f"Sign-up failed: {e}")


def get_current_user():
    """
    Return the logged-in user object, or None.
    Checks session_state first, then tries to restore from Supabase session.
    """
    if "user" in st.session_state and st.session_state["user"]:
        return st.session_state["user"]

    try:
        supabase = get_supabase()
        session = supabase.auth.get_session()
        if session and session.user:
            st.session_state["user"] = session.user
            return session.user
    except Exception:
        pass

    return None


def sign_out() -> None:
    try:
        get_supabase().auth.sign_out()
    except Exception:
        pass
    st.session_state.clear()
    st.rerun()
