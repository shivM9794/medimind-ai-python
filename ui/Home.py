
import os

import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000/api",
)

st.set_page_config(
    page_title="MediMind AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f9ff 0%, #f8fbfa 100%);
    }
    [data-testid="stSidebar"] {
        background-color: #102a43;
    }
    [data-testid="stSidebar"] * {
        color: white;
    }
    .hero {
        padding: 24px;
        border-radius: 18px;
        background: linear-gradient(110deg, #0f766e, #2563eb);
        color: white;
        margin-bottom: 20px;
    }
    .hero h1 { color: white; margin-bottom: 5px; }
    .muted { color: #64748b; }
    </style>
    """,
    unsafe_allow_html=True,
)


def api_get(path: str):
    try:
        response = requests.get(
            f"{API_BASE_URL}{path}",
            timeout=5,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def api_post(path: str, **kwargs):
    try:
        response = requests.post(
            f"{API_BASE_URL}{path}",
            timeout=60,
            **kwargs,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(
            "Could not reach the backend. Start FastAPI and try again."
        )
        return None


with st.sidebar:
    st.title("🩺 MediMind AI")
    st.caption("Your healthcare companion")
    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Assistant",
            "Medical Records",
            "Appointments",
            "Care Plans",
            "Privacy & Safety",
        ],
    )
    st.divider()
    st.caption("Demo application · Not for emergency use")


if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <h1>Your health, more organized.</h1>
            <p>Explore your health information and prepare for care.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dashboard = api_get("/dashboard")

    if dashboard:
        st.subheader(f"Welcome, {dashboard['patient_name']}")
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Upcoming appointments",
            dashboard["upcoming_appointments"],
        )
        col2.metric(
            "Active care plans",
            dashboard["active_care_plans"],
        )
        col3.metric(
            "Recent records",
            dashboard["recent_records"],
        )
    else:
        st.warning(
            "Dashboard data is unavailable. Is the FastAPI server running?"
        )

    st.subheader("Quick actions")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ask the AI assistant", use_container_width=True):
            st.session_state["selected_page"] = "AI Assistant"
            st.info("Choose AI Assistant in the sidebar.")

    with col2:
        if st.button("Upload a medical document", use_container_width=True):
            st.session_state["selected_page"] = "Medical Records"
            st.info("Choose Medical Records in the sidebar.")


elif page == "AI Assistant":
    st.title("AI Health Assistant")
    st.caption(
        "Ask general health-information questions. "
        "Avoid entering identifying patient information."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message.get("sources"):
                with st.expander("Sources"):
                    for source in message["sources"]:
                        st.markdown(f"**{source['title']}**")
                        st.caption(source["source"])
                        st.write(source["excerpt"])

    question = st.chat_input("Ask a general health question...")

    if question:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching available information..."):
                result = api_post(
                    "/chat",
                    json={"question": question},
                )

            if result:
                st.markdown(result["answer"])
                st.caption(result["disclaimer"])

                if result["sources"]:
                    with st.expander("Sources"):
                        for source in result["sources"]:
                            st.markdown(f"**{source['title']}**")
                            st.caption(source["source"])
                            st.write(source["excerpt"])

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            result["answer"]
                            + "\n\n*"
                            + result["disclaimer"]
                            + "*"
                        ),
                        "sources": result["sources"],
                    }
                )


elif page == "Medical Records":
    st.title("Medical Records")
    st.write(
        "Upload a PDF or text file to the local demo. "
        "Uploads are stored locally and are not yet indexed for AI search."
    )

    uploaded_file = st.file_uploader(
        "Choose a document",
        type=["pdf", "txt"],
    )

    if uploaded_file and st.button("Upload document"):
        result = api_post(
            "/documents",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                )
            },
        )

        if result:
            st.success(result["message"])


elif page == "Appointments":
    st.title("Appointments")
    st.info(
        "Appointment scheduling is a UI placeholder. "
        "Connect a secure backend and authorized scheduling system to enable it."
    )

    with st.form("appointment_form"):
        appointment_type = st.selectbox(
            "Appointment type",
            ["General consultation", "Follow-up", "Lab review"],
        )
        appointment_date = st.date_input("Preferred date")
        notes = st.text_area("Optional notes — do not include sensitive details")
        submitted = st.form_submit_button("Submit demo request")

    if submitted:
        st.success(
            f"Demo request prepared for {appointment_type} "
            f"on {appointment_date}. No booking was created."
        )


elif page == "Care Plans":
    st.title("Care Plans")
    st.info(
        "This section is a placeholder. Personal care plans should be "
        "created or approved by a qualified healthcare professional."
    )
    st.markdown(
        "- Review clinician-provided instructions\n"
        "- Keep follow-up appointments organized\n"
        "- Record questions to discuss with your care team"
    )


elif page == "Privacy & Safety":
    st.title("Privacy & Safety")
    st.markdown(
        """
        - Do not enter unnecessary personal or identifying health information.
        - This demo has no patient login or access-control system.
        - Uploaded files are saved locally and are not encrypted by this app.
        - Do not use real patient records in this development environment.
        - AI responses can be incorrect and must not replace professional care.
        - For a medical emergency, contact local emergency services.
        """
    )
