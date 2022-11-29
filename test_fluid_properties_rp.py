'''
testing script test fluid properties
author: Alexandra Welp
29.11.2022
'''
import fluid_properties_rp as fprop
import pytest

def test_T_prop_sat():
    T = 248.15
    fluid = "Propane"
    p_test = fprop.T_prop_sat(T, fluid, [1.0], option=1)
    assert p_test == pytest.approx(203428,rel=1)
