import pandas as pd
import matplotlib.pyplot as plt
import yaml

def load_params():
    
    with open('co2_emissions.yaml') as file:
        
        params = yaml.load(file)
        for key in params:
            params[key]=float(params[key])
        print(params)
        
    return pd.Series(params)

def analyse_and_plot_demand():
    rel_load_per_ctr = pd.DataFrame()
    
    for country_code in ['DE-LU','BE','DK','AT','BG','CH','CZ','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','NL','NO','PL','PT','RO','SE']:

        try:
            data = pd.read_csv('load_'+country_code+'.csv',index_col=0,header=None)
            data['weekday']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').dayofweek
            data['week']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').week
            data['month']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').month
            data['year']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').year
            data['days in month']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').days_in_month

            #calculate relative monthly change 2020 over 2019
            d1 = data[data['year']==2020].groupby('month').sum().sum(axis=1)
            d2 = data[data['year']==2019].groupby('month').sum().sum(axis=1)
            d3 = (d1-d2)/d2
            rel_load_per_ctr[country_code]=d3
            
        except:
            print('error')
            
    rel_load_per_ctr.iloc[3].plot.bar(title='relative demand',grid=True)
    plt.tight_layout()
    plt.savefig('rel_demand.pdf')

def analyse_and_plot_emissions():
    rel_emiss_per_ctr = pd.DataFrame()
    
    params=load_params()
    
    for country_code in ['DE-LU','BE','DK','AT','BG','CH','CZ','EE','ES','FI','FR','GB','GR','HR','HU','IE','IT','NL','NO','PL','PT','RO','SE']:


        try:
            data = pd.read_csv('gen'+country_code+'.csv',index_col=0)
            #convert to co2 emissions
            data=data*params
            
            data['weekday']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').dayofweek
            data['week']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').week
            data['month']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').month
            data['year']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').year
            data['days in month']=pd.to_datetime(data.index,utc=True).tz_convert(tz='Europe/Berlin').days_in_month

            d1 = data[data['year']==2020].groupby('month').sum().sum(axis=1)
            d2 = data[data['year']==2019].groupby('month').sum().sum(axis=1)
            d3 = (d1-d2)/d2
            
            rel_emiss_per_ctr[country_code] = d3
            
        except:
            print('error')
            
    rel_emiss_per_ctr.iloc[3].plot.bar(title='relative carbon dioxide emissions',grid=True)
    plt.tight_layout()
    plt.savefig('rel_emissions.pdf')
