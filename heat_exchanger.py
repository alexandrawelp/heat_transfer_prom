"""
script with heat exchanger modelling
co-current and counter-current as boundary value problem

author: Alexandra Welp
"""

import numpy as np
import CoolProp.CoolProp as CP
from scipy.integrate import solve_bvp
import matplotlib.pyplot as plt
import fluid_properties_rp as fprop
from scipy.optimize import root

_props = "REFPROP"

def heat_exchanger_counter_current(x, h, p1, p2, fluid_1, fluid_2, di, alpha_local, m_dot_1, m_dot_2):
    T_AF = fprop.hp_v(h[0], p1, fluid_1)[0]
    T_SF = fprop.hp_v(h[1], p2, fluid_2)[0]
    delta_T = T_AF - T_SF
    dhdx_0 = -np.pi * di * alpha_local * delta_T / m_dot_1
    dhdx_1 = -np.pi * di * alpha_local * delta_T / m_dot_2
    return np.array([dhdx_0, dhdx_1])

def bc_he_counter(hlinks, hrechts):
    return np.array([hlinks[0]-h1_ein, hrechts[1]-h2_ein])



def call_HE_co(T_KM_ein, T_W_out, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1, fluid_2, comp):
    def heat_exchanger_co_current(x, h, p1, p2, fluid_1, fluid_2, comp, di, alpha_local, m_dot_1, m_dot_2):
        T_AF = fprop.hp_v(h[0], p1, fluid_1, comp)[0]
        T_SF = fprop.hp_v(h[1], p2, fluid_2)[0]
        delta_T = T_AF - T_SF
        dhdx_0 = -np.pi * di * alpha_local * delta_T / m_dot_1
        dhdx_1 = np.pi * di * alpha_local * delta_T / m_dot_2
        return np.array([dhdx_0, dhdx_1])

    def bc_he_co(hleft, hright):
        return np.array([hleft[0] - h1_ein, hright[1] - h2_out])

    h1_ein = fprop.tp(T_KM_ein, p_KM, fluid_1, comp)[2]
    h2_out = fprop.tp(T_W_out, p_W, fluid_2)[2]
    x_var = np.linspace(0, l, resolution)
    h_schaetz = np.zeros((2, resolution))
    h_schaetz[0, :] = h1_ein
    h_schaetz[1, :] = h2_out
    res = solve_bvp(lambda x, h: heat_exchanger_co_current(x, h, p_KM, p_W, fluid_1, fluid_2, comp,
                                                           di, alpha_local, m_dot_1, m_dot_2),
                    bc_he_co, x_var, h_schaetz)
    if res.message != "The algorithm converged to the desired accuracy.":
        print(res.message)
        raise ValueError("The solver did not converge.")
    T_KM_aus = fprop.hp(res.y[0,-1], p_KM, fluid_1, comp)[0]
    T_W_ein = fprop.hp(res.y[1,0], p_W, fluid_2)[0]
    return T_KM_aus, T_W_ein

def linked_he(T_W9, T_KM1, T_W1_real, p_KM, p_W, fluid_1, fluid_2, comp, resolution):
    T_KM2, T_W8 = call_HE_co(T_KM1, T_W9, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1, fluid_2, comp)
    T_KM3, T_W7 = call_HE_co(T_KM2, T_W8, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM4, T_W6 = call_HE_co(T_KM3, T_W7, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM5, T_W5 = call_HE_co(T_KM4, T_W6, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM6, T_W4 = call_HE_co(T_KM5, T_W5, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM7, T_W3 = call_HE_co(T_KM6, T_W4, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM8, T_W2 = call_HE_co(T_KM7, T_W3, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM9, T_W1 = call_HE_co(T_KM8, T_W2, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    plt.figure(1)
    plt.plot(np.linspace(0,16,9), [T_KM1, T_KM2, T_KM3, T_KM4, T_KM5, T_KM6, T_KM7, T_KM8, T_KM9],'*k')
    plt.plot(np.linspace(0,14,8), [T_W8, T_W7, T_W6, T_W5, T_W4, T_W3, T_W2, T_W1],'*b')
    plt.plot(np.linspace(2, 16, 8), [T_W9, T_W8, T_W7, T_W6, T_W5, T_W4, T_W3, T_W2],'*r')

    return T_W1 - T_W1_real

def get_overall_temperatures(T_KM_ein, T_W_out, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1, fluid_2, comp):
    def heat_exchanger_co_current(x, h, p1, p2, fluid_1, fluid_2, comp, di, alpha_local, m_dot_1, m_dot_2):
        T_AF = fprop.hp_v(h[0], p1, fluid_1, comp)[0]
        T_SF = fprop.hp_v(h[1], p2, fluid_2)[0]
        delta_T = T_AF - T_SF
        dhdx_0 = -np.pi * di * alpha_local * delta_T / m_dot_1
        dhdx_1 = np.pi * di * alpha_local * delta_T / m_dot_2
        return np.array([dhdx_0, dhdx_1])

    def bc_he_co(hleft, hright):
        return np.array([hleft[0] - h1_ein, hright[1] - h2_out])

    h1_ein = fprop.tp(T_KM_ein, p_KM, fluid_1, comp)[2]
    h2_out = fprop.tp(T_W_out, p_W, fluid_2)[2]
    x_var = np.linspace(0, l, resolution)
    h_schaetz = np.zeros((2, resolution))
    h_schaetz[0, :] = h1_ein
    h_schaetz[1, :] = h2_out
    res = solve_bvp(lambda x, h: heat_exchanger_co_current(x, h, p_KM, p_W, fluid_1, fluid_2, comp,
                                                           di, alpha_local, m_dot_1, m_dot_2),
                    bc_he_co, x_var, h_schaetz)
    if res.message != "The algorithm converged to the desired accuracy.":
        print(res.message)
        raise ValueError("The solver did not converge.")
    T_KM_aus = fprop.hp_v(res.y[0], p_KM, fluid_1, comp)[0]
    T_W_ein = fprop.hp_v(res.y[1], p_W, fluid_2)[0]
    return T_KM_aus, T_W_ein


if __name__ == "__main__":
    fluid_1 = "Propane;Isobutane"
    comp = [0.4, 0.6]
    fluid_2 = "water"
    m_dot_1 = 20e-3
    m_dot_2 = 20e-3
    p_KM = 10e6
    p_W = 1e6

    alpha_local = 400
    di = 10e-3
    l = 2
    T_KM1 = 55 + 273.15
    T_W1_real = 20 +273.15
    T_W9_guess = 45+ 273.15
    resolution = 100

    res = root(linked_he, T_W9_guess, args=(T_KM1, T_W1_real, p_KM, p_W, fluid_1, fluid_2, comp, resolution))
    T_W9 = res.x

    T_KM_R1, T_W_R1 = get_overall_temperatures(T_KM1, T_W9, p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1, fluid_2, comp)
    T_KM_R2, T_W_R2 = get_overall_temperatures(T_KM_R1[-1], T_W_R1[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R3, T_W_R3 = get_overall_temperatures(T_KM_R2[-1], T_W_R2[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R4, T_W_R4 = get_overall_temperatures(T_KM_R3[-1], T_W_R3[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R5, T_W_R5 = get_overall_temperatures(T_KM_R4[-1], T_W_R4[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R6, T_W_R6 = get_overall_temperatures(T_KM_R5[-1], T_W_R5[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R7, T_W_R7 = get_overall_temperatures(T_KM_R6[-1], T_W_R6[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)
    T_KM_R8, T_W_R8 = get_overall_temperatures(T_KM_R7[-1], T_W_R7[0], p_KM, p_W, resolution, di, alpha_local, m_dot_1, m_dot_2, fluid_1,
                             fluid_2, comp)

    plt.figure(2)
    plt.plot(np.linspace(0,2,resolution), T_KM_R1, '-b')
    plt.plot(np.linspace(0, 2, resolution), T_W_R1, '-r')

    plt.plot(np.linspace(2, 4, resolution), T_KM_R2, '-b')
    plt.plot(np.linspace(2, 4, resolution), T_W_R2, '-r')

    plt.plot(np.linspace(4, 6, resolution), T_KM_R3, '-b')
    plt.plot(np.linspace(4, 6, resolution), T_W_R3, '-r')

    plt.plot(np.linspace(6, 8, resolution), T_KM_R4, '-b')
    plt.plot(np.linspace(6, 8, resolution), T_W_R4, '-r')

    plt.plot(np.linspace(8, 10, resolution), T_KM_R5, '-b')
    plt.plot(np.linspace(8, 10, resolution), T_W_R5, '-r')

    plt.plot(np.linspace(10, 12, resolution), T_KM_R6, '-b')
    plt.plot(np.linspace(10, 12, resolution), T_W_R6, '-r')

    plt.plot(np.linspace(12, 14, resolution), T_KM_R7, '-b')
    plt.plot(np.linspace(12, 14, resolution), T_W_R7, '-r')

    plt.plot(np.linspace(14, 16, resolution), T_KM_R8, '-b')
    plt.plot(np.linspace(14, 16, resolution), T_W_R8, '-r')

    plt.show()

