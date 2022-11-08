from heat_transfer_evaporator import PointND
import CoolProp.CoolProp as CP
import pytest

@pytest.fixture
def point_test():
    m_dot = 200
    d = 12e-3
    return PointND(T = 300, q = 2e5, "Pentane", "testcase"),m_dot,d

def test_Reynolds(point_test, m_dot, d):
    point_test.Reynolds(m_dot, d)
    test_dyn_vis = CP.PropsSI("")

