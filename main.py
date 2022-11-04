# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 06:11:55 2022

@author: olive
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from datamanager import Data_manager


data_manager = Data_manager()
#load csv with testdata
df_test = pd.read_csv("rawdata/test.csv")
x_test = df_test["x"].to_numpy()
y_test = df_test["y"].to_numpy()

print("Daten aus der Datenbank laden.")
#load trainingdata and ideal functions from database
training_data = data_manager.get_data_from_table_as_dataframe("train_dat")
data_ideal_funcs = data_manager.get_data_from_table_as_dataframe("ideal_dat")

print("Datenanalyse starten.")
func_per_dataset = {}#Dictionary containing which ideal function fits which training dataset
delta_ideal={}#dictionary containing the lowest differences between ideal function and test datapoint values
func_ideal={}#dictionary containing the ideal function numbers that fit each specific testdatapoint best
x_vals={}#dictionary containing testdata x-values
y_vals={}#dictionary containing testdata y-values

#for every training y-dataset
for y_nr_train in range(1,5):
    
    #Aufgabe 1.1.1
    ideal_func_num = 0
    ideal_func_diff_value = math.inf
    for y_nr_ideal in range(1, 51):
        temp_diff = data_manager.calculate_squared_difference(training_data[f"y{y_nr_train}"], data_ideal_funcs[f"y{y_nr_ideal}"])
        if(temp_diff < ideal_func_diff_value):
            ideal_func_num = y_nr_ideal
            ideal_func_diff_value = temp_diff
    
    #save the ideal function for the current training data
    func_per_dataset[y_nr_train] = ideal_func_num
    
    #Plot of trainingsdata and the determined ideal function
    plt.figure(f"Training Data {y_nr_train} with ideal function {ideal_func_num}")
    plt.title(f"Training Data {y_nr_train} with ideal function {ideal_func_num}")
    plt.scatter(training_data["x"], training_data[f"y{y_nr_train}"], label="training data")
    plt.scatter(data_ideal_funcs["x"], data_ideal_funcs[f"y{ideal_func_num}"], label="ideal function data")
    plt.legend(loc="upper right")
    
    #Aufgabe 1.1.2 a
    y_ideal_for_test_data = []
    value_diffs = []
    value_check_sqrt2 = []
    for nr, value in enumerate(y_test):
        y_ideal_for_test_data.append(data_ideal_funcs.loc[data_ideal_funcs['x'] == x_test[nr]][f"y{ideal_func_num}"].to_numpy()[0])
        value_diffs.append(abs(value - y_ideal_for_test_data[-1]))
        value_check_sqrt2.append(value_diffs[-1] < math.sqrt(2))
    value_diffs=np.array(value_diffs)
    
    #get the testdata values within sqrt(2) range around the current ideal function
    fitting_test_x_vals = x_test[value_check_sqrt2]
    fitting_test_y_vals = y_test[value_check_sqrt2]
    fitting_test_val_diffs = value_diffs[value_check_sqrt2]
    
    #Aufgabe 1.1.2 b
    func_ideal_keys = list(func_ideal.keys())
    for x_nr, x_val in enumerate(fitting_test_x_vals):
        point_name=f"{x_val}_{fitting_test_y_vals[x_nr]}"#because of duplicate x-values the index must be a combination of x and y
        if(point_name not in func_ideal_keys):
            func_ideal[point_name]=f"y{ideal_func_num}"
            delta_ideal[point_name]=fitting_test_val_diffs[x_nr]
            x_vals[point_name]=x_val
            y_vals[point_name]=fitting_test_y_vals[x_nr]
        else:
            if(fitting_test_val_diffs[x_nr]<delta_ideal[point_name]):
                func_ideal[point_name]=f"y{ideal_func_num}"
                delta_ideal[point_name]=fitting_test_val_diffs[x_nr]
    
    #sort testdata by x-values for plotting (otherwise x vals might be in wrong order and by that plotting might result in a chaotic plot)
    fitting_test_x_vals, fitting_test_y_vals = data_manager.sort_multiple_arrays([fitting_test_x_vals,fitting_test_y_vals])
    
    #Plot to compare testdata with the current ideal function
    plt.figure(f"Test Data with ideal function {ideal_func_num}")
    plt.title(f"Test Data with ideal function {ideal_func_num}")
    plt.scatter(data_ideal_funcs["x"], data_ideal_funcs[f"y{ideal_func_num}"], label="ideal function data")
    plt.scatter(x_test, y_test, label="test data")
    plt.legend(loc="upper right")
    
    
    #Plot of the testdata with datapoints marked, which fit the current ideal function in sqrt(2) difference
    plt.figure(f"Test Data with datapoints fitting the ideal function {ideal_func_num}")
    plt.title(f"Test Data with datapoints fitting the ideal function {ideal_func_num}")
    plt.scatter(x_test, y_test, label="test data")
    plt.scatter(fitting_test_x_vals, fitting_test_y_vals, label="datapoints fitting the ideal function")
    plt.legend(loc="upper right")
    
#Because some testdatapoints might not match any ideal function, add the remaining data points
func_ideal_keys = list(func_ideal.keys())
for x_nr, x_val in enumerate(x_test):
    point_name=f"{x_val}_{y_test[x_nr]}"
    if(point_name not in func_ideal_keys):
        func_ideal[point_name]=""
        delta_ideal[point_name]=math.inf
        x_vals[point_name]=x_val
        y_vals[point_name]=y_test[x_nr]
    
#Sort all testdatavalues by order of their x-values
x_vals, y_vals, delta_ideal, func_ideal = data_manager.sort_multiple_arrays([np.array(list(x_vals.values())), np.array(list(y_vals.values())), 
                                                                             np.array(list(delta_ideal.values())), np.array(list(func_ideal.values()))])    

#Build resulttable
df_result=pd.DataFrame({"X":x_vals,"Y1":y_vals,"Delta Y":delta_ideal,"Nummer der Idealen Funktion":func_ideal})
print("Datenanalyse beendet.")

#Save resulttable in database if it does not already exist
if(not data_manager.table_exists("test_dat")):
    print("Ergebnis der Datenanalyse in der Datenbank speichern.")
    data_manager.create_new_database_table(df_result, "test_dat")
    
#Plot all testdatapoints and mark the datapoints by the idealfuction they match
plt.figure("Test Data with datapoints marked for each ideal function")
plt.title("Test Data with datapoints marked for each ideal function")
plt.scatter(x_test, y_test, label="test data")
colors=["green","orange","red","purple"]
func_nums = [num for num in list(set(df_result['Nummer der Idealen Funktion'].to_numpy())) if num != ""]
for nr, ideal_func_num in enumerate(func_nums):
    #Extract the rows of the resulttable, which match the specific ideal function
    result_df_part = df_result.loc[df_result['Nummer der Idealen Funktion'] == ideal_func_num]
    #Plot the datapoints which match the current ideal function
    temp_x_vals = result_df_part["X"].to_numpy()
    temp_y_vals = result_df_part["Y1"].to_numpy()
    plt.scatter(temp_x_vals, temp_y_vals, color=colors[nr], label=f"test data fitting ideal function {ideal_func_num}")
    plt.plot(temp_x_vals, temp_y_vals, color=colors[nr])
plt.legend(loc="upper right")

print("Programm beendet.")













