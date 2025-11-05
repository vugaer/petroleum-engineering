import streamlit as st
import math

# --- Page Title ---
st.title("Water Resistivity & Salinity Calculator")

# --- User Inputs ---
st.header("Input Data")

# SP and Reservoir Temperature in one row
col1, col2 = st.columns(2)
with col1:
    sp_log_reading = st.number_input('SP Log (mV)', value=0.0)
with col2:
    reservoir_temp = st.number_input('Reservoir Temp (°F)', value=150.0)

# Mud filtrate resistivity and its temperature in one row with units
col3, col4, col5, col6 = st.columns([2, 1, 2, 1])
with col3:
    r_mf_x = st.number_input('R_mf', value=0.1, format="%.3f")
with col4:
    st.write("Ω·m")  # Unit for resistivity
with col5:
    r_mf_x_temp = st.number_input('at Temp', value=75.0)
with col6:
    st.write("°F")  # Unit for temperature

# Electrolyte selection below
electrolyte = st.radio(
    "Select Electrolyte Type:",
    ("NaCl (Default)", "KCl"),
    horizontal=True
)


def r_convert_temp(r1, temp1, temp2=75):
  return float((r1 * (temp1+6.77))/(temp2+6.77))

r_mf_reservoir = r_convert_temp(r_mf_x, r_mf_x_temp, 75)

if r_mf_reservoir > 0.1: # at 75F
  r_mfe = 0.85*r_mf_reservoir
if r_mf_reservoir <= 0.1:
  r_mfe = (146*r_mf_reservoir-5)/(377*r_mf_reservoir+77)

r_mfe_reservoir = r_convert_temp(r_mfe, 75, 150)

ssp = sp_log_reading

# ✅ Use ONLY the selected equation for r_we
if electrolyte == "NaCl (Default)":
    r_we = r_mfe_reservoir * 10 ** (ssp / (61 + 0.133 * reservoir_temp))
else:  # KCl
    r_we = r_mfe_reservoir * 10 ** (-(22 - ssp) / (56 + 0.12 * reservoir_temp))

r_we_75 = r_convert_temp(r_we, 150, 75)

if r_we_75 > 0.12:
  r_w_75 = -(0.58-10**(0.69*r_we_75-0.24))
if r_we_75 <= 0.12:
  r_w_75 = (77*r_we_75+5)/(146-377*r_we_75)

r_w_reservoir = r_convert_temp(r_w_75, 75, 150)
salinity = 10 ** ((3.562 - math.log10(r_w_75 - 0.0123)) / 0.955)

# --- Output Section ---
st.header("📊 Results")

st.write(f"**Electrolyte Used:** {'NaCl' if electrolyte == 'NaCl (Default)' else 'KCl'}")
st.write(f"**Reservoir Temperature:** {reservoir_temp} °F")
st.write(f"**R_mf_x:** {r_mf_x:.3f} Ω·m at {r_mf_x_temp}°F")
st.write(f"**R_mf at Reservoir Temp:** {r_mf_reservoir:.3f} Ω·m")
st.write(f"**R_mfe at 75°F:** {r_mfe:.3f} Ω·m")
st.write(f"**R_mfe at Reservoir Temp:** {r_mfe_reservoir:.3f} Ω·m")
st.write(f"**R_we at Reservoir Temp:** {r_we:.3f} Ω·m")
st.write(f"**R_we at 75°F:** {r_we_75:.3f} Ω·m")
st.write(f"**R_w at 75°F:** {r_w_75:.3f} Ω·m")
st.write(f"**R_w at Reservoir Temp:** {r_w_reservoir:.3f} Ω·m")
st.write(f"**Salinity:** {salinity:.3f} ppm")

st.success("Calculation completed successfully!")
