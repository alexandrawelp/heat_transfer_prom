# TREND 5.0 Python Interface
# Example Call
# @authors: David Celný , Sven Pohl
# Bochum, 16.05.2019

import fluid_properties_rp as fprop

# import bitzer_poly_read as br
import compressor_performance as comper
import matplotlib.pyplot as plt
import numpy as np


_props = "REFPROP"
Tevap = 273.15 - 20
Tcond = 273.15+60
Tin = 273.15 + 20
Tout = 273.15 + 131.5

fluid_s = "Propane * Pentane"
comp = [.4, 0.6]
fluid_s = "Propane"
comp = [1]
#secondary_fluid = CP.AbstractState("TTSE&HEOS", fluid_s)
# interesting, when using "BICUBIC&HEOS" the exergy of the ambient state is 0.15!

#statedata = fprop.T_prop_sat(Tevap, fluid_s, composition = comp, option=1)

def eta_calc(Tev, Tcond, Tin=Tin, fluid_s =fluid_s):
    """
    Calculate the isentropic work for different condenser and evaporator 
    pressures (at given T =Input) and compare it with the specific work
    as derived from a polinomial from Bitzer for their compressors.
    (From Bitzer we ger P_el and mdor , thus, h = P_el/mdot).
    The compressor inlet Temp.  is fixed at Tin
    BA 22.11.2022
    
    Parameters.
    
    ----------
    Tev : TYPE
      in K   DESCRIPTION.
    Tcond : TYPE
        DESCRIPTION.
    Tin : TYPE, optional
        DESCRIPTION. The default is Tin.
    fluid_s : TYPE, optional
        DESCRIPTION. The default is fluid_s.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    comp = [1]
    evap = fprop.T_prop_sat(Tev, fluid_s, composition=comp, option=1) # evaporator pressure
    comp_in = fprop.tp(Tin, evap, fluid_s, composition=comp, option=1)  # compressor entrance at 20C
    cond = fprop.T_prop_sat(Tcond, fluid_s, composition = comp, option=1) # condenser pressure
    # isentropic state after compressor
    comp_s = fprop.sp(comp_in[ 4], cond, fluid_s, composition=comp)
    print(f"comp_s {comp_s}")
    dhs = comp_s[2] - comp_in[2]
    
    to = Tev-273.15
    tc = Tcond-273.15

    coeff_Q, coeff_P, coeff_m = comper.read_file("polynom-2EESP-2P.xlsx")
    Q, power_el, mdot = comper.cal_range(to, tc, coeff_Q, coeff_P, coeff_m)
    #power_el = br.bitzer_pol(to, tc, br.cP)
    #mdot = br.bitzer_pol(to, tc, br.cm) / 3600
    dh = power_el / mdot
    comp_out = fprop.hp(comp_in[2]+dh, cond, fluid_s, composition=comp)
    # fld.ALLPROP('HP', comp_in["H"] + dh, cond["P"])  # real stae after compressor
    #   d = fld.ALLPROP('TP', Tout, cond["P"])  # real stae after compressor (Bitzer)
    v_ratio = comp_out[3] / comp_in[3]
    p_ratio = comp_out[1] / comp_in[1]
    etas = dhs / dh
    
    return np.array([etas, comp_out[0], comp_out[1], evap, v_ratio,
                     p_ratio, power_el, mdot])

if __name__ == "__main__":
    fi, ax = plt.subplots(2, 2)
    n_no = 5
    col = ["b.", "ro-", "k", "k.", "bv-"]
    Te = np.linspace(-25, 0, n_no)+273.15
    Tc = np.linspace(30, 60, 10)+273.15
    for i, te in enumerate(Te):
        result = []
        for tc in Tc:
            result.append(eta_calc(te, tc))
        result = np.array(result)
        ax[0, 0].plot(Tc, result[:, 0], col[i], label="%3i" % (te))
        ax[0, 1].plot(Tc, result[:, 1], col[i], label="%3i" % (te))
        ax[1, 0].plot(Tc, result[:, -2], col[i], label="%3i" % (te))
        ax[1, 1].plot(Tc, result[:, -1], col[i], label="%3i" % (te))
    for i in ax.flat:
        i.set_xlabel("tc, condensing temperature in °C")
    ax[0,0].set_ylabel("eta_s")
    ax[0,1].set_ylabel("T_out")
    ax[1,0].set_ylabel("Power_el")
    ax[1,1].set_ylabel("m_dot")
ax[1, 1].legend()
fi.savefig("bitzer2EESP-05PProbe.png")
print(eta_calc(Tevap, Tcond))
plt.show()
