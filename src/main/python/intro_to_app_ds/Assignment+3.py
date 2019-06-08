
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[2]:

import numpy as np
import pandas as pd


def read_energy_data(file_name):
    energy_excel = pd.ExcelFile(file_name)
    col_names=['na', 'na2','Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy = energy_excel.parse("Energy", skiprows=17, names=col_names, skip_footer=38)
    del energy['na2']
    del energy['na']
    energy = energy.reset_index()
    del energy['index']
    energy = energy.replace('...', np.nan)
    energy['Energy Supply'] = energy['Energy Supply'] * 1000000
    energy['Country'] = energy['Country'].str.replace('Republic of Korea', 'South Korea')
    energy['Country'] = energy['Country'].str.replace('United States of America', 'United States')
    energy['Country'] = energy['Country'].str.replace('United Kingdom of Great Britain and Northern Ireland', 'United Kingdom')
    energy['Country'] = energy['Country'].str.replace('China, Hong Kong Special Administrative Region', 'Hong Kong')
    energy['Country'] = energy['Country'].str.replace('\(.*\)', '')
    energy['Country'] = energy['Country'].str.replace('\d+', '')
    energy['Country'] = energy['Country'].str.lstrip()
    energy['Country'] = energy['Country'].str.rstrip()
    return energy
    

def read_gdp_data(file_name):
    gdp = pd.read_csv(file_name, header=4)
    gdp.rename(columns={'Country Name':'Country'}, inplace=True)
    gdp['Country'] = gdp['Country'].str.replace('Korea, Rep.', 'South Korea')
    gdp['Country'] = gdp['Country'].str.replace('Iran, Islamic Rep.', 'Iran')
    gdp['Country'] = gdp['Country'].str.replace('Hong Kong SAR, China', 'Hong Kong')
    cols = ['Country', 'Country Code', 'Indicator Name', 'Indicator Code', '2006', '2007', '2008', '2009', '2010', '2011',
           '2012', '2013', '2014', '2015']
    return gdp[cols]
    

def read_scim_en_data(file_name):
    scim_in_excel = pd.ExcelFile(file_name)
    scim_en = scim_in_excel.parse(0, header=0)
    return scim_en
    
    
def answer_one():
    # read
    gdp = read_gdp_data("world_bank.csv")
    energy = read_energy_data("Energy Indicators.xls")
    scim_en = read_scim_en_data("scimagojr-3.xlsx")
    
    # merge
    df_merge = pd.merge(gdp, energy, on='Country', how='inner')
    df_final = pd.merge(df_merge, scim_en, on='Country', how='inner')
    
    # set columns and index
    final_cols = ['Country', 'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    df_final = df_final[final_cols]
    df_final = df_final.set_index('Country')
    
    # result for top 15
    return df_final[df_final['Rank'] < 16]


answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[3]:

get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[4]:

def answer_two():
    # read
    energy = read_energy_data("Energy Indicators.xls")
    gdp = read_gdp_data("world_bank.csv")
    scim_en = read_scim_en_data("scimagojr-3.xlsx")
    
    # merge
    df_merge = pd.merge(gdp, energy, on='Country', how='outer')
    df_final = pd.merge(df_merge, scim_en, on='Country', how='outer')
    
    df_merge2 = pd.merge(gdp, energy, on='Country', how='inner')
    df_final2 = pd.merge(df_merge2, scim_en, on='Country', how='inner')
    
    return len(df_final) - len(df_final2)

answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[5]:

def answer_three():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15[['2006', '2007', '2008', '2009', '2010', '2011',
           '2012', '2013', '2014', '2015']].mean(axis=1)
    Top15 = Top15.sort_values(['avgGDP'], ascending=False)
    return Top15['avgGDP']

answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[6]:

def answer_four():
    Top15 = answer_one()
    Top15['avgGDP'] = Top15[['2006', '2007', '2008', '2009', '2010', '2011',
           '2012', '2013', '2014', '2015']].mean(axis=1)
    sixth = Top15.sort_values(['avgGDP'], ascending=False).iloc[[5]]
    result = np.float64(sixth['2015'] - sixth['2006'])
    return result

answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[7]:

def answer_five():
    Top15 = answer_one()
    return Top15['Energy Supply per Capita'].mean()

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[8]:

def answer_six():
    Top15 = answer_one()
    max_renew = Top15['% Renewable'].max()
    row = Top15[Top15['% Renewable'] == max_renew]
    return (row.reset_index()['Country'][0], max_renew)

answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[9]:

def answer_seven():
    Top15 = answer_one()
    Top15['citations_ratio'] = Top15['Self-citations'] / Top15['Citations']
    row = Top15[Top15['citations_ratio'] == Top15['citations_ratio'].max()]
    return (row.reset_index()['Country'][0], row.reset_index()['citations_ratio'][0])

answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[10]:

def answer_eight():
    Top15 = answer_one()
    Top15['population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15.sort_values('population', inplace=True, ascending=False)
    return Top15.iloc[[2]].reset_index()['Country'][0]

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[99]:

def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'].astype('float64') / Top15['Energy Supply per Capita'].astype('float64')
    Top15['Citable docs per Capita'] = Top15['Citable documents'].astype('float64') / Top15['PopEst'].astype('float64')
    return Top15['Citable docs per Capita'].astype('float64').corr(Top15['Energy Supply per Capita'].astype('float64'))

answer_nine()


# In[90]:

def plot9():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'].astype(np.float) / Top15['Energy Supply per Capita'].astype(np.float)
    Top15['Citable docs per Capita'] = Top15['Citable documents'].astype(np.float) / Top15['PopEst'].astype(np.float)
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[91]:

# plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[14]:

def answer_ten():
    Top15 = answer_one()
    Top15['median'] = Top15['% Renewable'].median()
    Top15['HighRenew'] = Top15.apply(lambda x: 1 if x['median'] <= x['% Renewable'] else 0, axis=1)
    Top15.sort_values('Rank', inplace=True)
    return Top15['HighRenew']

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[15]:

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

def answer_eleven():
    Top15 = answer_one()
    Top15['population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    grps = Top15.groupby(by=ContinentDict,axis=0)
    result = grps.sum()
    result['size'] = grps['population'].count()
    result['sum'] = grps['population'].sum()
    result['mean'] = grps['population'].mean()
    result['std'] = grps['population'].std()
    
    cols =  ['size', 'sum', 'mean', 'std']
    return result[cols]

answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[62]:

def answer_twelve():
    Top15 = answer_one()

    out, bins = pd.cut(Top15['% Renewable'].values, bins = 5, retbins = True)
    con = Top15.index.to_series().map(ContinentDict).values

    Top15.reset_index(inplace=True)
    Top15.index = pd.MultiIndex.from_arrays([con, out])
#     Top15.columns = Top15.columns.droplevel(0)
#     Top15.reset_index(inplace=True)
#     Top15 = Top15.set_index(['level_0', 'level_1'])
   
#     df.groupby(level=[0,1]).sum()
    
    return Top15.groupby(level=[0,1])['% Renewable'].count()
    
answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[329]:

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    return Top15['PopEst'].map('{:,}'.format)

answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[ ]:

def plot_optional():
    import matplotlib as plt
    get_ipython().magic('matplotlib inline')
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")


# In[ ]:

#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

