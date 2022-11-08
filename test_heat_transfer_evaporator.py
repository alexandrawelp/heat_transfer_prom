from heat_transfer_evaporator import PointND
import CoolProp.CoolProp as CP
import pytest


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

