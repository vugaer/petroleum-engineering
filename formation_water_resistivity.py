import math

sp_log_reading = float(input('SP(mV): '))
reservoir_temp = float(input('T(F): '))
r_mf_x, r_mf_x_temp = map(float, input('R_mf(Ohm.m) @ T(F): ').split('@'))

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
r_we = r_mfe_reservoir * 10 ** (ssp / (61 + 0.133 * reservoir_temp))

# for KCl
# r_we = r_mfe_reservoir * 10 ** (-(22 - ssp) / (56 + 0.12 * reservoir_temp))

r_we_75 = r_convert_temp(r_we, 150, 75)

if r_we_75 > 0.12:
  r_w_75 = -(0.58-10**(0.69*r_we_75-0.24))
if r_we_75 <= 0.12:
  r_w_75 = (77*r_we_75+5)/(146-377*r_we_75)

r_w_reservoir = r_convert_temp(r_w_75, 75, 150)
salinity = 10 ** ((3.562 - math.log10(r_w_75 - 0.0123)) / 0.955)


print("\n=== Resistivity and Temperature Summary ===\n")
print(f"Reservoir Temperature : {reservoir_temp}°F\n")
print(f"r_mf_x             : {r_mf_x:.3f} Ω·m   | Mud filtrate resistivity at {r_mf_x_temp}°F")
print(f"r_mf_reservoir     : {r_mf_reservoir:.3f} Ω·m   | Mud filtrate resistivity at reservoir temperature ({reservoir_temp}°F)")
print(f"r_mfe              : {r_mfe:.3f} Ω·m   | Effective mud filtrate resistivity at 75°F")
print(f"r_mfe_reservoir    : {r_mfe_reservoir:.3f} Ω·m   | Effective mud filtrate resistivity at {reservoir_temp}°F")
print(f"r_we               : {r_we:.3f} Ω·m   | Effective water resistivity at {reservoir_temp}°F")
print(f"r_we_75            : {r_we_75:.3f} Ω·m   | Effective water resistivity at 75°F")
print(f"r_w_75             : {r_w_75:.3f} Ω·m   | Water resistivity at 75°F")
print(f"r_w_reservoir      : {r_w_reservoir:.3f} Ω·m   | Water resistivity at reservoir temperature ({reservoir_temp}°F)")
print(f"Salinity           : {salinity:.3f} ppm   | Salinity")
