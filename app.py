import streamlit as st
import datetime
import os

# import cv2  # ❌ Commented for Streamlit Cloud compatibility

st.set_page_config(page_title="VIPERS Surveillance", layout="wide")

# ---------- UI Style ----------
st.markdown("""
    <style>
    .main { background-color: #0c1b2a; color: white; }
    .stButton>button { background-color: #1976d2; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color:#00FFCA'>🛡 VIPERS: Drone Video Surveillance System</h1>", unsafe_allow_html=True)

# Mode Toggle
mode = st.radio("🎛 Select Mode:", ["Live", "Playback"], horizontal=True)

# Logging setup
log_file = "logs/event_log.txt"
os.makedirs("logs", exist_ok=True)


def log_event(message):
    now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a") as f:
        f.write(f"{now} {message}\n")


# Layout
col1, col2 = st.columns([2, 1])
if "is_playing" not in st.session_state:
    st.session_state.is_playing = False

with col1:
    st.subheader(f"🎥 {mode} Mode")

    stframe = st.empty()

    if mode == "Playback":
        video_path = "assets/drone_footage.mp4"

        if os.path.exists(video_path):
            toggle = st.button("▶ Click to Play/Pause")
            if toggle:
                st.session_state.is_playing = not st.session_state.is_playing

            if st.session_state.is_playing:
                st.video(video_path)
            else:
                st.warning("⏸️ Video paused. Click above to resume.")
        else:
            st.error("⚠️ Video file not found.")

    elif mode == "Live":
        st.info("📡 Live mode is unavailable in deployed version (OpenCV not supported).")

    st.markdown("🔴 <i>Note: Detection disabled for cloud version. Logs can be manually added.</i>",
                unsafe_allow_html=True)

with col2:
    st.subheader("📅 Calendar")
    selected_date = st.date_input("Select a date", datetime.date.today())

    # Extract event dates from log
    event_dates = []
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            for line in f:
                if line.strip():
                    date_str = line[1:11]
                    try:
                        event_dates.append(datetime.datetime.strptime(date_str, "%Y-%m-%d").date())
                    except:
                        pass

    if selected_date in event_dates:
        st.success("✔ Detection recorded on this day!")
    else:
        st.warning("ℹ No activity recorded.")

    st.subheader("📄 Logs")
    with st.expander("📂 View Event Log"):
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                st.code(f.read())
        else:
            st.info("No logs available.")

    st.subheader("📡 Camera Status")
    st.success("Camera 01: ✅ Online")
    st.success("Camera 02: ✅ Online")

with st.expander("🚨 Live Alerts Panel"):
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
            if "detected" in last_line:
                st.error("⚠ Detection event recently logged!")
            else:
                st.info("✅ No current threats.")
    else:
        st.info("✅ System monitoring...")
