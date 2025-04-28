
import streamlit as st
from fpdf import FPDF
import base64
from datetime import date

st.set_page_config(page_title="Propwealth Cashflow Calculator", layout="wide")

# Propwealth Header
st.markdown(
    "<h1 style='text-align: center; background: linear-gradient(to right, #8e2de2, #4a00e0);"
    "padding:10px; border-radius:10px; color:white;'>🏠 Propwealth Investment Calculator</h1>",
    unsafe_allow_html=True
)

today = date.today().strftime("%d/%m/%y")

# Full Stamp Duty Functions
def calculate_stamp_duty(state, price):
    if state == "VIC":
        if price <= 25000:
            return price * 0.014
        elif price <= 130000:
            return 350 + (price - 25000) * 0.024
        elif price <= 960000:
            return 2870 + (price - 130000) * 0.06
        else:
            return price * 0.055
    elif state == "NSW":
        if price <= 14000:
            return price * 0.0125
        elif price <= 320000:
            return 175 + (price - 14000) * 0.015
        elif price <= 1000000:
            return 9190 + (price - 320000) * 0.035
        elif price <= 3000000:
            return 40490 + (price - 1000000) * 0.045
        else:
            return 150490 + (price - 3000000) * 0.07
    elif state == "QLD":
        if price <= 5000:
            return price * 0.015
        elif price <= 75000:
            return 75 + (price - 5000) * 0.015
        elif price <= 540000:
            return 1050 + (price - 75000) * 0.035
        elif price <= 1000000:
            return 17325 + (price - 540000) * 0.045
        else:
            return 41825 + (price - 1000000) * 0.0475
    elif state == "WA":
        if price <= 120000:
            return 0
        elif price <= 150000:
            return (price - 120000) * 0.015
        elif price <= 360000:
            return 450 + (price - 150000) * 0.025
        elif price <= 725000:
            return 5450 + (price - 360000) * 0.035
        else:
            return 19150 + (price - 725000) * 0.045
    elif state == "SA":
        if price <= 120000:
            return price * 0.01
        elif price <= 300000:
            return 1200 + (price - 120000) * 0.02
        elif price <= 500000:
            return 4800 + (price - 300000) * 0.035
        else:
            return 11800 + (price - 500000) * 0.05
    elif state == "TAS":
        if price <= 3000:
            return price * 0.015
        elif price <= 25000:
            return 45 + (price - 3000) * 0.018
        elif price <= 75000:
            return 405 + (price - 25000) * 0.021
        elif price <= 200000:
            return 1455 + (price - 75000) * 0.024
        elif price <= 375000:
            return 4455 + (price - 200000) * 0.045
        else:
            return 12330 + (price - 375000) * 0.045
    elif state == "ACT":
        if price <= 200000:
            return price * 0.002
        elif price <= 300000:
            return 400 + (price - 200000) * 0.025
        elif price <= 500000:
            return 2900 + (price - 300000) * 0.035
        else:
            return 9900 + (price - 500000) * 0.045
    elif state == "NT":
        if price <= 525000:
            return price * 0.0495
        else:
            return (0.065 * price) - 15750
    else:
        return 0

# Property Address
st.header("Property Address")
address = st.text_input("Address", "41 Redwood Avenue Hampton Park VIC 3976")
state = st.selectbox("State", ["VIC", "NSW", "QLD", "WA", "SA", "TAS", "ACT", "NT"], index=0)

# Purchase Inputs
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

# Remaining parts (Rental, Expenses, Cashflow, PDF Generation) are similar to before...

st.info("Next steps: Would you like me to continue building the remaining Rental, Cashflow, and PDF generation sections to complete this full app?")
