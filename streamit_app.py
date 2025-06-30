import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest 

st.set_page_config(page_title="A/B Testing Dashboard", layout="centered")

st.title("📊 Smart A/B Testing Platform")
st.markdown("Upload your A/B test CSV and get automated insights.")

uploaded_file = st.file_uploader(" Upload your A/B Test CSV", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)

    st.write("### Raw Data Preview")
    st.dataframe(data.head())

    # Optional filter: only for Kaggle ab_data.csv
    if 'landing_page' in data.columns and 'user_id' in data.columns:
        data = data.query(
            "(group == 'treatment' and landing_page == 'new_page') or (group == 'control' and landing_page == 'old_page')"
        ).drop_duplicates(subset='user_id')

    # Define 'converted' if not already there
    if 'converted' not in data.columns and '# of Purchase' in data.columns:
        data['converted'] = data['# of Purchase'].apply(lambda x: 1 if x >= 1 else 0)

    control = data[data['group'] == 'control']['converted']
    treatment = data[data['group'] == 'treatment']['converted']

    # Conversion rates
    p_control = control.mean()
    p_treatment = treatment.mean()
    diff = p_treatment - p_control

    # Z-test
    success = np.array([control.sum(), treatment.sum()])
    nobs = np.array([len(control), len(treatment)])
    z_score, p_value = proportions_ztest(success, nobs) 

    # Confidence Interval
    p_pool = (success[0] + success[1]) / (nobs[0] + nobs[1])
    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1/nobs[0] + 1/nobs[1]))
    margin = 1.96 * se_pool
    ci_lower = diff - margin
    ci_upper = diff + margin

    # Insight Generator
    def generate_ab_insight():
        if p_value < 0.05:
            return f"""
             **Statistically significant difference detected**

            Variant B shows an uplift of **{diff:.2%}** over control.  
            p-value = {p_value:.5f}, 95% CI = ({ci_lower:.2%}, {ci_upper:.2%})  
            **Recommendation:** Launch Variant B.
            """
        else:
            return f"""
             **No statistically significant difference detected**

            Uplift = **{diff:.2%}**  
            p-value = {p_value:.5f}, 95% CI = ({ci_lower:.2%}, {ci_upper:.2%})  
            **Recommendation:** Continue testing.
            """

    st.write("### Conversion Rates")
    st.metric("Control", f"{p_control:.2%}")
    st.metric("Treatment", f"{p_treatment:.2%}")
    st.metric("Uplift", f"{diff:.2%}")

    st.write("### Result")
    st.markdown(generate_ab_insight())

    # Optional: Chart
    st.write("### 🪄 Conversion Comparison")
    st.bar_chart(pd.DataFrame({
        "Control": [p_control],
        "Treatment": [p_treatment]
    }))


