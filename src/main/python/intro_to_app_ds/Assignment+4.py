
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[115]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[116]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[117]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    df = pd.read_csv('university_towns.txt', sep='\n', header=None)

    df['split'] = df[0].str.split('(', expand=True)[0]
    df['State'] = df.loc[df.split.str.contains('[edit]', regex=False), 'split'].str.extract(r'(.*?)\[edit\]', expand=False)

    df['RegionName'] = df['split'].astype(str).map(lambda x: x if '[edit]' not in x else '')
    df['RegionName'] = df['RegionName'].str.strip()

    df['State'] = df['State'].fillna(method='ffill')
    df = df[df.RegionName != '']

    df = df[['State', 'RegionName']]
#     df.set_index(['State', 'RegionName'], inplace=True)
    return df


get_list_of_university_towns()


# In[118]:

def read_gdp():
    xl = pd.ExcelFile("gdplev.xls", sheetname=0)
    cols=['annual', 'GDP in billions of current dollars 1', 'GDP in billions of chained 2012 dollars 1','empty1', 
          'quarterly', 'GDP in billions of current dollars 2', 'GDP in billions of chained 2012 dollars 2', 'empty2']
    
    df = xl.parse("Sheet1", header=6, names=cols, converters={'annual':str, 'GDP in billions of current dollars 1':str, 
                'GDP in billions of chained 2012 dollars 1':str,'empty1':str, 'quarterly':str, 
                'GDP in billions of current dollars 2':str, 
                'GDP in billions of chained 2012 dollars 2':str, 'empty2':str})
    df.head()
    
    del df['empty1']
    del df['empty2']
    
    # remove fields not needed
    del df['annual']
    del df['GDP in billions of current dollars 1']
    del df['GDP in billions of chained 2012 dollars 1']
    del df['GDP in billions of current dollars 2']
    
    # derive year and quarter cols
    df['quarterly_year'] = df['quarterly'].str.slice(0, 4)
    df['quarterly_qtr'] = df['quarterly'].str.slice(4, 6)
    
    # filter by year
    df = df[df['quarterly_year'].astype(int) > 1999]
    
    # calculate GDP change
    df['gdp_change'] = df['GDP in billions of chained 2012 dollars 2'] - df['GDP in billions of chained 2012 dollars 2'].shift(+1)
    
    return df

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    df = read_gdp()
    
    # infer recession start
    df['recession_start'] = (df['gdp_change'] < 0) & (df['gdp_change'].shift(-1) < 0)
    
    # return quarter for first occurence recession start equals True
    return df[df['recession_start'] == True].iloc[0]['quarterly']


get_recession_start()


# In[119]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    df = read_gdp()
    
    df['recession_start'] = (df['gdp_change'] < 0) & (df['gdp_change'].shift(-1) < 0)
    
    # get last recession quarter
    recession_end = df.loc[df['recession_start'] == True].iloc[-1]['quarterly']
    
    # return first quarter after recession end
    return df.loc[df[df['quarterly'] == recession_end].index + 3]['quarterly'].to_string(index=False)

get_recession_end()


# In[120]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    df = read_gdp()
    
    df['quarterly_year'] = df['quarterly_year'].astype(int)
    df['quarterly_qtr'] = df['quarterly_qtr'].str.slice(1,2).astype(int)
    
    recession_start_yr = int(get_recession_start()[0:4])
    recession_start_q = int(get_recession_start()[5:6])
    
    recession_end_yr = int(get_recession_end()[0:4])
    recession_end_q = int(get_recession_end()[5:6])
    
    df = df[(df['quarterly_year'] >= recession_start_yr) & (df['quarterly_qtr'] <= recession_start_q)
             & (df['quarterly_year'] <= recession_end_yr) & (df['quarterly_qtr'] <= recession_end_q)]
    
    df['gdp_change_abs'] = df['gdp_change'].abs()
    bottom = df['gdp_change_abs'].min()
    
    return df[df['gdp_change_abs'].abs() == bottom]['quarterly'].to_string(index=False)

get_recession_bottom()


# In[141]:

def read_zhvi():
    df = pd.read_csv("City_Zhvi_AllHomes.csv", header=0)
    return df

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df['State'] = df['State'].map(states)
    df.set_index(['State', 'RegionName'], inplace=True)
    df = df.loc[:, '2000-01': ]

    new_columns = [str(x)+y for x in range(2000, 2017) for y in ['q1', 'q2', 'q3', 'q4']]
    new_columns = new_columns[:-1] # drop the last quarter of 2016

    x = 0

    for c in new_columns:
        df[c] = df.iloc[:, x:x+3].mean(axis=1)
        x = x+3

    df = df.loc[:, '2000q1':]
    
#     df = df.fillna(0)

    return df

convert_housing_data_to_quarters().iloc[:10,[0,1,-2,-1]]


# In[143]:

def get_quarter_before_recession():
    start = get_recession_start()
    GDP = read_gdp()
    return GDP.loc[GDP[GDP.quarterly == start].index-1]['quarterly'].to_string(index=False)
    
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    housing = convert_housing_data_to_quarters()
    university_towns = get_list_of_university_towns()
    quarter_before_recession = get_quarter_before_recession()  
    recession_bottom = get_recession_bottom()

    # Keep columns corresponding to only two quarters:
    # quarter before recession and recession bottom
    housing = housing[[quarter_before_recession, recession_bottom]]
    housing["price_ratio"] = housing[quarter_before_recession].div(housing[recession_bottom])
#     housing = housing.dropna()

    # Merge the housing dataframa with the one with the university towns taking
    # the intersection of both the dataframes. The new dataframe for housing in
    # university towns has the multi-index of States and Region names.
    university_housing = pd.merge(university_towns, housing, how = "inner", left_on=['State', 'RegionName'], right_index=True)

    # Left over rows from housing gives the dataframe for housing in non-university towns
    university_housing.set_index(['State', 'RegionName'], inplace=True)
    non_university_housing = housing[~housing.index.isin(university_housing.index)]

    # Testing the hypotheses
    t_stat, p_value = ttest_ind(university_housing["price_ratio"], non_university_housing["price_ratio"], nan_policy='omit')

    if p_value < 0.01:
        different = True
    else:
        different = False
    if t_stat < 0:
        better = "university town"
    else:
        better = "non-university town"
#     return housing
    return (different, p_value, better)
#     return 

def test_q6():
    q6 = run_ttest()
    different, p, better = q6

    res = 'Type test: '
    res += ['Failed\n','Passed\n'][type(q6) == tuple]

    res += 'Test "different" type: '
    res += ['Failed\n','Passed\n'][type(different) == bool or type(different) == np.bool_]

    res += 'Test "p" type: '
    res += ['Failed\n','Passed\n'][type(p) == np.float64]

    res +='Test "better" type: '
    res += ['Failed\n','Passed\n'][type(better) == str]
    if type(better) != str:
        res +='"better" should be a string with value "university town" or  "non-university town"'
        return res
    res += 'Test "different" spelling: '
    res += ['Failed\n','Passed\n'][better in ["university town", "non-university town"]]
    return res
print(test_q6())
run_ttest()


# In[ ]:



