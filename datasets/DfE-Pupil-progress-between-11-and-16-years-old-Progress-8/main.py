#!/usr/bin/env python
# coding: utf-8

# In[197]:


from gssutils import *
import json

cubes = Cubes("info.json")
info = json.load(open('info.json'))

tidied_sheets = []


# In[198]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/education-skills-and-training/11-to-16-years-old/pupil-progress-progress-8-between-ages-11-and-16-key-stage-2-to-key-stage-4/latest/downloads/progress-8-2017-to-2018-local-authority.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[199]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: x['Time_type'] + '/' + x['Academic_Year'].replace('/','-'), axis =1)

df = df.drop(['Academic_Year', 'Ethnicity_Type', 'Time_type', 'Geography', 'Geography_type', 'Denominator'], axis=1)

df = df.rename(columns={'Measure' : 'Measure Type', 'Time' : 'Period', 'ONS_Geography_code' : 'Area', 'Gender' : 'Sex'})

df['Religious Character'] = 'All'
df['Type of School'] = 'All'
df['SEN'] = 'All'
df['Admission Basis'] = 'All'

df = df.replace({'FSM' : {'All Pupils' : 'All'},
                 'Sex' : {'All Pupils' : 'All',},
                 'Ethnicity' : {'All Pupils' : 'All'}})

df = df[['Period', 'Area', 'Ethnicity', 'Sex', 'FSM', 'SEN', 'Admission Basis', 'Type of School', 'Religious Character', 'Value', 'Lower confidence interval', 'Upper confidence interval']]

tidied_sheets.append(df)

df


# In[200]:


with open('info.json') as f:
  info_file_data = json.load(f)
info_file_data["dataURL"] = "https://www.ethnicity-facts-figures.service.gov.uk/education-skills-and-training/11-to-16-years-old/pupil-progress-progress-8-between-ages-11-and-16-key-stage-2-to-key-stage-4/latest/downloads/progress-8-2017-to-2018-england.csv"
with open('info.json', 'w') as f:
    json.dump(info_file_data, f, indent=2)

scraper = Scraper(seed="info.json")
scraper


# In[201]:


df = scraper.distributions[0].as_pandas()

df['Time'] = df.apply(lambda x: x['Time_type'] + '/' + x['Academic_Year'].replace('/','-'), axis =1)

df = df.drop(['Academic_Year', 'Time_type', 'Geography', 'Geography_type', 'Denominator', 'Ethnicity_type', 'Measure', 'Unnamed: 19','Unnamed: 20','Unnamed: 21','Unnamed: 22'], axis=1)

df = df.rename(columns={'Time' : 'Period', 'ONS geography code' : 'Area', 'Gender' : 'Sex', 'Admission_Basis' : 'Admission Basis', 'Type_of_school' : 'Type of School', 'Religious_character' : 'Religious Character'})

df = df.replace({'FSM' : {'All Pupils' : 'All'},
                 'Sex' : {'All Pupils' : 'All'},
                 'SEN' : {'All Pupils' : 'All'},
                 'Admission Basis' : {'All Pupils' : 'All'},
                 'Religious Character' : {'All Pupils' : 'All'},
                 'Ethnicity' : {'All pupils' : 'All'}})

df = df[['Period', 'Area', 'Ethnicity', 'Sex', 'FSM', 'SEN', 'Admission Basis', 'Type of School', 'Religious Character', 'Value', 'Lower confidence interval', 'Upper confidence interval']]

tidied_sheets.append(df)

df


# In[202]:


df = pd.concat(tidied_sheets)

df = df.replace({'Sex' : {'Boys' : 'M',
                          'Girls' : 'F',
                          'All' : 'T'}})

COLUMNS_TO_NOT_PATHIFY = ['Area', 'Value', 'Lower confidence interval', 'Upper confidence interval']

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


# In[203]:


cubes.output_all()

