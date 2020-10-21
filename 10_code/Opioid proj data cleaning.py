#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
#state_list = ['AL','AZ','AR','CA','CO','CT','DE','DC','FL','HI','GA','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI',
#             'MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NV','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT',
#              'VT','VA','WA','WV','WI','WY']


# #### Specify the regions 

# In[ ]:


northeast = ['CT','ME','MA','NH','RI','VT','NJ','NY','PA']
midwest = ['IL','IN','MI','OH','WI','IA','KS','MN','MO','NE','ND','SD']
south_1 = ['DE','FL','GA','MD','NC','SC','VA','WV']
south_2 = ['AL','KY','MS','TN','AR','LA','OK','TX']
west = ['AZ','CO','ID','MT','NV','NM','UT','WY','CA','HI','OR','WA']


# In[ ]:


# Read in data, set chuncksize
opioid = pd.read_csv("dataset/arcos_all_washpost.tsv.gz", compression = 'gzip',sep = '\t',
                     chunksize = 1000000, low_memory = False,
                    usecols=['BUYER_STATE', 'BUYER_COUNTY','TRANSACTION_DATE','CALC_BASE_WT_IN_GM','MME_Conversion_Factor'])


# In[ ]:


# northeast_data = pd.concat([chunk[chunk['BUYER_STATE'].isin(northeast)] for chunk in opioid])
# del northeast_data


# In[ ]:


# midwest_data = pd.concat([chunk[chunk['BUYER_STATE'].isin(midwest)] for chunk in opioid])
# del midwest_data


# In[ ]:


# south_1_data = pd.concat([chunk[chunk['BUYER_STATE'].isin(south_1)] for chunk in opioid])
# del south_1_data


# In[ ]:


# south_2_data = pd.concat([chunk[chunk['BUYER_STATE'].isin(south_2)] for chunk in opioid])
# del south_2_data


# In[ ]:


# west_data = pd.concat([chunk[chunk['BUYER_STATE'].isin(west)] for chunk in opioid])
# del west_data


# #### Function def

# In[ ]:


def clean_opioid_data(df):
    # 2. Data tranformation on TRANSACTION_DATE
    ## 2.1 Transform TRANSACTION_DATE into datetime type
    df["TRANSACTION_DATE"] = pd.to_datetime(df["TRANSACTION_DATE"], format = "%m%d%Y")
    ## 2.2 Expand TRANSACTION_DATE into Year & Month
    df['Year'] = df['TRANSACTION_DATE'].dt.year
    df['Month'] = df['TRANSACTION_DATE'].dt.month
    ## 2.3 Drop TRANSACTION_DATE
    df = df.drop(columns=['TRANSACTION_DATE'])
    
    
    # 3. Calculate opioid weight per shipment
    ## 3.1 Standardize opioid weight
    df['weight'] = df['CALC_BASE_WT_IN_GM']*df['MME_Conversion_Factor']
    ## 3.2 Change variable names, drop cols CALC_BASE_WT_IN_GM,MME_Conversion_Factor
    df = df.rename(columns={'BUYER_COUNTY':'county','BUYER_STATE':'state'}).drop(columns=['CALC_BASE_WT_IN_GM','MME_Conversion_Factor'])
    df.county = df.county.str.lower()
    
    
    # 4. Groupby state, county per month, per year
    df_clean = df.groupby(['state','county','Year','Month'])['weight'].sum().reset_index()
    df_clean.weight = df_clean.weight.round(2)
    
    return df_clean
    


# In[ ]:


west_clean = clean_opioid_data(west_data)


# In[ ]:


west_clean.to_csv("west.csv", index = False)


# In[3]:


# Import cleaned datasets
nor_mid = pd.read_csv('nor_mid.csv')
south = pd.read_csv('south.csv')
west = pd.read_csv('west.csv')


# In[4]:


opioids_clean = pd.concat([nor_mid,south,west])


# In[ ]:


opioids.to_csv("west.csv", index = False)


# In[ ]:


get_ipython().system('conda install -c conda-forge python-snappy fastparquet snappy')


# In[7]:


opioids_clean.to_parquet('prescription.parquet', engine='fastparquet')

