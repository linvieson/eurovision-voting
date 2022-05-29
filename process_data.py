import pandas as pd
import numpy as np

# iloc = row !!!
# migrants from cols to rows

def extract_participants(path):
    '''
    Extract participants list from dataset.
    all_eu_votes.csv
    '''
    df = pd.read_csv(path)
    countries = pd.unique(df['From'])

    for ind, country in enumerate(countries):
        if '-' in country:
            countries[ind] = country[country.index('-')+1:]

    countries.sort()
    return countries


def clean_data(participants, df):
    '''
    Drop rows and columns with non-participant countries.
    migrants.csv
    '''
    # drop rows
    for i in range(len(df)):
        elem = df.iloc[i]['Country of destination']

        if isinstance(elem, str) and (elem.lower() not in participants):
            df.iloc[i]['Country of destination'] = None

    df = df[df['Country of destination'].notna()]

    # drop columns
    for col in df.columns:
        if col == 'Year' or col == 'Country of destination':
            continue
        elif col.lower() not in participants:
            df = df.drop(columns=[col])

    df = df.set_index(df['Country of destination'])
    return df


def get_migrants_from_country(df, country, year):
    '''
    Create a dictionary for migrants from {country} to other countries, by years.
    migrants.csv
    '''
    possible_years = pd.unique(df['Year'])

    while year not in possible_years:
        year = str(int(year)-1)

    df = df[df['Year'] == year]
    col = df[country.capitalize()]
    col = col.dropna()

    destinations, migrants = df.index, np.array(col)
    migrants_data = {}

    for dest, migr in zip(destinations, migrants):
        migrants_data[dest.lower()] = migr

    return migrants_data


def get_votes_from_country(path, country, who, the_year):
    '''
    Create a dictionary for {country} with specified type of voting (jury or
    televoters), by years.
    all_eu_votes.csv
    '''
    with open(path, 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    data_arr = [line for line in data]
    data_arr = data_arr[1:]
    country_points = {}

    for row in data_arr:
        number, edition, year, vote_type, from_country, to_country, points = row.split(',')
        points = points[:-1]

        if (country in to_country and who in vote_type and the_year == year):
            country_points[from_country] = points

    return country_points


def main():
    participants = extract_participants('ev_all_votes.csv')
    # print(participants)

    votes = get_votes_from_country('ev_all_votes.csv', 'ukraine', 'televoters', '2016')
    print(votes)

    df = pd.read_csv('migrants.csv', dtype=str)
    df = clean_data(participants, df)
    # print(df)

    migrants = get_migrants_from_country(df, 'ukraine', '2014')
    print(migrants)




if __name__ == "__main__":
    main()


