# Smart A/B Testing Automation Platform

A complete web-based platform to upload A/B test data, run automatic statistical analysis, and receive clear insights — all with a simple UI powered by Streamlit.

---

## Features

- Performs Two-Proportion Z-Test to detect statistical uplift  
- Calculates conversion rates, confidence intervals, and p-values  
- Auto-generates plain-English business recommendations  
- Visualizes uplift and conversion trends in a dashboard  
- Upload any CSV file with A/B group data  
- Built-in error handling and CSV validation  

---

## Tech Stack

`Streamlit` • `pandas` • `numpy` • `statsmodels` • `GitHub`

---

## Dataset Format

Upload a CSV file with the following columns:

```csv
Campaign Name, Date, group, # of Purchase
Test A, 2024-01-01, control, 30
Test B, 2024-01-02, treatment, 45

The platform will automatically create a converted column using this rule:
→ converted = 1 if # of Purchase >= 1, else 0

How It Works
Upload your A/B test CSV

The app checks for required columns (group, # of Purchase)

Runs Z-Test to compare conversion rates

Calculates:

Conversion rates

p-value

95% Confidence Interval

Displays:

Key metrics

Business recommendation

Conversion comparison bar chart

Example Output
Sample Conversion Rates:

Control: 22.00%

Treatment: 48.00%

Uplift: +26.00%

Auto Insight:

Statistically significant difference detected
Variant B shows an uplift of 26.00% over control
p-value = 0.00642, 95% CI = (7.30%, 44.70%)
Recommendation: Launch Variant B 

Live App
[Try the Live App](https://smart-ab-testing-platform-aakiwlrhbg3xhnkqhwmru8.streamlit.app/)
Includes Sample CSV download button

Project Structure

smart-ab-testing-platform/
│
├── streamit_app.py          # Final Streamlit dashboard code  
├── ab_data.csv              # Sample dataset  
├── requirements.txt         # Dependencies for Streamlit Cloud  
└── README.md                # Project overview (this file)

## Author
Built by Manoj Kumar
GitHub: https://github.com/manojkumar5666

## License

This project is licensed under the [MIT License](LICENSE.md).
