
import pandas as pd
from pathlib import Path

# Load the synthetic wearable data
folder = Path(__file__).parent
file_path = folder / "synthetic_wearable_data.csv"

df = pd.read_csv(file_path)

# Convert timestamps and clean data
df["recorded_at"] = pd.to_datetime(df["recorded_at"])
df = df.sort_values("recorded_at")

df["date"] = df["recorded_at"].dt.date

# Validate readings
df.loc[~df["heart_rate_bpm"].between(30, 220),
       "heart_rate_bpm"] = None

df.loc[~df["spo2_percent"].between(50, 100),
       "spo2_percent"] = None

# Overall summary
print("\n===== CARDIOTWIN DEMO ANALYSIS =====")
print("DATA SOURCE: SYNTHETIC - NOT REAL PATIENT DATA")

print("\nTotal readings:", len(df))
print("Average heart rate:",
      round(df["heart_rate_bpm"].mean(), 1), "BPM")
print("Minimum heart rate:",
      df["heart_rate_bpm"].min(), "BPM")
print("Maximum heart rate:",
      df["heart_rate_bpm"].max(), "BPM")
print("Average SpO2:",
      round(df["spo2_percent"].mean(), 1), "%")

# Daily pattern
daily = df.groupby("date").agg(
    average_hr=("heart_rate_bpm", "mean"),
    maximum_hr=("heart_rate_bpm", "max"),
    average_spo2=("spo2_percent", "mean"),
    total_steps=("steps_interval", "sum"),
    average_resting_hr=("resting_heart_rate_bpm", "mean")
).round(1)

print("\n===== DAILY SUMMARY =====")
print(daily.to_string())

# Compare heart rate by activity
activity = df.groupby("activity_context")[
    "heart_rate_bpm"
].mean().round(1)

print("\n===== HEART RATE BY ACTIVITY =====")
print(activity.to_string())

# Find readings worth reviewing
print("\n===== DEMO FLAGS =====")

high_hr = df[df["heart_rate_bpm"] > 120]

if not high_hr.empty:
    print("Heart rate above 120 BPM:")
    print(high_hr[[
        "recorded_at", "heart_rate_bpm", "activity_context"
    ]].to_string(index=False))
else:
    print("No readings above the demo threshold.")

low_spo2 = df[df["spo2_percent"] < 95]

if not low_spo2.empty:
    print("\nSpO2 below 95%:")
    print(low_spo2[[
        "recorded_at", "spo2_percent"
    ]].to_string(index=False))
else:
    print("\nNo SpO2 readings below the demo threshold.")

print("\nAnalysis complete.")
