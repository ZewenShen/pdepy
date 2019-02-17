import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/..')
from core import time_dependent_op # diff_operators' core
import numpy as np
class td_d2dx(time_dependent_op.time_dependent_operator):
    def __init__(self, dx, coefficient = 1):
        left = [((-1, 1), 1/(2*dx**2)), ((0, 1), -1/dx**2), ((1, 1), 1/(2*dx**2))]
        right = [((-1, 0), 1/(2*dx**2)), ((0, 0), -1/dx**2), ((1, 0), 1/(2*dx**2))]
        super().__init__(left, right, coefficient)