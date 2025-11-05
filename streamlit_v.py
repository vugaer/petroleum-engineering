import streamlit as st
import math

# --- Page Title ---
st.title("Water Resistivity Calculator based on Mud Filtrate Resistivity and Temperature")

# --- User Inputs ---
st.header("Input: ")
sp_log_reading = st.number_input('SP Log Reading (mV)', value=-70)
reservoir_temp = st.number_input('Reservoir Temperature (°F)', value=150.0)
r_mf_x = st.number_input('Mud Filtrate Resistivity R_mf (Ω·m)', value=0.59)
r_mf_x_temp = st.number_input('Temperature of Mud at given resistivity (°F)', value=78.0)

# Select electrolyte type
electrolyte = st.radio(
    "SSP Determination:",
    ("NaCl (Default)", "KCl")
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

# For NaCl
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
st.header("Resistivity and Temperature Summary")

st.write(f"Reservoir Temperature : {reservoir_temp:.1f} °F")
st.write(f"Mud Filtrate Resistivity : {r_mf_x:.3f} Ω·m at {r_mf_x_temp:.1f} °F")
st.write(f"Mud Filtrate Resistivity at Reservoir Temperature : {r_mf_reservoir:.3f} Ω·m")
st.write(f"Effective Mud Filtrate Resistivity at 75°F : {r_mfe:.3f} Ω·m")
st.write(f"Effective Mud Filtrate Resistivity at Reservoir Temperature : {r_mfe_reservoir:.3f} Ω·m")
st.write(f"Water Resistivity (Rwe) at Reservoir Temperature : {r_we:.3f} Ω·m")
st.write(f"Water Resistivity (Rwe) at 75°F : {r_we_75:.3f} Ω·m")
st.write(f"Water Resistivity (Rw) at 75°F : {r_w_75:.3f} Ω·m")
st.write(f"Water Resistivity at Reservoir Temperature : {r_w_reservoir:.3f} Ω·m")
st.write(f"Salinity : {salinity:.3f} ppm")
