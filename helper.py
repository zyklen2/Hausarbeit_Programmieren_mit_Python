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
    
    def calculate_squared_difference(self, list1, list2):
        """
        Function to calculate the sum of the squared differences between the values of two lists of equal length

        Parameters
        ----------
        list1 : list of floats
        list2 : list of floats
            
        Raises
        ------
        ValueError
            if the lenth of list1 is not equal to the length of list2

        Returns
        -------
        float
            sum of the squared differences of the values of the two lists

        """
        if(len(list1) == len(list2)):
            differences = []
            for nr, val in enumerate(list1):
                differences.append((val - list2[nr])**2)
            return sum(differences)
        else:
            raise ValueError(f"Length of list1 ({len(list1)}) is not equal to the length of list2 ({len(list2)})")
            
        
        
    def sort_multiple_arrays(self, list_of_arrays, array_to_sort_after=None, as_list=True):
        """
        Function to sort multiple arrays by the order of items of another given array

        Parameters
        ----------
        list_of_arrays : list of arrays
            arrays that are to be sorted, with the same length as array_to_sort_after
        array_to_sort_after : optional, array of floats
            If its None, the first array of list_of_arrays will be used instead.
            Array that is to be used to sort the other arrays. 
        as_list : boolean
            if the return of this function should be a list or tuple

        Returns
        -------
        list or tuple depending on parameter "as_list"
            the sorted versions of the arrays given by list_of_arrays

        """
        #Reihenfolge der Werte bestimmen
        if(array_to_sort_after is None):
            sorting_indices = np.argsort(list_of_arrays[0])
        else:
            sorting_indices = np.argsort(array_to_sort_after)
        #Arrays sortieren und zurueckgeben
        if(as_list):
            return [array[sorting_indices] for array in list_of_arrays]
        else:
            return tuple([array[sorting_indices] for array in list_of_arrays])
            
            
            
            