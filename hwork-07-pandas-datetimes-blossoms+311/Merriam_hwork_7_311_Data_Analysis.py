#!/usr/bin/env python
# coding: utf-8

# ### Do your imports!

# In[105]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')


# # 311 data analysis
# 
# ## Read in `subset.csv` and review the first few rows
# 
# Even though it's a giant file – gigs and gigs! – it's a subset of the [entire dataset](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9). It covers plenty of years, but not all of the columns.
# 
# If your computer is struggling (which it will!) or you are impatient, feel free to use `nrows=` when reading it in to speed up the process by only reading in a subset of columns. Pull in at least a few million, or a couple years back.

# In[106]:


df = pd.read_csv("/Users/susanmerriam/Documents/DATABASES/data-hwork/github_folders/hwork-docs/07-homework/311/subset.csv", nrows = 1000000, encoding="utf-8")


# In[107]:


df.columns = df.columns.str.lower().str.replace(" ", "_")
df.head(3)


# In[108]:


df.agency_name = df.agency_name.str.lower().replace(" ", "_", regex=False)
df.complaint_type = df.complaint_type.str.lower().replace(" ", "_", regex=False)
df.complaint_type = df.complaint_type.str.lower().replace("-", "_", regex=False)
df.descriptor = df.descriptor.str.lower().replace(" ", "_", regex=False)
df.descriptor = df.descriptor.str.lower().replace("/", "_", regex=False)
df.location_type = df.location_type.str.lower().replace(" ", "_", regex=False)
df.address_type = df.address_type.str.lower().replace(" ", "_", regex=False)
df.city = df.city.str.lower().replace(" ", "_", regex=False)
df.status = df.status.str.lower().replace(" ", "_", regex=False)
df.open_data_channel_type = df.open_data_channel_type.str.lower().replace(" ", "_", regex=False)
df.borough = df.borough.str.lower().replace(" ", "_", regex=False)


# In[109]:


df = df.rename(columns={'open_data_channel_type': 'channel'})
df = df.rename(columns={'incident_zip': 'zip'})


# In[110]:


df.head(3)


# In[111]:


df.shape


# In[112]:


df.dtypes


# In[113]:


# df = df.dropna(subset=['Beer'])
# df = df.dropna(subset=['full_flowering_date'])


# In[114]:


# parse dates=date)colns 


# ### Where the subset came from
# 
# If you're curious, I took the [original data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9/data) and clipped out a subset by using the command-line tool [csvkit](https://csvkit.readthedocs.io/en/latest/).
# 
# First I inspected the column headers:
# 
# ```bash
# $ csvcut -n 311_Service_Requests_from_2010_to_Present.csv 
# ```
# 
# Then I selected the columns I was interested in and saved it to a file.
# 
# ```bash
# $ csvcut -c 1,2,3,4,5,6,7,8,9,10,16,17,20,26,29 311_Service_Requests_from_2010_to_Present.csv > subset.csv
# ```
# 
# This was much much much much faster than doing it in Python.

# ## We want more columns!
# 
# **Right now we don't see all of the columns.** For example, mine has `...` between the **Incident Address** column and the **City** column. Go up to the top where you imported pandas, and add a `pd.set_option` line that will allow you to view all of the columns of the dataset.

# In[115]:


pd.set_option("display.max_colwidth", None)
df.head(3)


# ## We hate those column names!
# 
# Change the column names to be tab- and period-friendly, like `df.created_date` instead of `df['Created Date']`

# # Dates and times
# 
# ## Are the datetimes actually datetimes?
# 
# We're going to be doing some datetime-y things, so let's see if the columns that look like dates are actually dates.

# In[116]:


df.dtypes


# ## In they aren't datetimes, convert them
# 
# The ones we're interested in are as follows:
# 
# * Created Date
# * Closed Date
# 
# You have two options to convert them:
# 
# 1. Do it like we did in class, but **overwrite the existing string columns with the new datetime versions**
# 2. Find an option with `read_csv` to automatically read certain columns as dates! Use the shift+tab trick to read the `read_csv` docs to uncover it. Once you find it, you'll set it to be the **list of date-y columns**.
# 
# They're both going to take forever if you do them wrong, but can be faster with a few tricks. For example, using `pd.to_datetime` can be sped up significantly be specifying the format of the datestring.
# 
# For example, if your datetime was formatted as `YYYY-MM-DD HH:MM:SS AM`, you could use the following:
# 
# ```
# df.my_datetime = pd.to_datetime(df.my_datetime, format="%Y-%m-%d %I:%M:%S %p")
# ```
# 
# It's unfortunately much much much faster than the `read_csv` technique. And yes, [that's `%I` and not `%H`](https://strftime.org/).
# 
# > *Tip: What should happen if it encounters an error or missing data?*

# In[117]:


df.created_date = pd.to_datetime(df.created_date, format="%m/%d/%Y %I:%M:%S %p")
# .dt.strftime("%m%d")
# df.head(3)


# In[118]:


df.closed_date = pd.to_datetime(df.closed_date, format="%m/%d/%Y %I:%M:%S %p")
# .dt.strftime("%m%d")
df.dtypes


# In[119]:


df.head(50)


# In[120]:


df = df.dropna(subset=['created_date'])
df = df.dropna(subset=['closed_date'])
# df = df.dropna(subset=['full_flowering_date'])
df.shape


# ## According to the dataset, which month of the year has the most 311 calls?
# 
# The kind of answer we're looking for is "January," not "January 2021"

# In[121]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[122]:


# using dt aggregates the data by month of the year as opposed to the specific month of a specific year


# In[123]:


df.created_date.dt.month.value_counts().sort_index(ascending = True)


# In[124]:


df.created_date.dt.month.value_counts().sort_index().plot(kind = 'bar')


# In[125]:


# WRONG!! df.created_date.resample('M', on='created_date').size()
# every time you do resample, do the entire dataframe


# In[127]:


# REF homicides_df = df[df.created_date == 'HOMICIDE'].copy()


# ## According to the dataset, which month has had the most 311 calls?
# 
# The kind of answer we're looking for is "January 2021," not "January" (although _techniucally_ it will say `2021-01-31`, not `January 2021`)

# In[128]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[129]:


# using resample not only considers the month of the year but also the year itself in which it measures which month in a particular year had the most calls


# In[130]:


df.resample('M', on='created_date').size().sort_values(ascending= False)


# In[131]:


df.resample('M', on='created_date').size().plot()


# ## Plot the 311 call frequency over our dataset on a _weekly_ basis
# 
# To make your y axis start at zero, use `ylim=(0,100000)` when doing `.plot`. But replace the `1000` with a large enough value to actually see your data nicely!

# In[132]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[133]:


df.created_date.dt.week.value_counts().sort_index().plot(kind = 'bar', ylim=(0,100000), xlabel='week', ylabel='# of calls')


# ## What time of day (by hour) is the least common for 311 complains? The most common?
# 

# In[134]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[135]:


df.created_date.dt.hour.value_counts()
# .sort_index(ascending = True)


# ### Make a graph of the results
# 
# * Make sure the hours are in the correct order
# * Be sure to set the y-axis to start at 0
# * Give your plot a descriptive title

# In[161]:


df.created_date.dt.hour.value_counts().sort_index().plot(kind = 'bar', ylim=(0,100000), xlabel='hour in the day (24-hr clock)', ylabel='# of calls')


# In[137]:


# df.resample('H', on='created_date').size().plot()


# # Agencies
# 
# ## What agencies field the most complaints in the dataset? Get the top 5.
# 
# Use the `agency` column for this one.

# In[138]:


df.agency.value_counts().head(5)


# ## What are each of those agencies?
# 
# Define the following five acronyms:
# 
# * NYPD
# * HPD
# * DOT
# * DSNY
# * DEP

# In[139]:


# NYPD = new york city police department
# HPD = department of housing preservation and development
# DOT = department of transportation 
# DSNY = department of sanitation
# DEP = department of environmental protection


# In[140]:


df.agency_name.value_counts().head(10)


# ## What is the most common complaint to HPD?

# In[141]:


HPD_df = df[df.agency == 'HPD'].copy()


# In[142]:


HPD_df.complaint_type.value_counts().head(1)


# In[143]:


# HPD_df.descriptor.value_counts().head(10)


# In[144]:


# Why did you pick these columns to calculate the answer?


# In[145]:


# I chose complaint type as opposed to descriptor for the
# Department of Housing Preservation and Development because
# it's a larger category that could be applied to multiple locations. 
# If I had used descriptor, the same type of complaint could be 
# refering to different locations and would be more difficult 
# to see what the complaints are for. For example, entire building 
# could refer to any type of complaint.


# In[146]:


# REF CODE df[df.manner_of_death == 'HOMICIDE'].copy()


# In[147]:


# complaint_type


# ## What are the top 3 complaints to each agency?
# 
# You'll want to use the weird confusing `.groupby(level=...` thing we learned when reviewing the homework.

# In[148]:


# look at dogs hwork, top 5 dogs name ber borough
# group by level = 0 just something to cut and paste
# top n something per group, it's always level = 0, n (or head)
# just the way it is

# This is just one of those things you cut-and-paste or memorize
# REF CODE merged.groupby('neighborhood')['Primary Breed'].value_counts().groupby(level=0).nlargest(1)


# In[149]:


df.groupby('agency')['complaint_type'].value_counts().groupby(level=0).nlargest(3)


# ## What is the most common kind of residential noise complaint?
# 
# The NYPD seems to deal with a lot of noise complaints at homes. What is the most common subtype?

# In[152]:


noise_residential_df = df[df.complaint_type == 'noise - residential'].copy()
# noise_residential_df.head(5)


# In[153]:


noise_residential_df.descriptor.value_counts().head(1)


# In[167]:


# noise_df = df[df.complaint_type == 'noise'].copy()
# noise_df.head(5)


# In[ ]:


# Why did you pick these columns to calculate the answer?


# In[151]:


# NYPD    NYPD    noise - residential           75828
# DEP     DEP     noise                         31234


# In[168]:


# I chose the complaint-type of "noise-residential" because it specified 
# the location as opposed to purely noise, which when in a quick look
# at the data sorted by noise tended to be complaints focused on 
# construction such as jack hammering which was unclear whether the 
# complaints were residential related


# In[154]:


# residential_df = df[df.location_type == 'residential building'].copy()
# residential_df.head(3)


# In[155]:


# residential_df.complaint_type.value_counts()


# In[156]:


# residential_df[residential_df.complaint_type.str.contains("noise")] 


# ## What time of day do "Loud Music/Party" complaints come in? Make it a chart!

# In[157]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[158]:


loud_music_party_df = df[df.descriptor == 'loud music/party'].copy()
# loud_music_party_df.head(3)


# In[177]:


loud_music_party_df.created_date.dt.hour.value_counts()


# In[159]:


loud_music_party_df.created_date.dt.hour.value_counts().sort_index().plot(kind = 'bar', ylim=(0,20000), xlabel='hour in the day (24-hr clock)', ylabel='# of complaints')


# ## When do people party hard?
# 
# Make a monthly chart of Loud Music/Party complaints since the beginning of the dataset. Make it count them on a biweekly basis (every two weeks).

# In[160]:


# there are two big techniques for date stuff: .dt or .resample
# if you use one of those, explain why you picked that one and not the other


# In[34]:


# make bi-weekly chart


# In[ ]:


# biweekly / 2 weekly
# homicides_df.resample('2W', on='incident_datetime').size().plot()


# In[193]:


loud_music_party_df.resample('2W', on='created_date').size().sort_values(ascending=False).head(5)


# In[187]:


loud_music_party_df.resample('2W', on='created_date').size().plot()


# ## People and their bees
# 
# Sometimes people complain about bees! Why they'd do that, I have no idea. It's somewhere in "complaint_type" – can you find all of the bee-related complaints?

# In[194]:


df[df.complaint_type.str.contains("bee")]


# ### What month do most of the complaints happen in? I'd like to see a graph.

# In[203]:


bees_df = df[df.complaint_type.str.contains("bee")]
bees.shape


# In[204]:


bees_df.created_date.dt.month.value_counts().sort_index().plot(kind = 'bar', xlabel='month', ylabel='# of complaints')


# In[206]:


# bees_df.resample('W', on='created_date').size().plot()


# ### Are the people getting in trouble usually beekeepers or not beekeepers?

# In[213]:


bees_df.descriptor.value_counts()


# # Math with datetimes
# 
# ## How long does it normally take to resolve a 311 complaint?
# 
# Even if we didn't cover this in class, I have faith that you can guess how to calculate it.

# In[227]:


# df.shape


# In[221]:


df = df.dropna(subset=['closed_date'])
df = df.dropna(subset=['created_date'])


# In[232]:


# df.created_date.shape


# In[231]:


# df.head(10)
# (df.closed_date - df.created_date).value_counts()


# In[ ]:


# (df.closed_date - df.created_date).value_counts()


# In[230]:


(df.closed_date - df.created_date).median()


# In[229]:


(df.closed_date - df.created_date).describe()


# Save it as a new column called `time_to_fix`

# In[234]:


df['time_to_fix'] = df.closed_date - df.created_date
# df.time_to_fix.head(3)


# ## Which agency has the best time-to-fix time?

# In[245]:


df.groupby('agency')['time_to_fix'].median().groupby(level=0).nlargest(1).sort_values(ascending = True)


# ## Maybe we need some more information...
# 
# I might want to know how big our sample size is for each of those, maybe the high performers only have one or two instances of having requests filed!
# 
# ### First, try using `.describe()` on the time to fix column after your `groupby`.

# In[249]:


df.groupby('agency')['time_to_fix'].describe().head(3)


# ### Now, an alternative
# 
# Seems a little busy, yeah? **You can also do smaller, custom aggregations.**
# 
# Try something like this:
# 
# ```python
# # Multiple aggregations of one column
# df.groupby('agency').time_to_fix.agg(['median', 'size'])
# 
# # You can also do something like this to reach multiple columns
# df.groupby('agency').agg({
#     'time_to_fix': ['median', 'size']
# })
# ```

# In[250]:


df.groupby('agency').time_to_fix.agg(['median', 'size'])


# In[251]:


df.groupby('agency').agg({
    'time_to_fix': ['median', 'size']
})


# ## Seems weird that NYPD time-to-close is so fast. Can we break that down by complaint type?
# 
# Remember the order: 
# 
# 1. Filter
# 2. Group
# 3. Grab a column
# 4. Do something with it
# 5. Sort

# In[264]:


# df[df.month == 'May'].groupby('products').sales.sum().sort_values()
# df.groupby('agency').time_to_fix.agg(['median', 'size'])

# .groupby('products').sales.sum().sort_values()
# df.groupby('agency').time_to_fix.agg(['median', 'size'])

df[df.agency == 'NYPD'].groupby('complaint_type').time_to_fix.agg(['median', 'size']).sort_values('median', ascending = True)


# ## Back to median fix time for all agencies: do these values change based on the borough?
# 
# First, use `groupby` to get the median time to fix per agency in each borough. You can use something like `pd.set_option("display.max_rows", 200)` if you can't see all of the results by default!

# In[321]:


pd.set_option("display.max_rows", 200)


# In[324]:


# df.groupby('agency').time_to_fix.agg(['median', 'size']).sort_values(by = 'borough', ascending = False)


# In[296]:


# df.groupby('agency')['borough'].time_to_fix.agg(['median', 'size']).sort_values()


# In[299]:


# df.groupby('agency').borough.time_to_fix.agg(['median', 'size'])
# df.groupby('agency').time_to_fix.agg(['median', 'size'])
# df.groupby('agency')['time_to_fix'].describe().head(3)


# In[268]:


# df.agency.groupby('borough').time_to_fix.agg(['median', 'size']).sort_values('median', ascending = True)


# In[320]:


# borough_df = df.borough


# ### Or, use another technique!

# We talked about pivot table for a hot second in class, but it's (potentially) a good fit for this situation:
# 
# ```python
# df.pivot_table(
#     columns='what will show up as your columns',
#     index='what will show up as your rows',
#     values='the column that will show up in each cell',
#     aggfunc='the calculation(s) you want dont'
# )
# ```

# In[275]:


df.pivot_table(
    columns='borough',
    index='agency',
    values='time_to_fix',
#     aggfunc='median'
)


# ### Use the pivot table result to find the worst-performing agency in the Bronx, then compare with Staten Island
# 
# Since it's a dataframe, you can use the power of `.sort_values` (twice!). Do any of the agencies have a large difference between the two?

# In[317]:


df.pivot_table(
    columns='borough',
    index='agency',
    values='time_to_fix',
#     aggfunc='median'
).sort_values(by = 'bronx', ascending = False).head(1)


# ## What were the top ten 311 types of complaints on Thanksgiving 2020? Are they different than the day before Thanksgiving?
# 
# **Finding exact dates is awful, honestly.** While you can do something like this to ask for rows after a specific date:
# 
# ```python
# df[df.date_column >= '2020-01-01']
# ```
# 
# You, for some reason, can't ask for an **exact match** unless you're really looking for exactly at midnight. For example, this won't give you what you want:
# 
# ```python
# df[df.date_column == '2020-01-01']
# ```
# 
# Instead, the thing you need to do is this:
# 
# ```python
# df[(df.date_column >= '2020-01-01') & (df.date_column < '2020-01-02']
# ```
# 
# Everything that starts at midnight on the 1st but *is still less than midnight on the 2nd**.

# In[330]:


# df[(df.date_column >= '2020-01-01') & (df.date_column < '2020-01-02']

# df[(df.created_date >= '2020-11-26') & (df.created_date < '2020-11-27')]
# .groupby('complaint_type').value_counts()

# df.created_date.plot(y = 'created_date')


# In[318]:


# df.pivot_table(
#     columns='complaint_type',
#     index='agency',
#     values='time_to_fix',
# #     aggfunc='median'
# ).sort_values(by = 'bronx', ascending = False).head(1)


# In[310]:


df.head(2)


# ## What is the most common 311 complaint types on Christmas day?
# 
# And I mean *all Christmas days*, not just in certain years)
# 
# * Tip: `dt.` and `&` are going to be your friend here
# * Tip: If you want to get fancy you can look up `strftime`
# * Tip: One of those is much much faster than the other

# In[ ]:





# In[ ]:





# # Stories
# 
# Let's approach this from the idea of **having stories and wanting to investigate them.** Fun facts:
# 
# * Not all of these are reasonably answered with what our data is
# * We only have certain skills about how to analyzing the data
# * There are about six hundred approaches for each question
# 
# But: **for most of these prompts there are at least a few ways you can get something interesting out of the dataset.**

# ## Fireworks and BLM
# 
# You're writing a story about the anecdotal idea that the summer of the BLM protests there were an incredible number of fireworks being set off. Does the data support this?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[ ]:


# summer 2020 


# In[ ]:





# In[ ]:





# ## Sanitation and work slowdowns
# 
# The Dept of Sanitation recently had a work slowdown to protest the vaccine mandate. You'd like to write about past work slowdowns that have caused garbage to pile up in the street, streets to not be swept, etc, and compare them to the current slowdown. You've also heard rumors that it was worse in Staten Island and a few Brooklyn neighborhoods - Marine Park and Canarsie - than everywhere else.
# 
# Use the data to find timeframes worth researching, and note how this slowdown might compare. Also, is there anything behind the geographic issue?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[ ]:





# In[ ]:





# In[ ]:





# ## Gentrification and whining to the government
# 
# It's said that when a neighborhood gentrifies, the people who move in are quick to report things to authorities that would previously have been ignored or dealt with on a personal basis. Use the data to investigate the concept (two techniques for finding gentrifying area are using census data and using Google).
# 
# What assumptions is your analysis making? What could make your analysis fall apart? Be sure to cite your sources. 

# In[ ]:





# In[ ]:





# In[ ]:





# ## 311 quirks
# 
# Our editor tried to submit a 311 request using the app the other day, but it didn't go through. As we all know, news is what happens to your editor! Has the 311 mobile app ever actually stopped working?
# 
# If that's a dead end, maybe you can talk about the differences between the different submission avenues: could a mobile outage disproportionately impact a certain kind of complaint or agency? How about if the phone lines stopped working?
# 
# What assumptions is your analysis making? What could make your analysis fall apart?

# In[ ]:





# In[ ]:





# In[ ]:





# ## NYCHA and public funds
# 
# NYC's public housing infrastructure is failing, and one reason is lack of federal funds. While the recent spending bills passed through Congress might be able to help, the feeling is that things have really fallen apart in the past however-many years – as time goes on it gets more and more difficult for the agency in control of things to address issues in a timely manner.
# 
# If you were tasked with finding information to help a reporter writing on this topic, you will **not** reasonably be able to find much in the dataset to support or refute this. Why not? 
# 
# If you wanted to squeeze something out of this dataset anyway, what could an option be? (You might need to bring in another dataset.)

# In[ ]:





# In[ ]:





# In[ ]:




