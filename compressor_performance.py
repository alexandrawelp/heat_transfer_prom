"""
created on 22.11.2022
compare compressor performance of Bitzer compressor
author: Alexandra Welp
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_polynom(to, tc, coefficients):
    """
    calculates value of polynom for Q, P, m, I depending on coefficients
    :param coefficients: array 1*10
    :param to: evaporating temperature
    :param tc: condensing temperature
    :return: Q, P, m, I depending on input coefficients
    """
    y = coefficients[0] + coefficients[1] * to + coefficients[2] * tc + coefficients[3] * to ** 2 + coefficients[4] * to * tc + \
         coefficients[5] * tc ** 2 + coefficients[6] * to ** 3 + coefficients[7] * tc * to ** 2 + coefficients[8] * to * tc ** 2 + \
         coefficients[9] * tc ** 3
    return y

# Compressor type 2HESP-2P
fluid = "Propane"
coeff_T_suction20 = pd.read_excel('HESP-2P_20temsuction.xlsx', header=26, usecols=[1,2,3,4,5,6,7,8,9,10])

coeff_Q = coeff_T_suction20.iloc[0]
coeff_P = coeff_T_suction20.iloc[1]
coeff_m = coeff_T_suction20.iloc[2]

to_var = np.linspace(-35, 0, 8)
tc_var = np.linspace(10, 65, 10)

Q = np.zeros((len(to_var),len(tc_var)))
P = np.zeros((len(to_var),len(tc_var)))
m = np.zeros((len(to_var),len(tc_var)))

for i, to in enumerate(to_var):
    for j, tc in enumerate(tc_var):
        Q[i,j] = calculate_polynom(to, tc, coeff_Q)
        P[i,j] = calculate_polynom(to, tc, coeff_P)
        m[i,j] = calculate_polynom(to, tc, coeff_m)

fig, ax = plt.subplots(1, 4)

ax[0].plot(to_var, P, label=np.round(tc_var,1))

ax[0].set_title("power")
ax[0].set_ylabel("power in W")


ax[1].plot(to_var, Q+P, label=np.round(tc_var,1))
ax[1].set_title("heating power")
ax[1].set_ylabel("heat in W")



ax[2].plot(to_var, m, label=np.round(tc_var,1))
ax[2].set_title("massflow")
ax[2].set_ylabel("massflow in kg/h")

ax[3].plot(to_var, (Q+P)/P, label=np.round(tc_var, 1))
ax[3].set_title("COP")
ax[3].set_ylabel("COP [-]")

for i in ax.flat:
    i.set_xlabel("to, evaporating temperature in °C")
    i.legend(loc="best")
plt.show()