import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../src/fdm/solver/")
import fdm_solver as fdm
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../src/util/diff_operator_expression")
import diff_op_expression as expr
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../src/util/")
import diff_operators.impl.ddx as ddx, diff_operators.impl.ddy as ddy, diff_operators.impl.laplacian2d as laplacian2d,\
    diff_operators.impl.ddt as ddt, diff_operators.impl.time_dependent_d2dx as td_d2dx
import diff_operators.core.diff_op as diff_op
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../src/util/domain_conditions/core/domain")
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../../src/util/domain_conditions/impl/dirichlet")
import dirichlet_rectangle as dr
import domain as dm
import unittest
import numpy as np
import math

class Test(unittest.TestCase):
    def setUp(self):
        td_domain = dm.domain(np.array([0, 0]), np.array([1, 1]))
        td_inDomain = lambda x, y: 0 < x < 1 and 0 < y < 1
        td_onBoundary = lambda x, y: abs(x-1) < np.spacing(1) or abs(x) < np.spacing(1) \
            or abs(y) < np.spacing(1)
        def td_getBV(x, y):
            if abs(x) < np.spacing(1) or abs(x-1) < np.spacing(1):
                return 0
            else:
                return 6*math.sin(math.pi*x)
        f_s = lambda x, y: 0
        dirichlet = dr.dirichlet_rectangular_bc(td_inDomain, td_onBoundary, td_getBV, td_domain)
        self.solver = fdm.fdm_solver([], f_s, dirichlet)

    def test_is_time_dependent(self):
        a = ddt.ddt(0.1)
        b = td_d2dx.td_d2dx(0.1)
        expression = expr.diff_operator_expression([a, b])
        self.solver.diff_op_expression = expression
        assert self.solver._is_time_dependent() is True
        assert self.solver._all_ops_are_time_dependent() is True
        
    def test_all_ops_are_time_dependent(self):
        a = ddt.ddt(0.1)
        b = ddx.ddx(0.1)
        expression = expr.diff_operator_expression([a, b])
        self.solver.diff_op_expression = expression
        assert self.solver._all_ops_are_time_dependent() is False
    
    def test_td_solver(self):
        for n in [3]:
            dx, dt = 1/(n+1), 1/(n+1)
            a = ddt.ddt(dt)
            b = td_d2dx.td_d2dx(dx, coefficient = -1)
            expression = expr.diff_operator_expression([a, b])
            self.solver.diff_op_expression = expression
            #self.solver.solve(n, n)
            print(self.solver.solve(n, n))

if __name__ == '__main__':
    unittest.main()