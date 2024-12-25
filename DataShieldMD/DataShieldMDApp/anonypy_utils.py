import pandas as pd
import anonypy
import numpy as np

'''
This file is used to properly apply the selected privacy algorithms to a specified dataset.

We are using the anonypy libary's implemention of these algorithm, so I ensure we are propely applying those methods.
'''

'''
Reads the dataset from a CSV file and prepares it for anonymization.
    
Args:
    data_path (str): Path to the input CSV file.
    sensitive_fields (list): List of columns considered sensitive.
    
Returns:
    - data (pd.DataFrame): The loaded dataset with categorical columns converted.
    - columns (list): A list of all column names in the dataset
'''
def read_data(data_path, sensitive_fields,):
    #Reading the file into a Pandas DataFrame
    data = pd.read_csv(data_path)
    categorical = set()
    columns = []
    
    #Looping through columns in DataFrame and if they are not numeric we are adding them to the categorical set.
    for column in data.columns:
        columns.append(column)
        if not pd.api.types.is_numeric_dtype(data[column]):
            categorical.add(column)
    
    #All categorical columns get converted to "category" datatype for proper processing     
    for column in categorical:
        data[column] = data[column].astype('category')
    
    #Return the DataFrame and all columns with types correctly applied 
    return data, columns

"""
Applies K-Anonymity to the dataset.

Args:
    data_path (str): Path to the input dataset.
    sensitive_fields (str): A the senstive colum name.
    k (int): The K value for K-Anonymity.
    output_path (str): Path to save the anonymized dataset.

Returns:
    nothing but saves processed file to specified output path
"""
def apply_k_anonymity(data_path,sensitive_fields, k,output_path):
    
    #Read and prepare data, then apply K-anonymity with specifed K value
    data , columns = read_data(data_path,sensitive_fields)
    p = anonypy.Preserver(data, columns, sensitive_fields)
    rows = p.anonymize_k_anonymity(k)

    #Convert output to a dataframe and remove count column created during processing.
    #Then save data frame as csv file to specified output_path
    dfn = pd.DataFrame(rows)
    dfn.drop(["count"],axis=1, inplace=True)
    dfn.to_csv(output_path, index=False)

"""
Applies L-Diversity to the dataset.

Args:
    data_path (str): Path to the input dataset.
    sensitive_fields (str): A the senstive colum name.
    k (int): The K value for L-Diversity.
    l (int): The L value for L-Diversity.
    output_path (str): Path to save the anonymized dataset.

Returns:
    nothing but saves processed file to specified output path
"""
def apply_l_diversity(data_path,sensitive_fields,k,l,output_path):
    #If no K value is provided default it to same value as L
    if k == None:
        k = l
    
    #Read and prepare data, then apply L-Diversity with specifed K and L values
    data , columns = read_data(data_path,sensitive_fields)
    p = anonypy.Preserver(data, columns, sensitive_fields)
    rows = p.anonymize_l_diversity(k,l)
    
    #Convert output to a dataframe and remove count column created during processing.
    #Then save data frame as csv file to specified output_path
    dfn = pd.DataFrame(rows)
    dfn.drop(["count"],axis=1, inplace=True)
    dfn.to_csv(output_path, index=False)
    
"""
Applies T-Closeness to the dataset.

Args:
    data_path (str): Path to the input dataset.
    sensitive_fields (str): A the senstive colum name.
    k (int): The K value for T-Closeness.
    t (int): The T value for T-Closeness.
    output_path (str): Path to save the anonymized dataset.

Returns:
    nothing but saves processed file to specified output path
"""
def apply_t_closeness(data_path, sensitive_fields, k, t, output_path):

    #Read and prepare data, then apply T-Closeness with specifed K and T values
    data , columns = read_data(data_path,sensitive_fields)
    p = anonypy.Preserver(data, columns, sensitive_fields)
    rows = p.anonymize_t_closeness(k,t)
    
    #Convert output to a dataframe and remove count column created during processing.
    #Then save data frame as csv file to specified output_path
    dfn = pd.DataFrame(rows)
    dfn.drop(["count"],axis=1, inplace=True)
    dfn.to_csv(output_path, index=False)
    
    
