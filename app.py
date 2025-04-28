
import streamlit as st
from fpdf import FPDF
import base64

st.set_page_config(page_title="Propwealth Cashflow Calculator", layout="wide")

st.markdown(
    "<h1 style='text-align: center; background: linear-gradient(to right, #0066ff, #33ccff);"
    "padding:10px; border-radius:10px; color:white;'>🏠 Propwealth Cashflow Calculator</h1>",
    unsafe_allow_html=True
)

st.header("1. Property Purchase Details")
address = st.text_input("Address", "1 Murtoa St Dallas")
purchase_price = st.number_input("Purchase Price", value=550000)
loan_amount = st.number_input("Loan Amount", value=440000)
loan_interest_rate = st.number_input("Loan Interest Rate (%)", value=6.0)
deposit = st.number_input("Deposit (20%)", value=110000)
stamp_duty = st.number_input("Estimated Stamp Duty", value=0)
lmi = st.number_input("Estimated LMI", value=0)
legals = st.number_input("Estimated Legals", value=2000)
reno_cost = st.number_input("Estimated Renovation Cost", value=0)

total_capital = deposit + stamp_duty + lmi + legals + reno_cost
st.success(f"💰 Total Capital Required: ${total_capital:,.2f}")

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

mgmt_fee_percent = st.number_input("Management Fee (%)", value=5.5)
mgmt_fees = ((low_rent + high_rent) / 2) * (mgmt_fee_percent / 100)

loan_repayments_weekly = ((loan_amount * (loan_interest_rate / 100)) / 12) / 4.33

landlord_insurance = st.number_input("Landlord Insurance ($/week)", value=9.62)

total_expenses = council + insurance + mgmt_fees + loan_repayments_weekly + landlord_insurance
st.warning(f"💸 Total Weekly Expenses: ${total_expenses:.2f}")

st.header("4. Estimated Cashflow")
cashflow_low_weekly = low_rent - total_expenses
cashflow_high_weekly = high_rent - total_expenses

cashflow_low_monthly = cashflow_low_weekly * 4.33
cashflow_high_monthly = cashflow_high_weekly * 4.33

cashflow_low_yearly = cashflow_low_weekly * 52
cashflow_high_yearly = cashflow_high_weekly * 52

col1, col2 = st.columns(2)
with col1:
    st.metric("Weekly Cashflow (Low Rent)", f"${cashflow_low_weekly:.2f}")
    st.metric("Monthly Cashflow (Low Rent)", f"${cashflow_low_monthly:.2f}")
    st.metric("Yearly Cashflow (Low Rent)", f"${cashflow_low_yearly:.2f}")
with col2:
    st.metric("Weekly Cashflow (High Rent)", f"${cashflow_high_weekly:.2f}")
    st.metric("Monthly Cashflow (High Rent)", f"${cashflow_high_monthly:.2f}")
    st.metric("Yearly Cashflow (High Rent)", f"${cashflow_high_yearly:.2f}")

st.header("5. Property Specs")
vacant_leased = st.text_input("Vacant / Leased", "Vacant")
bedrooms = st.number_input("Bedrooms", value=3)
bathrooms = st.number_input("Bathrooms", value=1)
garages = st.number_input("Lock-up Garage / Carport", value=2)
size = st.text_input("Size of Property", "588 sqm")
age = st.number_input("Age of Property", value=50)
construction_type = st.text_input("Construction Type", "Brick Veneer")
units_in_block = st.text_input("# Units in Block", "2")
work_needed = st.text_area("Work Needed", "")

# PDF Generator Section
st.header("📄 Download Report")
if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Propwealth Cashflow Report", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
    pdf.cell(200, 10, txt=f"Purchase Price: ${purchase_price:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Loan Amount: ${loan_amount:,.2f} @ {loan_interest_rate:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"Deposit: ${deposit:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Stamp Duty: ${stamp_duty:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Capital: ${total_capital:,.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Low Rent: ${low_rent}/week - Yield: {low_yield:.2f}%", ln=True)
    pdf.cell(200, 10, txt=f"High Rent: ${high_rent}/week - Yield: {high_yield:.2f}%", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Total Expenses: ${total_expenses:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Weekly Cashflow: ${cashflow_low_weekly:.2f} to ${cashflow_high_weekly:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Monthly Cashflow: ${cashflow_low_monthly:.2f} to ${cashflow_high_monthly:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Yearly Cashflow: ${cashflow_low_yearly:.2f} to ${cashflow_high_yearly:.2f}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Specs: {bedrooms} Bed / {bathrooms} Bath / {garages} Garage", ln=True)
    pdf.cell(200, 10, txt=f"Size: {size}, Age: {age} years, Type: {construction_type}", ln=True)
    if work_needed.strip():
        pdf.multi_cell(0, 10, txt=f"Work Needed: {work_needed}")

    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Propwealth_Cashflow_Report.pdf">📥 Download your PDF Report</a>'
    st.markdown(href, unsafe_allow_html=True)
