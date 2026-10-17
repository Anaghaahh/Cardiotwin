
import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="CardioTwin Wearable Demo",
    page_icon="❤️",
    layout="wide"
)

st.title("CardioTwin - Wearable Monitoring")
st.warning(
    "DEMO MODE: All readings are synthetic and are not real patient data."
)

# Load data
file_path = Path(__file__).parent / "synthetic_wearable_data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("synthetic_wearable_data.csv was not found.")
    st.stop()

df["recorded_at"] = pd.to_datetime(df["recorded_at"])
df = df.sort_values("recorded_at")
df["date"] = df["recorded_at"].dt.date

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Heart Rate",
    f"{df['heart_rate_bpm'].mean():.1f} BPM"
)

col2.metric(
    "Maximum Heart Rate",
    f"{df['heart_rate_bpm'].max():.0f} BPM"
)

col3.metric(
    "Average SpO2",
    f"{df['spo2_percent'].mean():.1f}%"
)

col4.metric(
    "Total Steps",
    f"{df['steps_interval'].sum():,}"
)

# Heart rate over time
st.subheader("1. Heart Rate Trend")

fig_hr = px.line(
    df,
    x="recorded_at",
    y="heart_rate_bpm",
    color="activity_context",
    markers=True,
    labels={
        "recorded_at": "Time",
        "heart_rate_bpm": "Heart Rate (BPM)",
        "activity_context": "Activity"
    }
)

fig_hr.update_layout(legend_title_text="Activity")
st.plotly_chart(fig_hr, use_container_width=True)

# SpO2 trend
st.subheader("2. Blood Oxygen (SpO2)")

spo2_df = df.dropna(subset=["spo2_percent"])

if not spo2_df.empty:
    fig_spo2 = px.line(
        spo2_df,
        x="recorded_at",
        y="spo2_percent",
        markers=True,
        labels={
            "recorded_at": "Time",
            "spo2_percent": "SpO2 (%)"
        }
    )
    st.plotly_chart(fig_spo2, use_container_width=True)
else:
    st.info("No SpO2 readings available.")

# Average HR by activity
st.subheader("3. Heart Rate by Activity")

activity_df = df.groupby(
    "activity_context", as_index=False
)["heart_rate_bpm"].mean()

activity_df["heart_rate_bpm"] = activity_df[
    "heart_rate_bpm"
].round(1)

fig_activity = px.bar(
    activity_df,
    x="activity_context",
    y="heart_rate_bpm",
    labels={
        "activity_context": "Activity",
        "heart_rate_bpm": "Average Heart Rate (BPM)"
    },
    text="heart_rate_bpm"
)

st.plotly_chart(fig_activity, use_container_width=True)

# Daily steps
st.subheader("4. Daily Step Pattern")

daily_df = df.groupby(
    "date", as_index=False
)["steps_interval"].sum()

fig_steps = px.bar(
    daily_df,
    x="date",
    y="steps_interval",
    labels={
        "date": "Date",
        "steps_interval": "Total Steps"
    },
    text="steps_interval"
)

st.plotly_chart(fig_steps, use_container_width=True)

# Readings table
st.subheader("5. Recorded Data")

st.dataframe(
    df.drop(columns=["date"]),
    use_container_width=True,
    hide_index=True
)

# Demo flags
st.subheader("6. Readings to Review")

high_hr = df[df["heart_rate_bpm"] > 120]

if not high_hr.empty:
    st.write("**Heart rate above the demo threshold of 120 BPM**")
    st.dataframe(
        high_hr[[
            "recorded_at",
            "heart_rate_bpm",
            "activity_context"
        ]],
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("No readings crossed the demo threshold.")

st.caption(
    "Synthetic data only. Threshold flags are for software testing, "
    "not medical diagnosis."
)
