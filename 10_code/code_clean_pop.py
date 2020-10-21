#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as py


# In[2]:


source = pd.read_csv("data/county_pop_2000_to_2019.csv")


# In[3]:


source = source.drop('county_FIPS', axis=1)


# In[4]:


source


# In[5]:


source["county"] = source["county"].str.replace(" County","")
source["county"] = source["county"].str.lower()


# In[6]:


source


# In[7]:


cleaned_pop = source.melt(id_vars=['state', 'county'], var_name='year', value_name = "total_population")


# In[8]:


cleaned_pop


# In[9]:


cleaned_pop.isnull().sum() #No missing values


# In[10]:


cleaned_pop = cleaned_pop[cleaned_pop["state"] != 'Alaska'] #exclude Alaska


# In[11]:


cleaned_pop


# In[12]:


cleaned_pop.to_csv(r'cleaned_population.csv', index = False)

