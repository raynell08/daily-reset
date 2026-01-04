import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# ---------------- DATABASE ---------------- #
conn = sqlite3.connect("daily_reset.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS mood_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    energy INTEGER,
    stress INTEGER,
    word TEXT,
    timestamp TEXT
)
""")
conn.commit()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Daily Reset",
    page_icon="🌿",
    layout="centered"
)

# ---------------- HEADER ---------------- #
st.markdown(
    """
    <h1 style='text-align: center;'>🌿 Daily Reset</h1>
    <p style='text-align: center; color: gray;'>
    A gentle daily mental reset
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------------- INPUTS ---------------- #
energy = st.slider("🔋 Energy level", 1, 5, 3)
stress = st.slider("🧠 Stress level", 1, 5, 3)
word = st.text_input("📝 One word for today")

# ---------------- ACTION BUTTON ---------------- #
if st.button("Unload Your Mind ✨"):

    timestamp = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO mood_logs (energy, stress, word, timestamp) VALUES (?, ?, ?, ?)",
        (energy, stress, word, timestamp)
    )
    conn.commit()

    if stress >= 4:
        action = "Take 3 slow breaths 🌿"
    elif energy <= 2:
        action = "Drink some water 💧"
    else:
        action = "Write one small task ✍️"

    st.success("Check-in saved")
    st.markdown(
        f"<h3 style='text-align: center;'>{action}</h3>",
        unsafe_allow_html=True
    )

    st.progress(100)

# ---------------- HISTORY ---------------- #
st.divider()
if st.checkbox("📊 View last 7 days"):
    cursor.execute(
        "SELECT energy, stress, word, timestamp FROM mood_logs ORDER BY id DESC LIMIT 7"
    )
    rows = cursor.fetchall()

    df = pd.DataFrame(
        rows,
        columns=["Energy", "Stress", "Word", "Timestamp"]
    )

    st.dataframe(df, use_container_width=True)

# ---------------- FOOTER ---------------- #
st.divider()
st.markdown(
    """
    <p style='text-align: center; color: gray; font-size: 12px;'>
    Created with 💙 by <b>Raynell Rebello</b>
    </p>
    """,
    unsafe_allow_html=True
)
