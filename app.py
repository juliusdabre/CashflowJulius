
import streamlit as st

st.set_page_config(page_title="Propwealth Cashflow Calculator", layout="wide")

st.title("🏠 Propwealth Cashflow Calculator")

st.header("1. Property Purchase Details")
address = st.text_input("Address", "1 Murtoa St Dallas")
purchase_price = st.number_input("Purchase Price", value=550000)
loan_amount = st.number_input("Loan Amount (6% Interest)", value=440000)
deposit = st.number_input("Deposit (20%)", value=110000)
stamp_duty = st.number_input("Estimated Stamp Duty", value=0)
lmi = st.number_input("Estimated LMI", value=0)
legals = st.number_input("Estimated Legals", value=2000)
reno_cost = st.number_input("Estimated Renovation Cost", value=0)

total_capital = deposit + stamp_duty + lmi + legals + reno_cost
st.success(f"Total Capital Required: ${total_capital:,.2f}")

st.header("2. Rental Yield & Income")
col1, col2 = st.columns(2)
with col1:
    low_rent = st.number_input("Low Rent ($/week)", value=350)
    low_yield = (low_rent * 52 / purchase_price) * 100
    st.metric("Yield on Purchase (Low Rent)", f"{low_yield:.2f}%")
with col2:
    high_rent = st.number_input("High Rent ($/week)", value=370)
    high_yield = (high_rent * 52 / purchase_price) * 100
    st.metric("Yield on Purchase (High Rent)", f"{high_yield:.2f}%")

st.header("3. Estimated Expenses")
council = st.number_input("Council Fees ($/week)", value=38.46)
insurance = st.number_input("Insurance ($/week)", value=19.23)
mgmt_fees = st.number_input("Management Fees (5.5%) ($/week)", value=19.25)
repayments = st.number_input("Repayments (6%) ($/week)", value=507.69)
landlord_insurance = st.number_input("Landlord Insurance ($/week)", value=9.62)

total_expenses = council + insurance + mgmt_fees + repayments + landlord_insurance
st.warning(f"Total Weekly Expenses: ${total_expenses:.2f}")

st.header("4. Estimated Cashflow Before Tax")
cashflow_low = low_rent - total_expenses
cashflow_high = high_rent - total_expenses
col1, col2 = st.columns(2)
with col1:
    st.metric("Weekly Cashflow (Low Rent)", f"${cashflow_low:.2f}", delta_color="inverse")
with col2:
    st.metric("Weekly Cashflow (High Rent)", f"${cashflow_high:.2f}", delta_color="inverse")

st.header("5. Property Specs")
st.text_input("Vacant / Leased", "Vacant")
st.number_input("Bedrooms", value=3)
st.number_input("Bathrooms", value=1)
st.number_input("Lock-up Garage / Carport", value=2)
st.text_input("Size of Property", "588 sqm")
st.number_input("Age of Property", value=50)
st.text_input("Construction Type", "Brick Veneer")
st.text_input("# Units in Block", "2")
st.text_area("Work Needed", "")
st.number_input("Estimated Renovation Cost (again)", value=0)
