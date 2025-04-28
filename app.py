import streamlit as st
from fpdf import FPDF
import base64
from datetime import date

st.set_page_config(page_title="Cashflow Calculator", layout="wide")

# Propwealth Header
st.markdown(
    "<h1 style='text-align: center; background: linear-gradient(to right, #8e2de2, #4a00e0);"
    "padding:10px; border-radius:10px; color:white;'> Investment Calculator</h1>",
    unsafe_allow_html=True
)

today = date.today().strftime("%d/%m/%y")

# Stamp Duty Function
def calculate_stamp_duty(state, price):
    # your stamp duty function as before (no change)
    ...

# Property Details
st.header("Property Address")
address = st.text_input("Address", "41 Redwood Avenue Hampton Park VIC 3976")
state = st.selectbox("State", ["VIC", "NSW", "QLD", "WA", "SA", "TAS", "ACT", "NT"], index=0)

st.header("1️⃣ Purchase Costs")
expected_price = st.number_input("Expected Purchase Price ($)", value=765000)
auto_stamp_duty = calculate_stamp_duty(state, expected_price)
stamp_override = st.checkbox("Override Stamp Duty?")
if stamp_override:
    stamp_duty = st.number_input("Manual Stamp Duty ($)", value=auto_stamp_duty)
else:
    stamp_duty = auto_stamp_duty
    st.success(f"Auto Calculated Stamp Duty: ${stamp_duty:,.2f}")

deposit_percent = st.number_input("Deposit %", value=20.0)
loan_lvr = 80
loan_amount = expected_price * loan_lvr / 100
deposit_amount = expected_price * deposit_percent / 100
mortgage_fees = st.number_input("Mortgage/Transfer Fees ($)", value=1995.40)
legal_fees = st.number_input("Legal Fees ($)", value=1320)
pest_building = st.number_input("Pest & Building Report ($)", value=550)
buyers_agency_fee = st.number_input("Buyers Agency Fee ($)", value=12200)
reno_cost = st.number_input("Estimated Renovation ($)", value=0)

total_funds = deposit_amount + stamp_duty + mortgage_fees + legal_fees + pest_building + buyers_agency_fee + reno_cost

st.header("2️⃣ Rental & Yield")
lower_rent = st.number_input("Lower Rent ($/week)", value=620)
higher_rent = st.number_input("Higher Rent ($/week)", value=630)

low_yield = (lower_rent * 52 / expected_price) * 100
high_yield = (higher_rent * 52 / expected_price) * 100

st.header("3️⃣ Expenses")
council_fees = st.number_input("Council Fees ($/week)", value=57.69)
strata_fees = st.number_input("Strata Fees ($/week)", value=0)
insurance = st.number_input("Building Insurance ($/week)", value=0)
landlord_insurance = st.number_input("Landlord Insurance ($/week)", value=38.46)
other_expenses = st.number_input("Other Expenses ($/week)", value=9.62)

property_mgmt_percent = st.number_input("Property Management Fee (%)", value=5.5)
property_mgmt_fees = (lower_rent * property_mgmt_percent / 100)

loan_interest_rate = st.number_input("Loan Repayment Interest Only Rate (%)", value=6.5)
loan_repayment_io = ((loan_amount * (loan_interest_rate/100))/12)/4.33

total_weekly_expenses = council_fees + strata_fees + insurance + landlord_insurance + other_expenses + property_mgmt_fees + loan_repayment_io

st.header("4️⃣ Cashflow Calculation")

# ✅ Cashflow Calculation
weekly_cashflow_low = lower_rent - total_weekly_expenses
weekly_cashflow_high = higher_rent - total_weekly_expenses

monthly_cashflow_low = weekly_cashflow_low * 4.33
monthly_cashflow_high = weekly_cashflow_high * 4.33

annual_cashflow_low = weekly_cashflow_low * 52
annual_cashflow_high = weekly_cashflow_high * 52

# 🟰 Show the Live Cashflow Before Tax
st.success(f"📈 Weekly Cashflow (Low Rent): ${weekly_cashflow_low:.2f} | High Rent: ${weekly_cashflow_high:.2f}")
st.success(f"📈 Monthly Cashflow (Low Rent): ${monthly_cashflow_low:.2f} | High Rent: ${monthly_cashflow_high:.2f}")
st.success(f"📈 Annual Cashflow (Low Rent): ${annual_cashflow_low:.2f} | High Rent: ${annual_cashflow_high:.2f}")

st.header("5️⃣ Post-Tax Cashflow Estimate")
tax_bracket = st.number_input("Your Tax Bracket (%)", value=42.0)

after_tax_annual_low = annual_cashflow_low * (1 - tax_bracket/100)
after_tax_annual_high = annual_cashflow_high * (1 - tax_bracket/100)

after_tax_weekly_low = after_tax_annual_low / 52
after_tax_weekly_high = after_tax_annual_high / 52

# 🟰 Show the Live Post-Tax Cashflow
st.info(f"🧾 Weekly Post-Tax Cashflow (Low Rent): ${after_tax_weekly_low:.2f} | High Rent: ${after_tax_weekly_high:.2f}")
st.info(f"🧾 Annual Post-Tax Cashflow (Low Rent): ${after_tax_annual_low:.2f} | High Rent: ${after_tax_annual_high:.2f}")

# PDF Export
st.header("📄 Download Investment Report")
if st.button("Generate PDF Report"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    pdf.cell(200, 10, txt="Property Investment Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Date: {today}", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", "B", 11)
    pdf.cell(90, 10, "Purchase Costs", 0, 0, 'L')
    pdf.cell(90, 10, "Rental & Expenses", 0, 1, 'L')

    pdf.set_font("Arial", size=10)
    pdf.cell(90, 8, f"State: {state}", 0, 0)
    pdf.cell(90, 8, f"Low Rent: ${lower_rent} /wk", 0, 1)

    pdf.cell(90, 8, f"Purchase Price: ${expected_price:,.2f}", 0, 0)
    pdf.cell(90, 8, f"High Rent: ${higher_rent} /wk", 0, 1)

    pdf.cell(90, 8, f"Deposit: ${deposit_amount:,.2f}", 0, 0)
    pdf.cell(90, 8, f"Yield (Low): {low_yield:.2f}%", 0, 1)

    pdf.cell(90, 8, f"Stamp Duty: ${stamp_duty:,.2f}", 0, 0)
    pdf.cell(90, 8, f"Yield (High): {high_yield:.2f}%", 0, 1)

    pdf.cell(90, 8, f"Mortgage Fees: ${mortgage_fees:,.2f}", 0, 0)
    pdf.cell(90, 8, f"Weekly Expenses: ${total_weekly_expenses:.2f}", 0, 1)

    pdf.cell(90, 8, f"Legal Fees: ${legal_fees:,.2f}", 0, 0)
    pdf.cell(90, 8, f"Loan Rate: {loan_interest_rate:.2f}%", 0, 1)

    pdf.cell(90, 8, f"Total Funds: ${total_funds:,.2f}", 0, 1)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(200, 10, "Cashflow Before and After Tax", 0, 1, 'C')

    pdf.set_font("Arial", size=10)
    pdf.cell(100, 8, f"Before Tax (Low Rent): ${annual_cashflow_low:,.2f}", 0, 0)
    pdf.cell(100, 8, f"Before Tax (High Rent): ${annual_cashflow_high:,.2f}", 0, 1)

    pdf.cell(100, 8, f"After Tax (Low Rent): ${after_tax_annual_low:,.2f}", 0, 0)
    pdf.cell(100, 8, f"After Tax (High Rent): ${after_tax_annual_high:,.2f}", 0, 1)

    pdf_output = pdf.output(dest='S').encode('latin-1')
    b64 = base64.b64encode(pdf_output).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Propwealth_Cashflow_Report.pdf">📥 Download Full Investment Report (PDF)</a>'
    st.markdown(href, unsafe_allow_html=True)
