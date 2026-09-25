import streamlit as st
from src.models.schemas import UserProfile
from src.engine.evaluator import EligibilityEvaluator

st.set_page_config(page_title="Benefit Bridge", page_icon="🌉", layout="centered")

st.title("🌉 Benefit Bridge")
st.markdown("""
Welcome to **Benefit Bridge**. This tool helps Singaporean seniors, caregivers, and social workers
identify eligible healthcare grants and benefits quickly.
""")

st.divider()

st.header("👤 Senior's Profile")
with st.form("user_profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=0, max_value=120, value=65)
        citizen_status = st.selectbox("Citizenship Status", ["Singaporean", "Permanent Resident", "Other"])
        monthly_income = st.number_input("Monthly Household Income ($)", min_value=0.0, value=1000.0, step=100.0)

    with col2:
        flat_type = st.selectbox("HDB Flat Type", ["1-room", "2-room", "3-room", "4-room", "5-room", "Executive", "Private", "Other"])
        dependents = st.number_input("Number of Dependents", min_value=0, value=0)

    submit_button = st.form_submit_button("Check Eligibility")

if submit_button:
    # 1. Create User Profile
    user = UserProfile(
        age=age,
        citizen_status=citizen_status,
        monthly_income=monthly_income,
        flat_type=flat_type,
        dependents_count=dependents
    )

    # 2. Evaluate Eligibility
    evaluator = EligibilityEvaluator("data/grants.yaml")
    results = evaluator.evaluate(user)

    # 3. Display Results
    st.divider()
    st.header("🚀 Eligibility Results")

    eligible_grants = [res for res in results if res[1]]
    ineligible_grants = [res for res in results if not res[1]]

    if eligible_grants:
        st.success(f"Found {len(eligible_grants)} eligible grant(s)!")
        for grant, _, reason in eligible_grants:
            with st.expander(f"✅ {grant.name}"):
                st.write(f"**Description:** {grant.description}")
                st.write(f"**Agency:** {grant.agency}")
                st.write(f"**Category:** {grant.category}")
                st.link_button("Apply Now", grant.application_url)
    else:
        st.warning("No eligible grants found based on the current profile.")

    if ineligible_grants:
        st.markdown("### 🔍 Other Potential Grants")
        for grant, _, reason in ineligible_grants:
            with st.expander(f"❌ {grant.name}"):
                st.write(f"**Reason for Ineligibility:** {reason}")
                st.write(f"**Description:** {grant.description}")
                st.link_button("View Details", grant.application_url)
