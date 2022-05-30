import pandas as pd
import numpy as np

# iloc = row !!!
# migrants from cols to rows

def extract_participants(path):
    '''
    Extract participants list from dataset.
    ev_all_votes.csv
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


def get_votes_from_country(country, who, the_year):
    '''
    Create a dictionary for {country} with specified type of voting (jury or
    televoters), by years.
    ev_all_votes.csv
    '''
    if who == 'jury' and the_year == '2021':
        return get_votes_from_country_2021(country)

    with open('data/ev_all_votes.csv', 'r', encoding='utf-8') as f:
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


def get_votes_from_country_2021(country):
    '''
    Create a dictionary for {country} with jury votes in 2021 year.
    ev_2021_votes.csv
    '''
    with open('data/ev_2021_votes.csv', 'r', encoding='utf-8') as f:
        data = f.readlines()
    
    data_arr = [line for line in data]
    countries, points = data_arr[0].split(',')[1:], []


    for row in data_arr[1:]:
        if country == row.split(',')[0].lower():
            points = row.split(',')[1:]
            break

    country_points = {}

    index = 0
    for voter, point in zip(countries, points):
        if index == len(countries) - 1:
            point = point[:-1]
            voter = voter[:-1]
        country_points[voter] = point
        index += 1

    country_points = {voter:point for voter, point in country_points.items() if point != '0'}
    return country_points


def main():
    '''
    Main function that calls other data processing functions.
    '''
    participants = extract_participants('data/ev_all_votes.csv')
    # print(participants)

    # votes = get_votes_from_country('ukraine', 'televoters', '2016')
    # print(votes)

    votes = get_votes_from_country('ukraine', 'jury', '2021')
    print(votes)

    # votes2021 = get_votes_from_country_2021()

    # df = pd.read_csv('migrants.csv', dtype=str)
    # df = clean_data(participants, df)
    # # print(df)

    # migrants = get_migrants_from_country(df, 'ukraine', '2014')
    # print(migrants)



if __name__ == "__main__":
    main()


