
from pathlib import Path
import sqlite3
from statistics import mean

DB_PATH = Path(__file__).with_name("cardiotwin.db")


def connect_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize():
    with connect_db() as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                sex TEXT,
                hypertension TEXT,
                diabetes TEXT,
                smoking TEXT,
                family_history TEXT,
                medications TEXT,
                medical_history TEXT,
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        con.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER NOT NULL,
                recorded_at TEXT NOT NULL,
                heart_rate INTEGER NOT NULL,
                systolic_bp INTEGER NOT NULL,
                diastolic_bp INTEGER NOT NULL,
                spo2 REAL,
                steps INTEGER,
                sleep_hours REAL,
                activity_context TEXT,
                symptoms TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(id)
            )
        """)


def create_patient(data):
    with connect_db() as con:
        cursor = con.execute("""
            INSERT INTO patients (
                name, age, sex, hypertension, diabetes,
                smoking, family_history, medications,
                medical_history, notes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["name"], data["age"], data["sex"],
            data["hypertension"], data["diabetes"],
            data["smoking"], data["family_history"],
            data["medications"], data["medical_history"],
            data["notes"]
        ))
        return cursor.lastrowid


def list_patients():
    with connect_db() as con:
        rows = con.execute(
            "SELECT * FROM patients ORDER BY name"
        ).fetchall()
        return [dict(row) for row in rows]


def get_patient(patient_id):
    with connect_db() as con:
        row = con.execute(
            "SELECT * FROM patients WHERE id = ?",
            (patient_id,)
        ).fetchone()
        return dict(row) if row else None


def add_reading(patient_id, data):
    with connect_db() as con:
        con.execute("""
            INSERT INTO readings (
                patient_id, recorded_at, heart_rate,
                systolic_bp, diastolic_bp, spo2, steps,
                sleep_hours, activity_context, symptoms
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id, data["recorded_at"],
            data["heart_rate"], data["systolic_bp"],
            data["diastolic_bp"], data["spo2"],
            data["steps"], data["sleep_hours"],
            data["activity_context"], data["symptoms"]
        ))


def get_readings(patient_id):
    with connect_db() as con:
        rows = con.execute("""
            SELECT * FROM readings
            WHERE patient_id = ?
            ORDER BY recorded_at ASC, id ASC
        """, (patient_id,)).fetchall()
        return [dict(row) for row in rows]


def analyze_patient(patient, readings):
    result = {
        "reading_count": len(readings),
        "latest_hr": None,
        "average_hr": None,
        "minimum_hr": None,
        "maximum_hr": None,
        "latest_bp": None,
        "baseline_hr": None,
        "hr_change": None,
        "bp_alert": "No readings available",
        "hr_alert": "No readings available",
        "overall_status": "Awaiting measurements",
        "reasons": []
    }


    if not readings:
        return result

    latest = readings[-1]
    hr_values = [r["heart_rate"] for r in readings]
    bp_values = [
        (r["systolic_bp"], r["diastolic_bp"])
        for r in readings
    ]

    result["latest_hr"] = latest["heart_rate"]
    result["average_hr"] = round(mean(hr_values), 1)
    result["minimum_hr"] = min(hr_values)
    result["maximum_hr"] = max(hr_values)
    result["latest_bp"] = (
        latest["systolic_bp"], latest["diastolic_bp"]
    )

    # Analyze the latest three BP readings.
    recent_bp = bp_values[-3:]
    elevated_count = sum(
        1 for systolic, diastolic in recent_bp
        if systolic >= 140 or diastolic >= 90
    )

    if elevated_count >= 2 and len(recent_bp) >= 2:
        result["bp_alert"] = "Repeated elevated readings"
        result["reasons"].append(
            "At least two of the latest three readings "
            "have systolic BP >= 140 or diastolic BP >= 90."
        )
    elif elevated_count == 1:
        result["bp_alert"] = "Elevated reading observed"
        result["reasons"].append(
            "An elevated blood-pressure reading was recorded. "
            "Repeat under appropriate resting conditions."
        )
    else:
        result["bp_alert"] = "No repeated elevation detected"

    # Use resting readings only for the personal HR baseline.
    resting = [
        r for r in readings
        if r["activity_context"] == "Resting"
    ]

    if len(resting) >= 4:
        # Compare the latest resting reading with earlier readings.
        previous = resting[:-1]
        baseline_values = [
            r["heart_rate"] for r in previous[-10:]
        ]
        baseline = mean(baseline_values)
        result["baseline_hr"] = round(baseline, 1)

        last_resting = resting[-1]["heart_rate"]
        result["hr_change"] = round(
            last_resting - baseline, 1
        )

        # A configurable prototype flag, not a diagnosis.
        if last_resting > 100:
            result["hr_alert"] = (
                "High resting HR reading — review"
            )
            result["reasons"].append(
                "The latest recorded resting heart rate exceeds "
                "100 BPM. Context and symptoms matter."
            )
        elif (
            baseline > 0
            and last_resting >= baseline * 1.20
            and last_resting - baseline >= 15
        ):
            result["hr_alert"] = (
                "Above personal baseline"
            )
            result["reasons"].append(
                "The latest resting HR is at least 20% and "
                "15 BPM above the earlier personal baseline."
            )
        else:
            result["hr_alert"] = (
                "No configured HR deviation detected"
            )
    else:
        result["hr_alert"] = (
            "Need at least four resting readings for baseline"
        )

    if elevated_count >= 2 or any(
        "review" in result["hr_alert"].lower()
        or "above personal baseline" in result["hr_alert"].lower()
        for _ in [1]
    ):
        result["overall_status"] = "Review recommended"
    else:
        result["overall_status"] = "Monitoring"

    return result
def delete_patient(patient_id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM readings WHERE patient_id = ?",
            (patient_id,)
        )

        con.execute(
            "DELETE FROM patients WHERE id = ?",
            (patient_id,)
        )

def delete_patient_readings(patient_id):
    with connect_db() as con:
        con.execute(
            "DELETE FROM readings WHERE patient_id = ?",
            (patient_id,)
        )


def delete_reading(patient_id, reading_id):
    with connect_db() as con:
        con.execute(
            """
            DELETE FROM readings
            WHERE id = ? AND patient_id = ?
            """,
            (reading_id, patient_id)
        )