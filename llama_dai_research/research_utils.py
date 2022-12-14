#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd

def llama_hist_circulating_stables(id:int):
    assert type(id) is int, 'stablecoin id should be an int'
    
    url = f'https://stablecoins.llama.fi/stablecoin/{id}'
    
    try:
        res = requests.get(url)
        res.raise_for_status()
        
        js = res.json()
        data = []

        for chain in js['chainBalances']:

            chain_data = [['date', 'circulating', 'minted', 'bridged_to']]

            for record in range(len(js['chainBalances'][chain]['tokens'])):

                date = js['chainBalances'][chain]['tokens'][record]['date']
                circulating = js['chainBalances'][chain]['tokens'][record]['circulating']['peggedUSD']
                minted = js['chainBalances'][chain]['tokens'][record]['minted']['peggedUSD']
                bridged_to = js['chainBalances'][chain]['tokens'][record]['bridgedTo']['peggedUSD']

                chain_data.append([date, circulating, minted, bridged_to])

            chain_df = pd.DataFrame(chain_data)
            chain_df.columns = chain_df.iloc[0]
            chain_df = chain_df.drop(0)
            chain_df['chain'] = chain
            chain_df['date'] = pd.to_datetime(chain_df['date'], unit = 's')
            chain_df.set_index('date', inplace = True)
            chain_df = chain_df.resample('D').last()
            chain_df = chain_df.reset_index()

            data.append(chain_df)

        stables_df = pd.concat(data, axis = 0)
        
        return stables_df
    
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

