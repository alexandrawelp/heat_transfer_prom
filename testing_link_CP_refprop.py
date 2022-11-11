# Testskript to us call refprop from coolprop

import CoolProp.CoolProp as CP

# High-level interface
fluid = "REFPROP::Butane"
p = 101325
q = 0

T = CP.PropsSI('T', 'P', p, 'Q', q, fluid)
print(T)

# Low level interface
testpoint = CP.AbstractState('REFPROP', 'Water')
testpoint.update(CP.PQ_INPUTS, 101325, 0)
print(testpoint.T)
