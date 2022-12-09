# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 06:11:55 2022

@author: Oliver
"""

import pandas as pd
import numpy as np
import math
import csv
import matplotlib
import matplotlib.pyplot as plt
from datamanager import Data_manager


font = {'weight' : 'bold',
        'size'   : 30}
matplotlib.rc('font', **font)


data_manager = Data_manager()
#load csv with testdata
x_test = []
y_test = []
with open("rawdata/test.csv", "r") as f:
    reader = csv.reader(f)
    for i, line in enumerate(reader):
        if(i!=0):
            x_test.append(line[0])
            y_test.append(line[1])
#convert x and y lists to numpy arrays for easier value extraction later on
x_test=np.array(x_test).astype(float)
y_test=np.array(y_test).astype(float)

print("Daten aus der Datenbank laden.")
#load trainingdata and ideal functions from database
training_data = data_manager.get_data_from_table_as_dataframe("train_dat")
data_ideal_funcs = data_manager.get_data_from_table_as_dataframe("ideal_dat")

print("Datenanalyse starten.")
delta_ideal={}#dictionary containing the lowest differences between ideal 
               #function and test datapoint values
func_ideal={}#dictionary containing the ideal function numbers that fit each 
              #specific testdatapoint best
x_vals={}#dictionary containing testdata x-values
y_vals={}#dictionary containing testdata y-values

#for every training y-dataset
for y_nr_train in range(1,5):
    #Aufgabe 1.1.1
    ideal_func_num = 0
    ideal_func_diff_value = math.inf
    for y_nr_ideal in range(1, 51):
        temp_diff = data_manager.calculate_squared_difference(
                                 training_data[f"y{y_nr_train}"], 
                                 data_ideal_funcs[f"y{y_nr_ideal}"])
        if(temp_diff < ideal_func_diff_value):
            ideal_func_num = y_nr_ideal
            ideal_func_diff_value = temp_diff
    
    #Plot of trainingsdata and the determined ideal function
    plt.figure(f"Training Data {y_nr_train} with ideal function {ideal_func_num}")
    plt.title(f"Training Data {y_nr_train} with ideal function {ideal_func_num}")
    plt.scatter(training_data["x"], training_data[f"y{y_nr_train}"], 
                label="Training data",s=64)
    plt.scatter(data_ideal_funcs["x"], data_ideal_funcs[f"y{ideal_func_num}"], 
                label="Ideal function data",s=64)
    plt.legend(loc="upper right")
    
    #Aufgabe 1.1.2 a
    #check which testdata values lie within sqrt(2) range around the current 
     #ideal function
    y_ideal_for_test_data = []
    value_diffs = []
    value_check_sqrt2 = []
    for nr, value in enumerate(y_test):
        y_ideal_for_test_data.append(data_ideal_funcs.loc[
                                     data_ideal_funcs['x'] == x_test[nr]
                                     ][f"y{ideal_func_num}"].to_numpy()[0])
        value_diffs.append(abs(value - y_ideal_for_test_data[-1]))
        value_check_sqrt2.append(value_diffs[-1] < math.sqrt(2))
    value_diffs = np.array(value_diffs)
    
    #get the testdata values within sqrt(2) range around the current ideal 
     #function
    fitting_test_x_vals = x_test[value_check_sqrt2]
    fitting_test_y_vals = y_test[value_check_sqrt2]
    fitting_test_val_diffs = value_diffs[value_check_sqrt2]
    
    #Aufgabe 1.1.2 b
    #if the current ideal function fits testdata values best, save that 
     #testdata values with reference to the current ideal function
    func_ideal_keys = func_ideal.keys()
    for x_nr, x_val in enumerate(fitting_test_x_vals):
        #because of duplicate x-values the index must be a combination of x and y
        point_name=f"{x_val}_{fitting_test_y_vals[x_nr]}"
        if(point_name not in func_ideal_keys):
            func_ideal[point_name]=f"y{ideal_func_num}"
            delta_ideal[point_name]=fitting_test_val_diffs[x_nr]
            x_vals[point_name]=x_val
            y_vals[point_name]=fitting_test_y_vals[x_nr]
        else:
            if(fitting_test_val_diffs[x_nr]<delta_ideal[point_name]):
                func_ideal[point_name]=f"y{ideal_func_num}"
                delta_ideal[point_name]=fitting_test_val_diffs[x_nr]
    
    #sort testdata by x-values for plotting (otherwise x vals might be in wrong 
     #order and by that plotting might result in a chaotic plot)
    fitting_test_x_vals, fitting_test_y_vals = data_manager.sort_multiple_arrays(
                                                            [fitting_test_x_vals,
                                                             fitting_test_y_vals])
    
    #Plot to compare testdata with the current ideal function
    plt.figure(f"Test Data with ideal function {ideal_func_num}")
    plt.title(f"Test Data with ideal function {ideal_func_num}")
    plt.scatter(data_ideal_funcs["x"], data_ideal_funcs[f"y{ideal_func_num}"], 
                label="Ideal function data",s=64)
    plt.scatter(x_test, y_test, label="Test data",s=64)
    plt.legend(loc="upper right")
    
    
    #Plot of the testdata with datapoints marked, which fit the current ideal 
     #function in sqrt(2) difference
    plt.figure(f"Test Data with datapoints fitting the ideal function {ideal_func_num}")
    plt.title(f"Test Data with datapoints fitting the ideal function {ideal_func_num}")
    plt.scatter(x_test, y_test, label="Test data",s=64)
    plt.scatter(fitting_test_x_vals, fitting_test_y_vals, 
                label="Datapoints fitting the ideal function",s=64)
    plt.legend(loc="upper right")
    
#Because some testdatapoints might not match any ideal function, 
 #add the remaining data points
func_ideal_keys = func_ideal.keys()
for x_nr, x_val in enumerate(x_test):
    point_name=f"{x_val}_{y_test[x_nr]}"
    if(point_name not in func_ideal_keys):
        func_ideal[point_name]=""
        delta_ideal[point_name]=math.inf
        x_vals[point_name]=x_val
        y_vals[point_name]=y_test[x_nr]

#Sort all testdatavalues by order of their x-values. Otherwise the plots might 
 #be messed up because of the random x value order of the testdata
x_vals, y_vals, delta_ideal, func_ideal = data_manager.sort_multiple_arrays(
                                          [np.array(list(x_vals.values())), 
                                           np.array(list(y_vals.values())), 
                                           np.array(list(delta_ideal.values())), 
                                           np.array(list(func_ideal.values()))])    

#Build resulttable
df_result=pd.DataFrame({"X":x_vals,"Y1":y_vals,"Delta Y":delta_ideal,
                        "Nummer der Idealen Funktion":func_ideal})
print("Datenanalyse beendet.")

#Save resulttable in database if it does not already exist
if(not data_manager.table_exists("test_dat")):
    print("Ergebnis der Datenanalyse in der Datenbank speichern.")
    data_manager.create_new_database_table(df_result, "test_dat")
    
#Plot all testdatapoints and mark the datapoints by the idealfuction they match
plt.figure("Test Data with datapoints marked for each ideal function")
plt.title("Test Data with datapoints marked for each ideal function")
plt.scatter(x_test, y_test, label="Test data fitting no ideal function",s=64)
colors=["green","orange","red","purple"]
func_nums = np.array([num for num in list(set(
                     df_result['Nummer der Idealen Funktion'].to_numpy())) 
                     if num != ""])
#sort the ideal function names, so that they will be displayed in descending 
 #order in the plot legend
func_nums = data_manager.sort_multiple_arrays([np.array([int(val[1:]) 
                                               for val in func_nums]), 
                                               func_nums])[1]
for nr, ideal_func_num in enumerate(func_nums):
    #Extract the rows of the resulttable, which match the specific ideal function
    result_df_part = df_result.loc[df_result['Nummer der Idealen Funktion'] 
                                   == ideal_func_num]
    #Plot the datapoints which match the current ideal function
    temp_x_vals = result_df_part["X"].to_numpy()
    temp_y_vals = result_df_part["Y1"].to_numpy()
    plt.scatter(temp_x_vals, temp_y_vals, color=colors[nr], 
                label=f"Test data fitting ideal function {ideal_func_num}",s=64)
    plt.plot(temp_x_vals, temp_y_vals, color=colors[nr], linewidth=4)
plt.legend(loc="upper right")

print("Programm beendet.")