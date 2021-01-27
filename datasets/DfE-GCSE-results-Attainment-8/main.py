#!/usr/bin/env python
# coding: utf-8

# In[112]:


from gssutils import *
import json

cubes = Cubes("info.json")
info = json.load(open('info.json'))

tidied_sheets = []


# In[113]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/education-skills-and-training/11-to-16-years-old/gcse-results-attainment-8-for-children-aged-14-to-16-key-stage-4/latest/downloads/attainment-8-scores-local-authority-2018-19.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[114]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: x['Time_type'] + '/' + x['Time'], axis =1)

df = df.drop(['Ethnicity_type', 'Time_type', 'Geography', 'Geography_type', 'Denominator', 'Numerator'], axis=1)

df = df.rename(columns={'Measure' : 'Measure Type', 'Time' : 'Period', 'Geography_code' : 'Area', 'Gender' : 'Sex'})

df['FSM'] = 'All'

df['SEN Type'] = 'All'

df['SEN Grouping'] = 'All'

df['Admission Type'] = 'All'

df['School Characteristic'] = 'All'

df['Religious Denomination'] = 'All'

df = df[['Period', 'Area', 'Ethnicity', 'Sex', 'Age', 'FSM', 'SEN Type', 'SEN Grouping', 'Admission Type', 'School Characteristic', 'Religious Denomination', 'Value']]

tidied_sheets.append(df)

df


# In[115]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/education-skills-and-training/11-to-16-years-old/gcse-results-attainment-8-for-children-aged-14-to-16-key-stage-4/latest/downloads/attainment-8-scores-national-2018-19.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[116]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: x['Time_type'] + '/' + x['Time'], axis =1)

df = df.drop(['Ethnicity_type', 'Time_type', 'Geography', 'Geography_type', 'Denominator', 'Numerator'], axis=1)

df = df.rename(columns={'Measure' : 'Measure Type', 'Time' : 'Period', 'Geography_code' : 'Area', 'Gender' : 'Sex', 'SEN_type' : 'SEN Type', 'SEN_grouping' : 'SEN Grouping', 'Admission_type' : 'Admission Type', 'school_characteristic' : 'School Characteristic', 'Religious_denomination' : 'Religious Denomination'})

df = df[['Period', 'Area', 'Ethnicity', 'Sex', 'Age', 'FSM', 'SEN Type', 'SEN Grouping', 'Admission Type', 'School Characteristic', 'Religious Denomination', 'Value']]

tidied_sheets.append(df)

df


# In[117]:


df = pd.concat(tidied_sheets)

df['Age'] = df.apply(lambda x: x['Age'].strip(), axis = 1)

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value']

for col in df.columns.values.tolist():
	if col in COLUMNS_TO_NOT_PATHIFY:
		continue
	try:
		df[col] = df[col].apply(pathify)
	except Exception as err:
		raise Exception('Failed to pathify column "{}".'.format(col)) from err

csvName = 'observations'
cubes.add_cube(scraper, df.drop_duplicates(), csvName)

df


# In[118]:


cubes.output_all()


# In[119]:


notes = """
Value is Average Attainment 8 score out of 90
"""

