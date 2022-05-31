
# null hypothesis
# people vote for neighbouring countries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

from process_data import get_votes_from_country
from process_data import get_migrants_from_country
from process_data import clean_data
from process_data import extract_participants

# winners table
winners_data = pd.read_csv('eurovision_winners.csv')
# print(winners_data.head()) 

sample = winners_data.sample()

# YEAR = sample.iat[0,0]
# COUNTRY = sample.iat[0,1]

# print(YEAR)
# print(COUNTRY)

YEAR = '2016'
COUNTRY = 'Ukraine'

for_country_dict = get_votes_from_country(str(COUNTRY.lower()), 'televoters', str(YEAR))
# print(for_country_dict)

participants = extract_participants('ev_all_votes.csv')
df = pd.read_csv('migrants.csv', dtype=str)
df = clean_data(participants, df)


migrants_from = get_migrants_from_country(df, str(COUNTRY.lower()), str(YEAR))


# print(get_migrants_from_country('migrants.csv', str(COUNTRY.lower()), str(YEAR)))


votes = pd.DataFrame(list(for_country_dict.items()), index = [x for x in range(len(for_country_dict.items()))], columns = ['country', 'votes'])
votes['votes'] = votes['votes'].astype(int)
# print(votes)

migrants = pd.DataFrame(list(migrants_from.items()), index = [x for x in range(len(migrants_from.items()))], columns = ['country', 'migrants'])
migrants['migrants'] = migrants['migrants'].apply(lambda x: x.replace(',', '')).astype(int)
# print(migrants)

borders = pd.read_csv('borders.csv')
# print(borders)

counrty_borders = pd.DataFrame()
counrty_borders['country'] = borders['Country']
counrty_borders['borders'] = borders[str(COUNTRY).lower()].astype(int)
# print(counrty_borders)

votes_migrants = pd.merge(votes, migrants, on=['country'])
country_merged = pd.merge(votes_migrants, counrty_borders, on=['country'])
# print(country_merged)


model = smf.ols(formula = 'votes ~ migrants + borders', data=country_merged.dropna())
model = model.fit()
print(model.summary())

# lm = sm.OLS.from_formula('votes ~ migrants + borders', country_merged)
# result = lm.fit()
# print(result.summary())



# YEAR = 1999
# COUNTRY = 

