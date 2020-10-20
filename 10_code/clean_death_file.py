#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# In[2]:


death_files = os.listdir("../00_source/US_VitalStatistics")


# In[3]:


path = "../00_source/US_VitalStatistics/" 
df_list = []
for f in death_files:
    df = pd.read_csv(path + f,
                 sep = "\t").drop(['Notes'], axis = 1)
    df.dropna(axis = 0, inplace = True)
    df[["county", "state"]] = df.County.str.split(",", expand = True)
    df["county"] = df.county.str.strip("County").str.lower()
    df["Year"] = pd.to_datetime(df["Year"], format = "%Y").dt.year
    df = df.loc[df["Drug/Alcohol Induced Cause"] == "Drug poisonings (overdose) Unintentional (X40-X44)"]
    df_list.append(df)
    df = pd.concat(df_list, ignore_index = True)
    


# In[4]:


df = df.drop(["County", "County Code",  "Year Code", "Drug/Alcohol Induced Cause"], axis = "columns")


# In[5]:


df = df.sort_values(by = "Year")


# In[6]:


# df.to_csv("death_rate.csv", index = False)

