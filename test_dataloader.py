# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 18:16:51 2022

@author: Oliver
"""

import unittest
import os
import numpy as np
import pandas as pd
from helper import Helper
from datamanager import Data_manager

class Helpertests(unittest.TestCase):
    
    test_list1 = np.array([1, 6, 8, 3, 7, 7, 5, 3, 6, 3, 5, 7, 1, 2, 8, 6, 2, 9, 3, 9])
    test_list2 = np.array([5, 7, 5, 3, 8, 4, 0, 8, 1, 3, 5, 1, 8, 8, 9, 3, 6, 6, 5, 6])
    test_list3 = np.array([3, 1, 8, 9, 6, 0, 6, 4, 1, 4, 6, 3, 4, 2, 2, 9, 8, 9, 0, 1])
    test_list4 = np.array([3, 9, 3, 4, 1, 3, 9, 5, 7, 4, 7, 8, 5, 2, 9, 8, 7, 3, 8, 3])
    
    def test_init(self):
        self.assertFalse(os.path.isfile("test_data.db"))
        dmanager = Data_manager("test_data")
        self.assertTrue(os.path.isfile("test_data.db"))
        try:
            os.remove("test_data.db")
        except OSError:
            pass
        return
    
    
    def test_get_table_names(self):
        dmanager = Data_manager("test_data")
        table_names = dmanager.get_table_names()
        self.assertEqual(table_names, ["ideal_dat","train_dat"])
        try:
            os.remove("test_data.db")
        except OSError:
            pass
        return
    
    
    def test_get_data_from_table_as_dataframe(self):
        dmanager = Data_manager("test_data")
        table_train = dmanager.get_data_from_table_as_dataframe("train_dat")
        self.assertEqual(len(table_train), 400)
        column_names = ['index', 'x', 'y1', 'y2', 'y3', 'y4']
        self.assertEqual(list(table_train.columns), column_names)
        table_ideal = dmanager.get_data_from_table_as_dataframe("ideal_dat")
        self.assertEqual(len(table_ideal), 400)
        column_names = ['index', 'x', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7', 'y8', 'y9', 'y10', 'y11', 'y12', 'y13', 'y14', 'y15', 'y16', 'y17', 'y18', 'y19', 'y20', 
                        'y21', 'y22', 'y23', 'y24', 'y25', 'y26', 'y27', 'y28', 'y29', 'y30', 'y31', 'y32', 'y33', 'y34', 'y35', 'y36', 'y37', 'y38', 'y39', 'y40', 'y41', 
                        'y42', 'y43', 'y44', 'y45', 'y46', 'y47', 'y48', 'y49', 'y50']
        self.assertEqual(list(table_ideal.columns), column_names)
        
        try:
            os.remove("test_data.db")
        except OSError:
            pass
        return
    
    
    def test_table_exists(self):
        dmanager = Data_manager("test_data")
        table_names = dmanager.get_table_names()
        for name in table_names:
            self.assertTrue(dmanager.table_exists(name))
        self.assertFalse(dmanager.table_exists("wrong name"))
        self.assertFalse(dmanager.table_exists("wrong name 2"))
        try:
            os.remove("test_data.db")
        except OSError:
            pass
        return
        

    def test_create_new_database_table(self):
        dmanager = Data_manager("test_data")
        self.assertFalse(dmanager.table_exists("test_name"))
        test_df = pd.DataFrame({"test_list1":self.test_list1,"test_list2":self.test_list2,"test_list3":self.test_list3,"test_list4":self.test_list4})
        dmanager.create_new_database_table(test_df,"test_name")
        self.assertTrue(dmanager.table_exists("test_name"))
        try:
            os.remove("test_data.db")
        except OSError:
            pass
        return
    
    
if __name__ == '__main__':
    unittest.main()