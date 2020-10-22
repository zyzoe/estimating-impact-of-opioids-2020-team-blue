#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[65]:


pop = pd.read_csv("cleaned_population.csv")
death_rate = pd.read_csv("death_rate.txt")
opioids = pd.read_csv("opioids_clean.txt")
opioids_year = opioids.groupby(["Year","state","county"]).sum()['weight'].reset_index()
death_rate["state"] = death_rate["state"].str.lstrip()
death_rate["county"] = death_rate["county"].str.rstrip()
death_rate = death_rate[(death_rate["state"] != "DC") | (death_rate["state"] != "AK")]


# In[47]:


pop = pop[(pop["Year"]>=2003) & (pop["Year"] <= 2015)]


# In[48]:


len(death_rate["county"].unique())


# In[49]:


len(pop["county"].unique())


# In[50]:


len(opioids["county"].unique())


# In[51]:


pop


# In[52]:


merge = pop.merge(opioids_year, on = ["Year", "state", "county"], how = "left", validate = "many_to_one")


# In[53]:


merge.shape


# In[ ]:





# In[54]:


final = pd.merge(merge, death_rate, on = ["state", "county", "Year"], how = "left", indicator = True)


# In[55]:


final[final["_merge"] == "both"]


# In[56]:


death_rate.shape


# In[57]:


death_rate[death_rate["state"] == "AK"].shape


# In[58]:


death_rate[death_rate["state"] == "DC"].shape


# In[59]:


set(death_rate["county"]) - set(final[final["_merge"] == "both"]["county"])


# In[ ]:





# In[ ]:




