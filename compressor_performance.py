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
def read_file(name_file):
    coeff_T_suction20 = pd.read_excel(name_file, header=26, usecols=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    coeff_Q = coeff_T_suction20.iloc[0]
    coeff_P = coeff_T_suction20.iloc[1]
    coeff_m = coeff_T_suction20.iloc[2]
    return coeff_Q, coeff_P, coeff_m

def cal_range(to_var, tc_var, coeff_Q, coeff_P, coeff_m):
    Q = np.zeros((len(to_var), len(tc_var)))
    P = np.zeros((len(to_var), len(tc_var)))
    m = np.zeros((len(to_var), len(tc_var)))
    for i, to in enumerate(to_var):
        for j, tc in enumerate(tc_var):
            Q[i,j] = calculate_polynom(to, tc, coeff_Q)
            P[i,j] = calculate_polynom(to, tc, coeff_P)
            m[i,j] = calculate_polynom(to, tc, coeff_m)
    return Q, P, m

def plot_results(Q, P, m):
    fig, ax = plt.subplots(2, 3)

    ax[0, 0].plot(to_var, P, label=np.round(tc_var, 1))
    ax[0, 0].set_title("power compressor")
    ax[0, 0].set_ylabel("power in W")

    ax[0, 1].plot(to_var, Q + P, label=np.round(tc_var, 1))
    ax[0, 1].set_title("heating power")
    ax[0, 1].set_ylabel("heat in W")

    ax[0, 2].plot(to_var, m, label=np.round(tc_var, 1))
    ax[0, 2].set_title("massflow")
    ax[0, 2].set_ylabel("massflow in kg/h")

    ax[1, 2].plot(to_var, (Q + P) / P, label=np.round(tc_var, 1))
    ax[1, 2].set_title("COP")
    ax[1, 2].set_ylabel("COP [-]")

    for i in ax.flat:
        i.set_xlabel("to, evaporating temperature in °C")

    ax[1, 0].plot(P, (Q + P) / P, label=np.round(tc_var, 1))
    ax[1, 0].set_title("COP - power compressor w")
    ax[1, 0].set_ylabel("COP")
    ax[1, 0].set_xlabel("power compressor in W")

    ax[1, 1].plot(Q + P, (Q + P) / P, label=np.round(tc_var, 1))
    ax[1, 1].set_title("COP - heating power w")
    ax[1, 1].set_ylabel("COP")
    ax[1, 1].set_xlabel("power heat in W")

    for i in ax.flat:
        i.legend(loc="best")
    plt.show()

if __name__ == "__main__":
    # Compressor type 2HESP-2P
    fluid = "Propane"
    name = 'HESP-2P_20temsuction.xlsx'

    to_var = np.linspace(-35, 0, 8)
    tc_var = np.linspace(10, 65, 10)

    coeff_Q, coeff_P, coeff_m = read_file(name)
    Q, P, m = cal_range(to_var, tc_var, coeff_Q, coeff_P, coeff_m)

    plot_results(Q, P, m)






