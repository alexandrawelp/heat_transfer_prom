from heat_transfer_evaporator import PointND
import CoolProp.CoolProp as CP
import pytest
import numpy as np


@pytest.fixture
def m_dot():
    return 200


@pytest.fixture
def d():
    return 12e-3


@pytest.fixture
def T():
    return 300


@pytest.fixture
def q():
    return 0.4


@pytest.fixture
def fluid():
    return "n-Butane"


@pytest.fixture
def point_test(m_dot, d, T, q, fluid):
    return PointND(T, q, fluid, "testcase")


def test_reynolds_l(point_test, m_dot, d, T, q, fluid):
    re_l_script = point_test.reynolds_l(m_dot, d)
    test_dyn_vis_l = CP.PropsSI('V', 'T', T, 'Q', 0, fluid)
    re_l_test = m_dot * (1 - q) * d / test_dyn_vis_l
    assert re_l_test == re_l_script


def test_reynolds_v(point_test, m_dot, d, T, q, fluid):
    re_v_script = point_test.reynolds_v(m_dot, d)
    test_dyn_vis_v = CP.PropsSI('V', 'T', T, 'Q', 1, fluid)
    re_v_test = m_dot * q * d / test_dyn_vis_v
    assert re_v_test == re_v_script

def test_alpha_lo():
    # values from example 1 VDI heat atlas p. 931
    d = 27e-3
    Ra = 2e-6
    p = 4.82e5
    fluid = "IsoButane"
    T = CP.PropsSI('T', 'P', p, 'Q', 1, fluid)
    q_dot = 60000
    m_dot = 250
    q_var = np.linspace(0, 0.3, 7)
    l = 4.3
    global inlet_flow
    inlet_flow = 'true'
    Rb = "qzu"
    alpha_lo_res = []
    for q in q_var:
        testpoint = PointND(T, q, fluid, "testcase test alpha_lo")
        z_i = q / max(q_var) * l
        alpha_lo_res.append(testpoint.alpha_1p_l(m_dot, d, z_i))

    alpha_lo_test = [1274, 992, 978, 973, 970, 968, 967]
    assert alpha_lo_test == pytest.approx(alpha_lo_res, rel=0.01)

    # TODO fix global variable issue



