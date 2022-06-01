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
winners_data = pd.read_csv('eurovision_winners.csv')
# print(winners_data.head()) 

# random sampling of the year the winner of this year (some country)
sample = winners_data.sample()

# YEAR = sample.iat[0,0]
# COUNTRY = sample.iat[0,1]

# example
YEAR = '2015'
COUNTRY = 'Sweden'

# get votes for COUNTRY
for_country_dict = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(YEAR))

votes = pd.DataFrame(list(for_country_dict.items()), \
                    index = [x for x in range(len(for_country_dict.items()))], \
                    columns = ['country', 'votes'])
votes['votes'] = votes['votes'].astype(int)
# print(votes)

votes_list = []
for year_number in range(int(YEAR) - 5, int(YEAR)):
    country_dict = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(year_number))
    # print(country_dict)
    if len(country_dict) != 0:
        votes_year = pd.DataFrame(list(country_dict.items()), \
                        index = [x for x in range(len(country_dict.items()))], \
                        columns = ['country', f'votes{year_number}'])
        # print(votes_year)
        votes_year[f'votes{year_number}'] = votes_year[f'votes{year_number}'].astype(int)
        votes = pd.concat([votes, votes_year])
        # votes = votes.groupby(['country']).sum()
        # votes = pd.merge(votes, votes_year, on=['country'])
        # votes_list.append(votes_year)

# votes_df = votes_list[0].merge(votes_list[1], on=['country']).merge(votes_list[2], on=['country']).merge(votes_list[3], on=['country'])
# votes.df = votes.merge(votes_df, on=['country'])

votes_df = votes.fillna(0)

# get migrants from this COUNTRY in chosen YEAR 
participants = extract_participants('ev_all_votes.csv')
df = pd.read_csv('migrants.csv', dtype=str)
df = clean_data(participants, df)

# migrants in YEAR
migrants_from = get_migrants_from_country(df, str(COUNTRY.lower()), str(int(YEAR) - 1))

migrants = pd.DataFrame(list(migrants_from.items()), \
                        index = [x for x in range(len(migrants_from.items()))], \
                        columns = ['country', 'migrants'])
migrants[f'migrants{int(YEAR) - 1}'] = migrants['migrants'].apply(lambda x: x.replace(',', '')).astype(int)

# migrants in 4 previous years
# migrants_list = []
# for year_number in range(int(YEAR) - 4, int(YEAR)):
#     migrants_dict = get_migrants_from_country(df, str(COUNTRY.lower()), str(year_number))
#     # print(country_dict)
#     if len(migrants_dict) != 0:
#         migrants_year = pd.DataFrame(list(migrants_dict.items()), \
#                         index = [x for x in range(len(migrants_dict.items()))], \
#                         columns = ['country', f'migrants{year_number}'])
#         # print(votes_year)
#         migrants_year[f'migrants{year_number}'] = migrants_year[f'migrants{year_number}'].apply(lambda x: x.replace(',', '')).astype(int)
#         # votes = pd.concat([votes, votes_year])
#         # votes = votes.groupby(['country']).sum()
#         # votes = pd.merge(votes, votes_year, on=['country'])
#         migrants_list.append(migrants_year)

# migrants_df = migrants_list[0].merge(migrants_list[1], on=['country']).merge(migrants_list[2], on=['country']).merge(migrants_list[3], on=['country'])
# print(migrants_df)


# create dataframe with this COUNTRYs borders
borders = pd.read_csv('borders.csv')

country_borders = pd.DataFrame()
country_borders['country'] = borders['Country']
country_borders['borders'] = borders[str(COUNTRY).lower()].astype(int)

# merge votes, migrants and borders into one dataframe
# votes_merged = pd.merge(votes, votes_df, on=['country'])
votes_migrants = pd.merge(votes_df, migrants, on=['country'])
country_merged = votes_migrants.merge(country_borders, on=['country'])
print(country_merged)

# model the Ordinary Least Squares regression
model = smf.ols(formula = f'votes{int(YEAR) - 1} ~ votes{int(YEAR) - 2} + votes{int(YEAR) - 3} + votes{int(YEAR) - 4} \
                            + migrants{int(YEAR) - 1} + borders', data=country_merged.dropna())
model = model.fit()
print(model.summary())



# {int(YEAR) - 1} + migrants{int(YEAR) - 2} + migrants{int(YEAR) - 3} + migrants{int(YEAR) - 4}
