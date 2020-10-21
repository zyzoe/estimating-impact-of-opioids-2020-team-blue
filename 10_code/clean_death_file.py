#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


death_files = os.listdir("../00_source/US_VitalStatistics")
# death_files is a list of all the files we want to read in

# In[3]:


path = "../00_source/US_VitalStatistics/" 

# read in all file in a loop and concat them together to form the final mortality file
df_list = []
for f in death_files:
    df = pd.read_csv(path + f,
                 sep = "\t").drop(['Notes'], axis = 1)
    df.dropna(axis = 0, inplace = True)
    
    # split state and county
    df[["county", "state"]] = df.County.str.split(",", expand = True)
    
    # standardize county names
    df["county"] = df.county.str.strip("County").str.lower()
    
    # convert Year to datetime in pandas
    df["Year"] = pd.to_datetime(df["Year"], format = "%Y").dt.year
    
    # subset to get only drug overdoes related death
    df = df.loc[df["Drug/Alcohol Induced Cause"] == "Drug poisonings (overdose) Unintentional (X40-X44)"]
    
    # append dataframes
    df_list.append(df)
    df = pd.concat(df_list, ignore_index = True)
    


# In[4]:

# drop columns that we don't need
df = df.drop(["County", "County Code",  "Year Code", "Drug/Alcohol Induced Cause"], axis = "columns")


# In[5]:

# sort by year
df = df.sort_values(by = "Year")


# In[6]:


# df.to_csv("death_rate.csv", index = False)

