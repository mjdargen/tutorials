from imdb import IMDb
import plotly.express as px
import pandas as pd
import os
import datetime
import string

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


# makes required directories for project
def make_dirs():
    if not os.path.exists(f'{DIR_PATH}/input'):
        os.makedirs(f'{DIR_PATH}/input')

    if not os.path.exists(f'{DIR_PATH}/output'):
        os.makedirs(f'{DIR_PATH}/output')


# retrieves ratings for every episode from imdb, returns correct title
def get_ratings(show):

    ia = IMDb()  # create instance of imdb class

    # search for show to get id
    results = ia.search_movie(show)
    # search results not the best, filter and check with user
    results = [res for res in results if res['kind'] == 'tv series']
    i = 0
    r = input(
        f"Top result is {results[i]['title']} ({results[i]['year']}). Is that correct (y/n)? ")
    while 'y' not in r.lower():
        i += 1
        try:
            r = input(
                f"Next result is {results[i]['title']} ({results[i]['year']}). Is that correct (y/n)? ")
        except IndexError:
            print('No more results. Exiting program...')
            quit()
    id = results[i].getID()
    show = results[i]['title']

    # use id to retrieve episode data
    series = ia.get_movie(id)
    ia.update(series, 'episodes')

    # open csv file to save episode title and rating
    filename = show
    for punc in string.punctuation:
        filename = filename.replace(punc, '')
    filename = filename.replace(' ', '_').lower()
    f = open(f'{DIR_PATH}/input/{filename}.csv', 'w')
    f.write('Episode,Rating\n')
    # for each season
    for i in range(1, series['number of seasons']+1):
        # for each episode in season
        for j in range(1, len(series['episodes'][i].keys())+1):
            try:
                # check air dates for show still presently airing
                air = series['episodes'][i][j]['original air date']
                air = air.replace('.', '')
                try:
                    air = datetime.datetime.strptime(air, '%d %b %Y')
                except ValueError:
                    air = datetime.datetime.strptime(air, '%Y')
                if air > datetime.datetime.now():
                    f.close()
                    return show, filename
                # write data to file
                f.write(f"\"S{i}E{j} {series['episodes'][i][j]['title']}\","
                        + f"{series['episodes'][i][j]['rating']}\n")
            except KeyError:
                pass  # typically issue with episode 0 or double ep
    f.close()
    return show, filename


# returns a list containing the titles of the 5 highest rated episodes
def get_best(filename):
    df = pd.read_csv(f'{DIR_PATH}/input/{filename}.csv', encoding='latin')
    return list(df.nlargest(5, 'Rating')['Episode'])


# returns a list containing the titles of the 5 lowest rated episodes
def get_worst(filename):
    df = pd.read_csv(f'{DIR_PATH}/input/{filename}.csv', encoding='latin')
    return list(df.nsmallest(5, 'Rating')['Episode'])


# plot the ratings on an interactive graph using plotly
def plot_ratings(show, filename, best, worst):
    df = pd.read_csv(f'{DIR_PATH}/input/{filename}.csv', encoding='latin')
    df['Episode'] = df['Episode'].str.slice(0, 40)
    fig = px.bar(df, title=f'{show} IMDb Ratings', x='Episode', y='Rating',
                 color='Rating', color_continuous_scale='bluyl')
    fig.add_annotation(
        text='<b>Highest Rated Episodes:</b><br>' + '<br>'.join(best),
        xref="paper", yref="paper", x=0.1, y=0.02,
        align='left', bgcolor="#f1f1f1", showarrow=False
        )
    fig.add_annotation(
        text='<b>Lowest Rated Episodes:</b><br>' + '<br>'.join(worst),
        xref="paper", yref="paper", x=0.9, y=0.02,
        align='left', bgcolor="#f1f1f1", showarrow=False
        )
    fig.show()
    fig.write_html(f'{DIR_PATH}/output/{filename}.html')


# main processing
def main():
    make_dirs()
    show = input("Which TV show's ratings would you like to see? ")
    show, filename = get_ratings(show)
    best = get_best(filename)
    worst = get_worst(filename)
    plot_ratings(show, filename, best, worst)


if __name__ == '__main__':
    main()
