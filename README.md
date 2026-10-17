# Cardiotwin
CardioTwin analyzes wearable data using Python and displays heart rate, SpO₂, and activity trends through an interactive dashboard. Future development includes real-time wearable integration.


 CardioTwin: A Personalized Cardiovascular Digital Twin

 1. Project Overview

CardioTwin is a healthcare digital twin prototype designed to support personalized cardiovascular health monitoring by combining individual health history with physiological and lifestyle data.

The platform visualizes health trends using available readings such as heart rate, blood pressure, physical activity, and sleep. Its goal is to help users understand changes in their health patterns and support preventive healthcare monitoring.

Project Status: Prototype

2. Team Details

- Team Member:Anagha S Kumar
- Department:Electronics and Communication Engineering (ECE)
- Year:Third Year
- Institution: Meenakshi Sundararajan Engineering College, Chennai, Tamil Nadu, India

3. Problem Statement

Cardiovascular health monitoring often relies on isolated measurements and periodic clinical assessments. These may not provide a convenient way to visualize an individual's changing health patterns over time.

CardioTwin addresses this challenge through a personalized digital representation that organizes health history, physiological readings, and lifestyle indicators into a unified monitoring dashboard.

4. Healthcare Use Case

CardioTwin is intended to support:

- Monitoring heart-rate and blood-pressure trends.
- Visualizing physical activity and sleep patterns.
- Combining available health readings with individual health history.
- Highlighting potentially concerning trends for further review.
- Supporting health awareness and preventive monitoring.

The platform is a prototype and is not intended to diagnose diseases or replace professional medical advice.

## 5. Proposed Solution

CardioTwin provides a dashboard where health information can be recorded, organized, visualized, and reviewed over time.

The system is designed to support:
- Patient profile management.
- Health-reading storage and retrieval.
- Historical trend visualization.
- Integration with wearable-derived data where supported.
- Future extensions for validated AI/ML-based risk estimation.

## 6. Technical Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Data processing | Pandas |
| Visualization | Plotly |
| Database | SQLite |
| Wearable data integration | Health Connect, where supported |
| Development environment | Visual Studio Code |

Update this list to match the technologies actually implemented in the submitted version.

 7. AI/ML Model Details

Describe the model used in the current implementation, including its framework, input features, training dataset, evaluation metrics, and limitations.

If the current prototype uses rule-based indicators or statistical analysis rather than a trained machine-learning model, state that clearly. Validated predictive modelling can be included as future work.

8. System Architecture

The proposed system workflow is:

Wearable Devices / Manual Health Inputs  
↓  
Health Data Collection  
↓  
Data Processing and Validation  
↓  
Database Storage  
↓  
Cardiovascular Digital Twin Dashboard  
↓  
Trend Visualization and Health Indicators


 Prerequisites

- Python 3.10 or a compatible version supported by the project's dependencies.
- pip package manager.

 Steps

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Open the project directory:

   `cd CardioTwin`

3. Install dependencies:

   `pip install -r requirements.txt`

4. Launch the application:

   `streamlit run app.py`

The application will open in your browser.

## 12. Repository Structure

```text
CardioTwin/
├── app.py
├── database.py
├── digital_twin.py
├── README.md
├──wearable_analysis.py
├──wearable_dashboard.py
└── synthetic_data.csv
```


 Results and Outcomes

Document the features successfully implemented and demonstrated, including:

- Patient registration and profile management.
- Recording and managing health readings.
- Visualizing health data and historical trends.
- Displaying available health indicators.
- Demonstrating the current prototype workflow.

Include screenshots, test results, or measured evaluation metrics where available. Do not report unverified performance improvements or predictive accuracy.

 Future Scope

- Integration with additional wearable devices.
- Automated synchronization of supported health data.
- Validated machine-learning models for cardiovascular risk estimation.
- Personalized trend analysis and alerting.
- Improved interoperability with healthcare systems.

Disclaimer

CardioTwin is a prototype developed for healthcare technology research and demonstration. Its outputs are intended for informational and educational purposes only. They are not a diagnosis, a substitute for clinical evaluation, or a replacement for professional medical advice.

Contact

**Anagha S Kumar**  
Third-Year Electronics and Communication Engineering  
Meenakshi Sundararajan Engineering College, Chennai, India
