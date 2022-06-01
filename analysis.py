# import libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

# import functions from data processing modules
from process_data import get_votes_from_country
from process_data import get_migrants_from_country
from process_data import clean_data
from process_data import extract_participants

# winners table
winners_data = pd.read_csv('data/eurovision_winners.csv')

# random sampling of the year the winner of this year (some country)
# sample = winners_data.sample()
# YEAR = sample.iat[0,0]
# COUNTRY = sample.iat[0,1]

# example
YEAR = '2015'
COUNTRY = 'Sweden'
LANGUAGE = 'english'

# get votes for COUNTRY in the chosen YEAR
this_year = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(YEAR))

votes_this = pd.DataFrame(list(this_year.items()), \
                    index = [x for x in range(len(this_year.items()))], \
                    columns = ['country', 'votes_this'])
votes_this['votes_this'] = votes_this['votes_this'].astype(int)

# get votes for COUNTRY in the previous year (YEAR - 1)
previous = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(int(YEAR) - 1))

votes_previous = pd.DataFrame(list(previous.items()), \
                    index = [x for x in range(len(previous.items()))], \
                    columns = ['country', 'votes_previous'])
votes_previous['votes_previous'] = votes_previous['votes_previous'].astype(int)

# join series into one dataframe with votes
votes = pd.concat([votes_this, votes_previous])
votes = votes.groupby(['country']).sum().reset_index()

# get migrants from this COUNTRY in chosen YEAR 
participants = extract_participants('data/ev_all_votes.csv')
df = pd.read_csv('data/migrants.csv', dtype=str)
df = clean_data(participants, df)

# migrants in YEAR
migrants_from = get_migrants_from_country(df, str(COUNTRY.lower()), str(YEAR))

migrants = pd.DataFrame(list(migrants_from.items()), \
                        index = [x for x in range(len(migrants_from.items()))], \
                        columns = ['country', 'migrants'])
migrants[f'migrants{YEAR}'] = migrants['migrants'].apply(lambda x: x.replace(',', '')).astype(int)

# migrants in previous years
migrants_list = []
for year_number in range(1990, int(YEAR) + 1):
    migrants_dict = get_migrants_from_country(df, str(COUNTRY.lower()), str(year_number))
    if len(migrants_dict) != 0:
        migrants_year = pd.DataFrame(list(migrants_dict.items()), \
                        index = [x for x in range(len(migrants_dict.items()))], \
                        columns = ['country', f'migrants{year_number}'])
        migrants_year[f'migrants{year_number}'] = migrants_year[f'migrants{year_number}'].apply(lambda x: x.replace(',', '')).astype(int)
        migrants_list.append(migrants_year)

migrants_df = migrants_list[0].merge(migrants_list[1], on=['country'])
for year_num in range(2, int(YEAR) - 1990):
    migrants_df = migrants_df.merge(migrants_list[year_num], on=['country'])

# create dataframe with this COUNTRYs borders
borders = pd.read_csv('data/borders.csv')
country_borders = pd.DataFrame()
country_borders['country'] = borders['Country']
country_borders['borders'] = borders[str(COUNTRY).lower()].astype(int)

# dataframe for languages match
language = pd.DataFrame()
language['country'] = pd.read_csv('data/borders.csv')['Country']
language['lang'] = np.where(pd.read_csv('data/borders.csv')['official_language'] == LANGUAGE, 1, 0)


# Regression by migrants  

# merge votes, migrants and borders into one dataframe
votes_migrants = pd.merge(votes, migrants_df, on=['country'])
country_merged = votes_migrants.merge(country_borders, on=['country'])
merged_df = country_merged.merge(language, on=['country'])
print(merged_df)

str_formula = f'votes_previous ~ borders + lang +'
for year in range(1990, int(YEAR) - 1):
    str_formula = str_formula + f'migrants{year} + '
str_formula = str_formula[:-2]

# model the Ordinary Least Squares regression
model = smf.ols(formula = str_formula, data=merged_df.dropna())
model = model.fit()
print(model.summary())


# Regression by votes
votes_list = []
for year_number in range(1990, int(YEAR)):
    country_dict = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(year_number))
    if len(country_dict) != 0:
        votes_year = pd.DataFrame(list(country_dict.items()), \
                        index = [x for x in range(len(country_dict.items()))], \
                        columns = ['country', f'votes{year_number}'])
        votes_year[f'votes{year_number}'] = votes_year[f'votes{year_number}'].astype(int)
        votes_list.append(votes_year)

# dataframe with votes from 1990 to the YEAR
votes_df = pd.concat([votes_list[0], votes_list[1]])
for year_num in range(2, int(YEAR) - 1990 - 1):
    votes_df = pd.concat([votes_df, votes_list[year_num]])
    votes_df = votes_df.groupby(['country']).sum().reset_index()

votes_df = votes_df.merge(votes, on=['country'])

# merge needed dataframes
country_merged = votes_df.merge(country_borders, on=['country'])
merged_df = country_merged.merge(language, on=['country'])
print(merged_df)

str_formula = f'votes_previous ~ borders + lang +'
for year in range(1990, int(YEAR) - 1):
    str_formula = str_formula + f'votes{year} + '
str_formula = str_formula[:-2]
str_formula = str_formula.replace('votes2010 +', '')

# model the Ordinary Least Squares regression
model_2 = smf.ols(formula = str_formula, data=merged_df.dropna())
model_2 = model_2.fit()
print(model_2.summary())
