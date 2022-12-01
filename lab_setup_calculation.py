'''
calculate benchmarks for lab setup
author: Alexandra Welp
1: compressor inlet
2: compressor outlet
3: condenser outlet
4: evaporator inlet
'''

import CoolProp.CoolProp as CP
import numpy as np
import matplotlib.pyplot as plt

fluid = "IsoButane"

p_o = 103000        # lowest possible pressure
T_o = CP.PropsSI("T", "P", p_o, "Q", 0.5, fluid)

p_c = 13e5
T_c = CP.PropsSI("T", "P", p_c, "Q", 0, fluid)

delta_T_sh_lp = 20          # delta T superheated low pressure
eta_compressor = 0.65

T_1 = (T_o + delta_T_sh_lp)
h_1 = CP.PropsSI("H", "T", T_1, "P", p_o, fluid)
s_1 = CP.PropsSI("S", "T", T_1, "P", p_o, fluid)
h_2s = CP.PropsSI("H", "S", s_1, "P", p_c, fluid)

h_2 = (h_2s - h_1) / eta_compressor + h_1
T_2 = CP.PropsSI("T", "P", p_c, "H", h_2, fluid)
s_2 = CP.PropsSI("S", "T", T_2, "P", p_c, fluid)

w_compressor = h_2 - h_1
T_2 = CP.PropsSI("T", "H", h_2, "P", p_c, fluid)
delta_T_sh_hp = T_2 - T_c

h_2b = CP.PropsSI("H", "P", p_c, "Q", 1, fluid)
s_2b = CP.PropsSI("S", "P", p_c, "Q", 1, fluid)
h_2c = CP.PropsSI("H", "P", p_c, "Q", 0, fluid)
s_2c = CP.PropsSI("S", "P", p_c, "Q", 0, fluid)

delta_h_sh = h_2 - h_2b
delta_h_ws = h_2b - h_2c

h_4b = CP.PropsSI("H", "P", p_o, "Q", 0, fluid)
s_4b = CP.PropsSI("S", "P", p_o, "Q", 0, fluid)
h_4c = CP.PropsSI("H", "P", p_o, "Q", 1, fluid)
s_4c = CP.PropsSI("S", "P", p_o, "Q", 1, fluid)

delta_T_sc_lp = 10          # deltaT subcooled low pressure
T_4 = T_o - delta_T_sc_lp
h_4 = CP.PropsSI("H", "T", T_4, "P", p_o, fluid)
h_3 = h_4                   # throttle isenthalp
T_3 = CP.PropsSI("T", "P", p_c, "H", h_3, fluid)
s_3 = CP.PropsSI("S", "T", T_3, "P", p_c, fluid)

s_4 = CP.PropsSI("S", "P", p_o, "H", h_4, fluid)

delta_h_sc = h_2c - h_3

delta_h_o = h_1 - h_4

# plt.plot(s_1, T_1, '*')
# plt.plot(s_2, T_2, '*')
# plt.plot(s_2b, T_c, '*')
# plt.plot(s_2c, T_c, '*')
# plt.plot(s_3, T_3, '*')
# plt.plot(s_4, T_4, '*')
# plt.plot(s_4b, T_o, '*')
# plt.plot(s_4c, T_o, '*')
point_label = ["1", "2", "2b", "2c", "3", "4", "4b", "4c"]
x = [s_1, s_2, s_2b, s_2c, s_3, s_4, s_4b, s_4c]
y = [T_1, T_2, T_c, T_c, T_3, T_4, T_o, T_o]
for i in range(len(x)):
    plt.plot(x[i], y[i], '*', markersize=15)
    plt.annotate(point_label[i], (x[i]+25, y[i]), fontsize=12)

plt.xlabel("s in J/kg/K")
plt.ylabel("T in K")
plt.legend()

#plt.show()

# Berechnung des Nassdampfbereichs #

s_i = []
s_j = []
t_step = np.linspace(200, 400, 50)
for t_i in t_step:
    s_i1 = CP.PropsSI('S', 'T', t_i, 'Q', 0, fluid)
    s_i2 = CP.PropsSI('S', 'T', t_i, 'Q', 1, fluid)
    s_i.append(s_i1)
    s_j.append(s_i2)

plt.plot(s_i, t_step, 'k-')
plt.plot(s_j, t_step, 'k-', label="wet steam region")
#plt.xlabel('s in J/kg/K')
#plt.ylabel('T in K')
plt.title('T-s-Diagramm für ' + fluid)

# Berechnung Isobare #
s_step = np.linspace(200, 2700, 100)
for px in [p_o, p_c]:
    t_isobar = []
    for si in s_step:
        t_iso = CP.PropsSI('T', 'S', si, 'P', px, fluid)
        t_isobar.append(t_iso)

    plt.plot(s_step, t_isobar, 'b:', label="isobare")
plt.legend()


print(f"delta_h superheated hp: {delta_h_sh} J/kg")
print(f"delta_h wet steam hp: {delta_h_ws} J/kg")
print(f"delta_h subcooled: {delta_h_sc} J/kg")
plt.show()