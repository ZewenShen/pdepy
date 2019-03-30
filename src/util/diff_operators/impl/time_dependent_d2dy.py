import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
from core import time_dependent_op # diff_operators' core
import numpy as np
class td_d2dy(time_dependent_op.time_dependent_operator):
    def __init__(self, dy, coefficient = 1):
        stencil = [((-1, 0), 1/(2*dy**2)), ((0, 0), -1/dy**2), ((1, 0), 1/(2*dy**2)), ((-1, -1), 1/(2*dy**2)), ((0, -1), -1/dy**2), ((1, -1), 1/(2*dy**2))]
        explicit_stencil = [((0, -1), 1/(dy**2)), ((0, 0), -2/(dy**2)), ((0, 1), 1/(dy**2))]
        super().__init__(stencil, explicit_stencil=explicit_stencil, coefficient=coefficient)