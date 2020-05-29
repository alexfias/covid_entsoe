from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt

#download load and generation data from the entso-e platform

#enter your own api_key 
client = EntsoePandasClient(api_key="")

ts = pd.DataFrame()
ts2 = pd.DataFrame()

start,end = pd.Timestamp('20190101', tz='Europe/Brussels'),pd.Timestamp('20190501', tz='Europe/Brussels')
start2,end2 = pd.Timestamp('20200101', tz='Europe/Brussels'),pd.Timestamp('20200501', tz='Europe/Brussels')


for country_code in ['DE-LU','BE','DK','AT','BG','CH','CZ','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','NL','NO','PL','PT','RO','SE']:
    
    try:
	
	#download load data
	pd.concat([client.query_load(country_code, start=start,end=end),client.query_load(country_code, start=start2,end=end2)]).to_csv('./data/load_'+country_code+'.csv')
	#download generation data
        pd.concat([client.query_generation(country_code, start=start,end=end, psr_type=None),client.query_generation(country_code, start=start2,end=end2, psr_type=None)]).to_csv('./data/gen'+country_code+'.csv')

        
    except: 
        
        print('an error occured, country code: ',country_code)
