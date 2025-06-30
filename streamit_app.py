import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest

st.set_page_config(page_title="Smart A/B Test Analyzer", layout="centered")
st.title("📊 Smart A/B Testing Platform")
st.caption("Upload your A/B test CSV and get automated insights")

# 📥 Sample CSV Download
with st.expander("📥 Download Sample CSV (for testing)"):
    sample = pd.DataFrame({
        "Campaign Name": ["Test A", "Test B"],
        "Date": ["2024-01-01", "2024-01-02"],
        "group": ["control", "treatment"],
        "# of Purchase": [30, 45]
    })
    st.download_button("Download Sample CSV", sample.to_csv(index=False), "sample_ab_data.csv")

# 📤 Upload File
uploaded_file = st.file_uploader("📁 Upload your A/B Test CSV", type=["csv"])

# 💡 Insight Generator
def generate_ab_insight(p_c, p_t, p_val, ci_lo, ci_hi):
    uplift = p_t - p_c
    if p_val < 0.05:
        return f"""
✅ **Statistically significant difference detected**

Variant B shows an uplift of **{uplift:.2%}** over Control.  
p-value = {p_val:.5f}  
95% CI = ({ci_lo:.2%}, {ci_hi:.2%})  
**Recommendation:** Launch Variant B ✅
"""
    else:
        return f"""
⚠️ **No statistically significant difference detected**

Observed uplift = **{uplift:.2%}**  
p-value = {p_val:.5f}  
95% CI = ({ci_lo:.2%}, {ci_hi:.2%})  
**Recommendation:** Continue testing or collect more data.
"""

# 🧪 Main Logic
if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        st.subheader("📄 Raw Data Preview")
        st.dataframe(data.head())

        # Create converted column
        if 'converted' not in data.columns and '# of Purchase' in data.columns:
            data['converted'] = data['# of Purchase'].apply(lambda x: 1 if x >= 1 else 0)

        if 'group' not in data.columns or 'converted' not in data.columns:
            st.error("❌ Required columns missing: 'group' and '# of Purchase'")
            st.stop()

        # Split groups
        control = data[data['group'] == 'control']['converted']
        treatment = data[data['group'] == 'treatment']['converted']

        if len(control) < 10 or len(treatment) < 10:
            st.warning("⚠️ Fewer than 10 samples in control/treatment. Results may be unreliable.")

        # Stats
        p_c = control.mean()
        p_t = treatment.mean()
        uplift = p_t - p_c

        success = np.array([control.sum(), treatment.sum()])
        nobs = np.array([len(control), len(treatment)])
        z_score, p_val = proportions_ztest(success, nobs)

        p_pool = (success[0] + success[1]) / (nobs[0] + nobs[1])
        se = np.sqrt(p_pool * (1 - p_pool) * (1/nobs[0] + 1/nobs[1]))
        margin = 1.96 * se
        ci_lo = uplift - margin
        ci_hi = uplift + margin

        # Display Metrics
        st.subheader("📊 Key Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Control CR", f"{p_c:.2%}")
        col2.metric("Treatment CR", f"{p_t:.2%}", delta=f"{uplift:.2%}")
        col3.metric("Sample Sizes", f"{nobs[0]} / {nobs[1]}")

        st.subheader("📋 Auto Insight")
        st.markdown(generate_ab_insight(p_c, p_t, p_val, ci_lo, ci_hi))

        st.subheader("📈 Conversion Comparison")
        st.bar_chart(pd.DataFrame({
            "Control": [p_c],
            "Treatment": [p_t]
        }))

    except Exception as e:
        st.error(f"❌ Error while processing file: {e}")




