"""
Script to test the time consumption for different alternatives of getting fluid properties
11.11.2022
Author: Alexandra Welp
"""

import CoolProp.CoolProp as CP
import time
import numpy as np
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary
import os
RP = REFPROPFunctionLibrary(os.environ['RPPREFIX'])
RP.SETPATHdll(os.environ['RPPREFIX'])
MOLAR_BASE_SI = RP.GETENUMdll(0, "MOLAR BASE SI").iEnum

def get_properties_high_level(P, q, fluid):
    fluid = 'REFPROP::' + fluid
    T = CP.PropsSI('T', 'P', P, 'Q', q, fluid)
    h = CP.PropsSI('H', 'P', P, 'Q', q, fluid)
    rho = CP.PropsSI('D', 'P', P, 'Q', q, fluid)
    return h, T, rho


def get_properties_low_level(P, q, fluid):
    testpoint = CP.AbstractState('REFPROP', fluid)
    testpoint.update(CP.PQ_INPUTS, P, q)
    T = testpoint.T()
    h = testpoint.hmass()
    rho = testpoint.rhomass()
    return T, h, rho

def get_properties_direct_refprop(P, q, fluid):
    RP.SETFLUIDSdll(fluid)
    l = RP.ABFLSHdll("PQ", P, q, [1.0], 000)
    T = l.T
    h = l.h
    rho = l.D
    return T, h, rho

def get_properties_direct_refprop_dll(P, q, fluid):
    l = RP.REFPROPdll(fluid, 'PQ', "T;H;D",
                                 RP.MASS_BASE_SI, 1, 0, P, q, [1.0]).Output[0:3]
    T = l[0]
    h = l[1]
    rho = l[2]
    return T, h, rho

i = np.linspace(0,1,10000)
fluid = "Water"

print("call low level")
starttime_low_level = time.time()
for q in i:
    get_properties_low_level(101325, q, fluid)
endtime_low_level = time.time()
runtime_low_level = endtime_low_level - starttime_low_level

print("call high level")
starttime_high_level = time.time()
for q in i:
    get_properties_high_level(101325, q, fluid)
endtime_high_level = time.time()
runtime_high_level = endtime_high_level - starttime_high_level

print("call direct refprop")
starttime_refprop = time.time()
for q in i:
    get_properties_direct_refprop(101325, q, fluid)
endtime_refprop = time.time()
runtime_refprop = endtime_refprop - starttime_refprop

print("call direct refprop dll")
starttime_refprop_dll = time.time()
for q in i:
    get_properties_direct_refprop_dll(101325, q, fluid)
endtime_refprop_dll = time.time()
runtime_refprop_dll = endtime_refprop_dll - starttime_refprop_dll

print(f"Laufzeit low level {runtime_low_level}s")
print(f"Laufzeit high level {runtime_high_level}s")
print(f"Laufzeit RefProp {runtime_refprop}s")
print(f"Laufzeit Refprop dll {runtime_refprop_dll}s")
