import pandas as pd
import matplotlib.pyplot as plt

def get_winning_metrics(file_name):
    '''
    Get two dataframes: winners by language, and winners by country.
    '''

    winning_df = pd.read_csv(file_name)
    winning_df['Counter'] = [1 for i in range(len(winning_df.index))]

    metrics_language = winning_df.groupby(['SongLanguage']).Counter.sum().reset_index()
    
    metrics_country = winning_df.groupby(['Winner']).Counter.sum().reset_index()

    return [metrics_language.sort_values(by=['Counter'], ascending=False), metrics_country.sort_values(by=['Counter'], ascending=False)]


def plot_results(language_winners, winners):
    '''
    Plot the results of the language analysis.
    '''
    colors = ['#a8acc4', '#65ecfb', '#e190f7', '#335d6a', '#5496a8', '#d3d3a1', '#4c2c54', '#0c5484']

    x = language_winners['Counter']
    labels = language_winners['SongLanguage']
    x_new, labels_new = [], []

    for elem, label in zip(x, labels):
        if label != 'None':
            x_new.append(elem)
            labels_new.append(label)

    plt.title('Song languages by number of wins')
    plt.pie(x_new, labels=labels_new, colors=colors)
    plt.show()

    winners = winners.dropna()
    winners.plot(kind='bar',x='Winner', y='Counter', color='#a8acc4')
    plt.show()


if __name__ == '__main__':
    path = 'data/eurovision_winners.csv'
    language_winners, winners = get_winning_metrics(path)

    plot_results(language_winners, winners)
    