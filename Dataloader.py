# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 08:28:39 2022

@author: olive
"""
from numpy import genfromtxt
from sqlalchemy import Column, Integer, Float, Date, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
from helper import Helper

class Data_manager(Helper):
    """
    Class to manage the database in- and outputs made with sqlalchemy
    as well as other data operations
    """
    
    def __init__(self):
        #Create the database
        self.engine = create_engine('sqlite:///data.db',echo=False)
        #Create the session
        self.sess_maker = sessionmaker()
        self.sess_maker.configure(bind=self.engine)
        self.db_session = self.sess_maker()      
        try:
            #if training-data table doesnt exist, read the csv file and add the data to the database
            if(not self.table_exists("train_dat")):
                df_train = pd.read_csv("train.csv")
                df_train.to_sql('train_dat', con=self.engine)
                self.db_session.commit() #Attempt to commit all the records
            #if ideal-model-data table doesnt exist, read the csv file and add the data to the database
            if(not self.table_exists("ideal_dat")):
                df_train = pd.read_csv("ideal.csv")
                df_train.to_sql('ideal_dat', con=self.engine)
                self.db_session.commit() #Attempt to commit all the records
        except Exception as e:
            self.db_session.rollback() #Rollback the changes on error
            raise Exception(e)
        return 
    
    
    def get_session(self):
        """
        Getter-function to get the database-session

        Returns
        -------
        sqlalchemy.orm.session.Session
            Current database-session

        """
        return self.db_session
    
    
    def get_data_from_table_as_dataframe(self, table_name, column_name="*"):
        """
        Function to get data out of a given table.

        Parameters
        ----------
        table_name : String
            DESCRIPTION.
        column_name : String, optional
            Which Column of the table should be returned. The default is "*".
            To return all columns use *, otherwise give the name of a specific column
            or give multiple column names separated by ","

        Returns
        -------
        pandas dataframe
            Returns is a pandas dataframe containing the data from one or multiple columns of the selected table.

        """
        return pd.read_sql(f"SELECT {column_name} FROM {table_name}", self.db_session.bind)
    
    
    def table_exists(self, tablename):
        """
        Helper function to check if the table "tablename" exists in the database

        Parameters
        ----------
        tablename : String
            Tablename that should be checked

        Returns
        -------
        Boolean
            True=table exists, False=table doesnt exist

        """
        return inspect(self.engine).has_table(tablename)
        