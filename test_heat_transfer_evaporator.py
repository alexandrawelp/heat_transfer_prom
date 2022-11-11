# Testcase for heat transfer calculation evaporator
"""
created on 08.11.2022 by Alexandra Welp
Testcase for heat transfer coefficient testing
@ author: welp
"""

from heat_transfer_evaporator import PointND
import CoolProp.CoolProp as CP
import pytest
import numpy as np
from unittest.mock import Mock


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
    return PointND('TQ', T, q, fluid, "testcase")


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

def test_init():
    testpoint = PointND(387.52, 0.2, "Butane", "testcase")
    assert testpoint.T == pytest.approx(387.52, rel=1)
    assert testpoint.h == pytest.approx(554.03e3, rel=1)
    assert testpoint.h_v == pytest.approx(735.98e3,rel=1)
    assert testpoint.h_l == pytest.approx(508.54e3,rel=1)
    assert testpoint.rho == pytest.approx(181.71,rel=1)
    assert testpoint.rho_v == pytest.approx(54.354,rel=1)
    assert testpoint.rho_l == pytest.approx(438.66,rel=1)
    assert testpoint.cp_l == pytest.approx(3387.1,rel=1)
    assert testpoint.cp_v == pytest.approx(2981.5,rel=1)
    assert testpoint.c_v == pytest.approx(168.1, rel=1)
    assert testpoint.lam_v == pytest.approx(30.824e-3, rel=1)
    assert testpoint.lam_l == pytest.approx(74.056e-3, rel=1)
    assert testpoint.pr_v == pytest.approx(1.0052, rel=1)
    assert testpoint.pr_l == pytest.approx(3.477,rel=1)
    assert testpoint.sigma == pytest.approx(2.7377e-3, rel=1)


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



