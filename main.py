# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 06:11:55 2022

@author: olive
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from Dataloader import Data_manager
import statsmodels.api as sm


data_manager = Data_manager()

training_data = data_manager.get_data_from_table_as_dataframe("train_dat")
print(training_data.head(10))
data_ideal_funcs = data_manager.get_data_from_table_as_dataframe("ideal_dat")
print(data_ideal_funcs.head(10))


df_test = pd.read_csv("test.csv")
# print(df_test.columns)











func_params_list = []
for y_nr_train in range(1,5):
    if(y_nr_train == 1):
        # deg=2
        deg=1
    elif(y_nr_train == 2):
        deg=1
    elif(y_nr_train == 3):
        # deg=3
        deg=1
    elif(y_nr_train == 4):
        # deg=2
        deg=1
    
    func_params = data_manager.calculate_lin_reg_params(training_data["x"], training_data[f"y{y_nr_train}"], deg)
    func_params_list.append(func_params)
    
    y_test = df_test["y"]
    y = data_manager.calculate_lin_reg_values(func_params, training_data["x"])
    # y = calculate_lin_reg_values(func_params, df_test["x"])
    # trained_func_fits_test = not any([abs(y[nr]-y_test[nr])>math.sqrt(2) for nr in range(len(y))])
    
    plt.figure(f"linreg {y_nr_train}")
    plt.scatter(training_data["x"], training_data[f"y{y_nr_train}"])
    plt.plot(training_data["x"],y)
    
    # plt.figure(f"linreg {y_nr_train}")
    # plt.scatter(df_test["x"],df_test["y"])
    # plt.plot(df_test["x"],y)
    













