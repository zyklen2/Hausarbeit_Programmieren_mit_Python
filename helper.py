# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 07:47:18 2022

@author: olive
"""
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import statsmodels.api as sm

class Helper:
    
    def calculate_lin_reg_params(self,x, y, deg):
        print(np.polyfit(x, y, deg))
        params = np.polyfit(x, y, deg)
        return params

    def calculate_lin_reg_values(self, params, x):
        vals = np.linspace(1,1,len(x))
        temp_exp = len(params)-1
        for nr in range(len(params)-1):
            vals += x*(params[nr]**temp_exp)
            temp_exp-=1
        return vals+params[-1]