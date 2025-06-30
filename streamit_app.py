import streamlit as st
import pandas as pd
import numpy as np
from statsmodels.stats.proportion import proportions_ztest 

st.set_page_config(page_title="Smart A/B Test Analyzer", layout="centered")

st.title("📊 Smart A/B Testing Platform")
st.caption("Upload A/B test CSV → Get automatic statistical insights & business recommendation")

# 📥 Sample CSV Download
with st.expander("📥 Download Sample CSV"):
    sample_df = pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6],
        "group": ["control", "control", "treatment", "treatment", "control", "treatment"],
        "landing_page": ["old_page", "old_page", "new_page", "new_page", "old_page", "new_page"],
        "converted": [0, 1, 1, 0, 0, 1]
    })
    st.download_button("Download Sample CSV", sample_df.to_csv(index=False), "sample_ab_data.csv")

# 📤 Upload File
uploaded_file = st.file_uploader("Upload your A/B test CSV file", type=["csv"])

# 💡 Insight Generator
def generate_ab_insight(p_c, p_t, p_val, ci_lo, ci_hi):
    uplift = p_t - p_c
    if p_val < 0.05:
        return f"""
✅ **Statistically significant difference detected**

Variant B (Treatment) shows an uplift of **{uplift:.2%}** over Control  
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
        df = pd.read_csv(uploaded_file)

        # ✅ Step 1: Basic column check (user_id, group, landing_page)
        required = {'user_id', 'group', 'landing_page'}
        if not required.issubset(df.columns):
            st.error("❌ CSV missing required columns: user_id, group, landing_page")
            st.stop()

        # ✅ Step 2: Handle missing 'converted' column
        if 'converted' not in df.columns:
            if '# of Purchase' in df.columns:
                df['converted'] = df['# of Purchase'].apply(lambda x: 1 if x >= 1 else 0)
            else:
                st.error("❌ CSV is missing both 'converted' and '# of Purchase' columns.")
                st.stop()

        # ✅ Step 3: Filter (for ab_data-style CSV)
        df = df.query(
            "(group == 'treatment' and landing_page == 'new_page') or (group == 'control' and landing_page == 'old_page')"
        ).drop_duplicates(subset='user_id')

        if df.empty:
            st.warning("⚠️ No valid records after filtering. Please check your data.")
        else:
            control = df[df['group'] == 'control']['converted']
            treatment = df[df['group'] == 'treatment']['converted']

            if len(control) < 10 or len(treatment) < 10:
                st.warning("⚠️ Fewer than 10 users per group. Consider adding more data.")

            # 🔢 Stats
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

            # 📋 Results
            st.subheader("🧪 Test Results")
            col1, col2, col3 = st.columns(3)
            col1.metric("Control", f"{p_c:.2%}")
            col2.metric("Treatment", f"{p_t:.2%}", delta=f"{uplift:.2%}")
            col3.metric("Sample Sizes", f"{nobs[0]} / {nobs[1]}")

            st.subheader("📋 Auto-Generated Insight")
            st.markdown(generate_ab_insight(p_c, p_t, p_val, ci_lo, ci_hi))

            st.subheader("📈 Conversion Comparison")
            st.bar_chart(pd.DataFrame({
                "Control": [p_c],
                "Treatment": [p_t]
            }))
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")



