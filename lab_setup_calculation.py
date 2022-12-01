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

h_1 = CP.PropsSI("H", "T", (T_o + delta_T_sh_lp), "P", p_o, fluid)
s_1 = CP.PropsSI("S", "T", (T_o + delta_T_sh_lp), "P", p_o, fluid)
h_2s = CP.PropsSI("H", "S", s_1, "P", p_c, fluid)
h_2 = (h_2s - h_1) / eta_compressor + h_1

w_compressor = h_2 - h_1
T_2 = CP.PropsSI("T", "H", h_2, "P", p_c, fluid)
delta_T_sh_hp = T_2 - T_c

h_2b = CP.PropsSI("H", "P", p_c, "Q", 1, fluid)
h_3 = CP.PropsSI("H", "P", p_c, "Q", 0, fluid)

