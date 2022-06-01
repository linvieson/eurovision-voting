

import pandas as pd


def get_winning_metrics(file_name):

    winning_df = pd.read_csv(file_name)
    winning_df['Counter'] = [1 for i in range(len(winning_df.index))]

    metrics_language = winning_df.groupby(['SongLanguage']).Counter.sum().reset_index()
    
    metrics_country = winning_df.groupby(['Winner']).Counter.sum().reset_index()

    return [metrics_language.sort_values(by=['Counter'], ascending=False), metrics_country.sort_values(by=['Counter'], ascending=False)]





if __name__ == '__main__':
    path = 'eurovision_winners.csv'
    
    print(get_winning_metrics(path)[0])
    print(get_winning_metrics(path)[1])
