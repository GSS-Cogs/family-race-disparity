#!/usr/bin/env python
# coding: utf-8

# In[249]:


from gssutils import *
import json

cubes = Cubes("info.json")
info = json.load(open('info.json'))


# In[250]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/uk-population-by-ethnicity/national-and-regional-populations/regional-ethnic-diversity/latest/downloads/population-by-ethnicity-and-region.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[251]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: 'Year/' + str(x['Time']), axis =1)

df = df.drop(['Ethnicity_type', 'Geography', 'Geography', 'Source', 'Value_label1', 'Value_label2'], axis=1)

df = df.rename(columns={'Time' : 'Period', 'Region' : 'Area', 'All usual residents' : 'Total Population', 'Population' : 'Ethnic Population', 'Measure' : 'Measure Type'})

df = df.rename(columns={'Value2' : 'Percentage of ethnic group'})

df = df.replace({'Area' : {'East' : 'E12000006',
                             'East Midlands' : 'E12000004',
                             'London' : 'E12000007',
                             'North East' : 'E12000001',
                             'North West' : 'E12000002',
                             'South East' : 'E12000008',
                             'South West' : 'E12000009',
                             'West Midlands' : 'E12000005',
                             'Yorkshire and The Humber' : 'E12000003',
                             'England and Wales' : 'K04000001',
                             'Total E&W' : 'K04000001',
                             'Wales' : 'W92000004'}})

df['Unit'] = 'Percent'
df['Measure Type'] = 'Percentage of Population'

df = df[['Period', 'Area', 'Total Population', 'Ethnicity', 'Ethnic Population', 'Percentage of ethnic group', 'Value', 'Measure Type', 'Unit']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value', 'Total Population', 'Ethnic Population', 'Percentage of ethnic group']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

csvName = pathify('Population by ethnicity and region')
cubes.add_cube(scraper, df.drop_duplicates(), csvName)

df


# In[252]:


"""
Adding value 2 as attribute to main value rather than initial idea of melting table and having it as a second measure type
Value 1 is % of region
"""


# In[253]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/uk-population-by-ethnicity/national-and-regional-populations/regional-ethnic-diversity/latest/downloads/population-by-ethnicity-region-and-urban-rural-location.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[254]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: 'Year/' + str(x['Time']), axis =1)

df = df.drop(['Source'], axis=1)

df = df.rename(columns={'Time' : 'Period', 'Region' : 'Area', 'Measure' : 'Measure Type'})

df = df.replace({'Area' : {'East' : 'E12000006',
                             'East Midlands' : 'E12000004',
                             'London' : 'E12000007',
                             'North East' : 'E12000001',
                             'North West' : 'E12000002',
                             'South East' : 'E12000008',
                             'South West' : 'E12000009',
                             'West Midlands' : 'E12000005',
                             'Yorkshire and The Humber' : 'E12000003',
                             'England and Wales' : 'K04000001',
                             'Total E&W' : 'K04000001',
                             'Wales' : 'W92000004'}})

df['Unit'] = 'Percent'
df['Measure Type'] = 'Percentage of Ethnic Population'

df = df[['Period', 'Area', 'Urban/Rural', 'Ethnicity', 'Value', 'Measure Type', 'Unit']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

csvName = pathify('Population by ethnicity, region and urban/rural location')
cubes.add_cube(scraper, df.drop_duplicates(), csvName)

df


# In[255]:


"""
Measure is percentage of population in urban/rural broken down by ethnicity Eg 81.5% of all residents live in urban environment, 18.5% live in rural
"""


# In[256]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/uk-population-by-ethnicity/national-and-regional-populations/regional-ethnic-diversity/latest/downloads/ethnic-population-by-local-authority.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[257]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: 'Year/' + str(x['Time']), axis =1)

df = df.drop(['Ethnicity_type', 'Geography_name', 'Geography_type', 'Denominator', 'Numerator'], axis=1)

df = df.rename(columns={'Time' : 'Period', 'Geography_code' : 'Area', 'Measure' : 'Measure Type'})

df['Unit'] = 'Percent'

df = df.replace({'Measure Type' : {'% of local population in this ethnic group' : 'Percentage of Local Population',
                                   '% of national ethnic population in this LA area' : 'Percentage of National Ethnic Population'}})

df = df[['Period', 'Area', 'Ethnicity', 'Value', 'Measure Type', 'Unit']]

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

csvName = pathify('Ethnic population by local authority')
cubes.add_cube(scraper, df.drop_duplicates(), csvName)

df


# In[258]:


"""
Will need investigation to determine if/how to join for multi measure.
decision will have to be made whether its possible to join this to tables based on ethnic population in LA/Region.
Whether its fine to join these with either N/A or All in this field, as its not really feasible to determine per region/LA which are urban/rural
"""

