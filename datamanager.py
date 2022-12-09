# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 08:28:39 2022

@author: Oliver
"""
from sqlalchemy import inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from helper import Helper

class Data_manager(Helper):
    """
    Class to manage the database in- and outputs made with sqlalchemy
    as well as other data operations
    """
    
    def __init__(self, db_file_name="data"):
        """
        Init of the Data_manager-Class

        Parameters
        ----------
        db_file_name : String, optional
            Name of the Database-File, in which all tables should be saved and 
            from which all data will be loaded. The default is "data".

        Returns
        -------
        None.

        """
        
        #Create the database
        self.engine = create_engine(f'sqlite:///{db_file_name}.db', echo=False)
        #Create the session
        self.sess_maker = sessionmaker()
        self.sess_maker.configure(bind=self.engine)
        self.db_session = self.sess_maker() 
        #if training-data table doesnt exist, read the csv file and add the 
         #data to the database
        if(not self.table_exists("train_dat")):
            df = pd.read_csv("rawdata/train.csv")
            self.create_new_database_table(df, 'train_dat')
        #if ideal-model-data table doesnt exist, read the csv file and add 
         #the data to the database
        if(not self.table_exists("ideal_dat")):
            df = pd.read_csv("rawdata/ideal.csv")
            self.create_new_database_table(df, 'ideal_dat')
        return 
    
    
    def get_table_names(self):
        """
        Getter-function to get the database table_names

        Returns
        -------
        list of strings

        """
        return self.engine.table_names()
    
    
    def get_data_from_table_as_dataframe(self, table_name, column_name="*"):
        """
        Function to get data out of a given table.

        Parameters
        ----------
        table_name : String
            DESCRIPTION.
        column_name : String, optional
            Which Column of the table should be returned. The default is "*".
            To return all columns use *, otherwise give the name of a 
            specific column or give multiple column names separated by ","

        Raises
        ------
        ValueError
            If table_name or column_name is invalid.

        Returns
        -------
        pandas dataframe
            Returns is a pandas dataframe containing the data from one or 
            multiple columns of the selected table.

        """
        if(self.table_exists(table_name)):
            db_table = pd.read_sql(f"SELECT * FROM {table_name}",
                                   self.db_session.bind)
            if(column_name=="*"):
                return db_table#All columns
            elif(type(column_name)!=list and column_name in list(db_table.columns)):
                return db_table[column_name]#One specific column
            elif(type(column_name)==list and all([name in list(db_table.columns) 
                                                  for name in column_name])):
                return db_table[column_name]#Multiple specific columns
            else:
                raise ValueError(f"""The table {table_name} does not have the 
                                   column(s) {column_name}.""")
        else:
            raise ValueError(f"""The table {table_name} does not exist in the 
                               database.""")
    
    
    def table_exists(self, table_name):
        """
        Function to check if the table "table_name" exists in the database

        Parameters
        ----------
        table_name : String
            table_name that should be checked

        Returns
        -------
        Boolean
            True=table exists, False=table doesnt exist

        """
        return inspect(self.engine).has_table(table_name)
        
    
    def create_new_database_table(self, dataframe, table_name):
        """
        Function to create a new table to the database using a pandas dataframe

        Parameters
        ----------
        dataframe : pandas dataframe
            Dataframe with the data that should be added as table into the 
            database.
        table_name : String
            Name under which the table should be added to the database

        Returns
        -------
        None.

        """
        #add the table if no table with this name exists
        if(not self.table_exists(table_name)):
            dataframe.to_sql(table_name, con=self.engine)
            self.db_session.commit() #Attempt to commit all the records
        return