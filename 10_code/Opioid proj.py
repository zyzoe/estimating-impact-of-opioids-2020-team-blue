#!/usr/bin/env python
# coding: utf-8

# #### Import data

# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


### Try open file through url, failed

#import pandas as pd
#import io
#import requests
#url="https://d2ty8gaf6rmowa.cloudfront.net/dea-pain-pill-database/bulk/arcos_all_washpost.tsv.gz"
#s=requests.get(url).content
#c=pd.read_csv(io.StringIO(s.decode('utf-8')),compression='gzip',nrows=10,sep='\t')

#import pandas as pd
#url="https://d2ty8gaf6rmowa.cloudfront.net/dea-pain-pill-database/bulk/arcos_all_washpost.tsv.gz"
#c=pd.read_csv(url,compression='gzip',nrows=10, sep='\t')


# In[ ]:


# Specify the state to use, excluding Alaska
state_list = ['AL','AZ','AR','CA','CO','CT','DE','DC','FL','HI','GA','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI',
             'MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NV','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT',
              'VT','VA','WA','WV','WI','WY']


# In[ ]:


# We will need to split data into 3 subsets - based on geographical location?


# In[ ]:


# Read in data, set chuncksize
opioid = pd.read_csv("dataset/arcos_all_washpost.tsv.gz", compression = 'gzip',sep = '\t',
                     chunksize = 1000000, low_memory = False,
                    usecols=['BUYER_STATE', 'BUYER_COUNTY','TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor'])


# In[ ]:


# Nathan's method
# FL_data = pd.concat([chunk[chunk['BUYER_STATE'] == "FL"] for chunk in opioid])


# In[ ]:


# Transform `TRANSACTION_DATE` into datetime type 
opioid["TRANSACTION_DATE"] = pd.to_datetime(opioid["TRANSACTION_DATE"], format = "%m%d%Y")


# In[ ]:


df = pd.DataFrame()

for i in opioid:
    #i["TRANSACTION_DATE"] = pd.to_datetime(i["TRANSACTION_DATE"], format = "%m%d%Y")
    df = df.append(i.loc[i['BUYER_STATE'].isin(state_list)])
    


# In[ ]:


df.head()


# In[ ]:


# Check the cols we will need
# BUYER_DEA_NO, BUYER_STATE, BUYER_COUNTY(only name, to_lower)
# TRANSACTION_DATE(2 col, month,year)
# groupby county, merge state & county

