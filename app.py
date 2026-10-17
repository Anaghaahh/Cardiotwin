
from datetime import datetime

import pandas as pd
import plotly.express as px
import streamlit as st

import digital_twin as dt


st.set_page_config(
    page_title="CardioTwin | Patient Monitoring",
    page_icon="❤️",
    layout="wide"
)

dt.initialize()

st.title("CardioTwin")
st.caption(
    "Personalized cardiovascular digital twin | "
    "Patient history, longitudinal monitoring and early warnings"
)

st.warning(
    "Research prototype only. Not for clinical decision-making. "
    "Alerts are rule-based and are not validated predictions of "
    "heart attack, stroke or other cardiovascular events."
)


# --------------------------------------------------
# PATIENT REGISTRATION
# --------------------------------------------------

with st.expander("Register a new patient", expanded=False):
    with st.form("patient_registration"):
        st.subheader("Patient details")

        name = st.text_input("Patient name")
        age = st.number_input(
            "Age", min_value=18, max_value=120, value=40
        )
        sex = st.selectbox(
            "Sex", ["Not specified", "Female", "Male", "Other"]
        )

        st.markdown("**Medical and lifestyle history**")

        c1, c2 = st.columns(2)

        with c1:
            hypertension = st.selectbox(
                "Previously diagnosed hypertension?",
                ["No", "Yes", "Unknown"]
            )
            diabetes = st.selectbox(
                "Previously diagnosed diabetes?",
                ["No", "Yes", "Unknown"]
            )

        with c2:
            smoking = st.selectbox(
                "Smoking history",
                ["Never", "Current", "Former", "Unknown"]
            )
            family_history = st.selectbox(
                "Family history of cardiovascular disease",
                ["No", "Yes", "Unknown"]
            )

        medications = st.text_area(
            "Current medications",
            placeholder="Include name and dose if known"
        )

        medical_history = st.text_area(
            "Past medical history",
            placeholder="Previous diagnoses, procedures, etc."
        )

        notes = st.text_area(
            "Additional clinical notes",
            placeholder="Optional notes"
        )

        submitted = st.form_submit_button(
            "Register Patient", type="primary"
        )

        if submitted:
            if not name.strip():
                st.error("Please enter the patient's name.")
            else:
                patient_data = {
                    "name": name.strip(),
                    "age": int(age),
                    "sex": sex,
                    "hypertension": hypertension,
                    "diabetes": diabetes,
                    "smoking": smoking,
                    "family_history": family_history,
                    "medications": medications.strip(),
                    "medical_history": medical_history.strip(),
                    "notes": notes.strip()
                }

                dt.create_patient(patient_data)
                st.success("Patient registered successfully.")
                st.rerun()


# --------------------------------------------------
# PATIENT SELECTION
# --------------------------------------------------


patients = dt.list_patients()

if not patients:
    st.info(
        "Register your first patient above to open their "
        "digital twin dashboard."
    )
    st.stop()

st.sidebar.header("Patient Workspace")

patient_options = {
    f"{p['name']} (ID: {p['id']})": p["id"]
    for p in patients
}

selected_label = st.sidebar.selectbox(
    "Select patient",
    list(patient_options.keys())
)

patient_id = patient_options[selected_label]
patient = dt.get_patient(patient_id)

st.sidebar.markdown("---")
st.sidebar.subheader("Patient profile")
st.sidebar.write("**Name:**", patient["name"])
st.sidebar.write("**Age:**", patient["age"])
st.sidebar.write("**Hypertension:**", patient["hypertension"])
st.sidebar.write("**Diabetes:**", patient["diabetes"])
st.sidebar.write("**Smoking:**", patient["smoking"])
st.sidebar.write(
    "**Family history:**", patient["family_history"]
)

with st.sidebar.expander("Full medical history"):
    st.write("**Medications**")
    st.write(patient["medications"] or "Not provided")
    st.write("**Past medical history**")
    st.write(patient["medical_history"] or "Not provided")
    st.write("**Notes**")
    st.write(patient["notes"] or "Not provided")


# Clear readings while keeping the patient profile
with st.expander("Manage Patient Readings"):
    st.warning(
        f"This permanently deletes all readings for "
        f"{patient['name']}, but keeps their patient profile."
    )

    confirm_clear = st.checkbox(
        "I confirm that I want to delete all readings "
        "for this patient.",
        key=f"confirm_clear_{patient_id}"
    )

    if st.button(
        "Clear Patient Readings",
        key=f"clear_readings_{patient_id}"
    ):
        if confirm_clear:
            dt.delete_patient_readings(patient_id)
            st.success("Patient readings deleted.")
            st.rerun()
        else:
            st.warning("Please confirm deletion.")


# Delete the patient profile and all their readings
with st.expander("Delete Patient Record"):
    st.warning(
        f"This permanently deletes {patient['name']}'s "
        "profile and reading history."
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to permanently delete "
        "this patient and their history.",
        key=f"confirm_delete_{patient_id}"
    )

    if st.button(
        "Delete Patient",
        key=f"delete_patient_{patient_id}"
    ):
        if confirm_delete:
            dt.delete_patient(patient_id)
            st.success("Patient and history deleted.")
            st.rerun()
        else:
            st.warning("Please confirm deletion.")
# --------------------------------------------------
# ADD NEW MEASUREMENT
# --------------------------------------------------

st.header("Record a new measurement")
st.caption(
    "Enter a real measurement or a clearly identified test value. "
    "Wearable connection will be added separately."
)

with st.form("reading_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        heart_rate = st.number_input(
            "Heart rate (BPM)",
            min_value=30, max_value=220, value=75
        )
        systolic_bp = st.number_input(
            "Systolic BP (mmHg)",
            min_value=50, max_value=280, value=120
        )

    with c2:
        diastolic_bp = st.number_input(
            "Diastolic BP (mmHg)",
            min_value=30, max_value=180, value=80
        )
        spo2 = st.number_input(
            "Oxygen saturation (%)",
            min_value=50.0, max_value=100.0, value=98.0,
            step=0.5
        )

    with c3:
        steps = st.number_input(
            "Steps recorded",
            min_value=0, max_value=100000, value=0, step=100
        )
        sleep_hours = st.number_input(
            "Sleep in last 24 hours (hours)",
            min_value=0.0, max_value=24.0, value=7.0,
            step=0.5
        )

    activity_context = st.selectbox(
        "Measurement context",
        ["Resting", "After activity", "During activity", "Unknown"]
    )

    symptoms = st.text_input(
        "Symptoms or context",
        placeholder="e.g. no symptoms, dizziness, chest discomfort"
    )

    reading_submitted = st.form_submit_button(
        "Save Measurement", type="primary"
    )

    if reading_submitted:
        if diastolic_bp >= systolic_bp:
            st.error(
                "Please check the BP values: systolic should "
                "normally be higher than diastolic."
            )
        else:
            reading_data = {
                "recorded_at": datetime.now().isoformat(
                    timespec="seconds"
                ),
                "heart_rate": int(heart_rate),
                "systolic_bp": int(systolic_bp),
                "diastolic_bp": int(diastolic_bp),
                "spo2": float(spo2),
                "steps": int(steps),
                "sleep_hours": float(sleep_hours),
                "activity_context": activity_context,
                "symptoms": symptoms.strip()
            }

            dt.add_reading(patient_id, reading_data)
            st.success("Measurement saved to patient history.")
            st.rerun()


# --------------------------------------------------
# DIGITAL TWIN STATE
# --------------------------------------------------

readings = dt.get_readings(patient_id)
state = dt.analyze_patient(patient, readings)

st.header("Digital Twin Overview")

if not readings:
    st.info(
        "No measurements yet. Save a measurement above to "
        "initialize the patient's monitored state."
    )
else:
    latest = readings[-1]

    a, b, c, d = st.columns(4)

    a.metric(
        "Latest Heart Rate",
        f"{state['latest_hr']} BPM"
    )
    b.metric(
        "Latest Blood Pressure",
        f"{latest['systolic_bp']}/{latest['diastolic_bp']}"
    )
    c.metric(
        "Average Heart Rate",
        f"{state['average_hr']} BPM"
    )
    d.metric(
        "Measurements",
        state["reading_count"]
    )

    a, b, c = st.columns(3)

    a.metric(
        "Lowest Recorded HR",
        f"{state['minimum_hr']} BPM"
    )
    b.metric(
        "Highest Recorded HR",
        f"{state['maximum_hr']} BPM"
    )
    c.metric(
        "Personal Resting HR Baseline",
        f"{state['baseline_hr']} BPM"
        if state["baseline_hr"] is not None else "Building baseline"
    )

    st.subheader("Current Monitoring Status")

    if state["overall_status"] == "Review recommended":
        st.warning(state["overall_status"])
    else:
        st.success(state["overall_status"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Blood pressure pattern**")
        st.write(state["bp_alert"])

    with col2:
        st.markdown("**Resting heart-rate pattern**")
        st.write(state["hr_alert"])

    if state["reasons"]:
        st.markdown("**Reasons for review**")
        for reason in state["reasons"]:
            st.write("- " + reason)

    st.caption(
        "The configured thresholds are screening rules for this "
        "prototype, not diagnoses. A clinician must interpret "
        "readings in context."
    )


# --------------------------------------------------
# HISTORY CHARTS
# --------------------------------------------------

st.header("Longitudinal Patient History")

if readings:
    history = pd.DataFrame(readings)
    history["recorded_at"] = pd.to_datetime(
        history["recorded_at"]
    )

    fig_hr = px.line(
        history,
        x="recorded_at",
        y="heart_rate",
        markers=True,
        title="Heart Rate Over Time",
        labels={
            "recorded_at": "Measurement time",
            "heart_rate": "Heart rate (BPM)"
        }
    )
    fig_hr.update_layout(template="plotly_white", height=350)
    st.plotly_chart(fig_hr, use_container_width=True)

    fig_bp = px.line(
        history,
        x="recorded_at",
        y=["systolic_bp", "diastolic_bp"],
        markers=True,
        title="Blood Pressure Over Time",
        labels={
            "recorded_at": "Measurement time",
            "value": "Blood pressure (mmHg)",
            "variable": "Measurement"
        }
    )
    fig_bp.update_layout(template="plotly_white", height=350)
    st.plotly_chart(fig_bp, use_container_width=True)

    st.subheader("Recorded Measurements")

    display_history = history[
        [
            "recorded_at", "heart_rate",
            "systolic_bp", "diastolic_bp",
            "spo2", "steps", "sleep_hours",
            "activity_context", "symptoms"
        ]
    ].copy()

    st.dataframe(
        display_history.sort_values(
            "recorded_at", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )

    csv_data = history.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Patient History (CSV)",
        data=csv_data,
        file_name=f"cardiotwin_patient_{patient_id}.csv",
        mime="text/csv"
    )

else:
    st.info("The charts will appear after the first measurement.")


# --------------------------------------------------
# RESEARCH / SAFETY NOTES
# --------------------------------------------------

with st.expander("How this prototype works and its limitations"):
    st.markdown("""
    **Patient-specific state**
    - Stores the patient's profile and measurement history.
    - Computes descriptive heart-rate statistics.
    - Builds a resting heart-rate baseline from earlier resting readings.

    **Early-warning rules**
    - Checks the latest three blood-pressure readings for repeated
      elevated values using configurable prototype thresholds.
    - Flags selected resting heart-rate deviations from the personal
      baseline when enough readings are available.

    **Important limitations**
    - This version does not calculate a validated cardiovascular
      event probability or predict a heart attack or stroke.
    - The rules have not been clinically validated.
    - Measurements entered manually are not live wearable data.
    - Clinical decisions must not be made from this application.
    - Use de-identified or consented data for demonstrations.
    """)