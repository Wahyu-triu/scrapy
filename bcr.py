# source reference: "https://towardsdatascience.com/creating-bar-chart-race-animation-with-python-cdb01144074e"
#import library
import pandas as pd
import bar_chart_race as bcr
import matplotlib
matplotlib.use('Agg')

def to_normal(number):
    result = []
    for num in number:
        if num == 'N.A.':
            num = 0
            result.append(num)
        else:
            num = num.replace("''", "")
            num = num.replace(",", '')
            num = int(num)
            result.append(num)
    return result

# import data
df = pd.read_csv('/mnt/d/scrapy/worldpopulation/population_new.csv')

# split the data into urban population and population
urban_pop = df[['country_name', 'year', 'urban pop']]
population = df[['country_name', 'year', 'population']]

#normalize number and datatypes
population['population'] = to_normal(population['population'])
urban_pop['urban pop'] = to_normal(urban_pop['urban pop'])

# transform the data
population_df = population.pivot_table(values='population',
                                      index='year',
                                      columns = 'country_name')
urban_df = urban_pop.pivot_table(values='urban pop',
                               index='year',
                               columns='country_name')

# remove NaN values
# population_df
population_df.fillna(0, inplace=True)
population_df.sort_values(list(population_df.columns), inplace=True)
population_df = population_df.sort_index()
# urban_df
urban_df.fillna(0, inplace=True)
urban_df.sort_values(list(urban_df.columns), inplace=True)
urban_df = urban_df.sort_index()

# aggregate the data
population_df.iloc[:, 0:-1] = population_df.iloc[:, 0:-1].cumsum()
urban_df.iloc[:, 0:-1] = urban_df.iloc[:, 0:-1].cumsum()

# top population
top_pop = set()
for index, row in population_df.iterrows():
    top_pop |= set(row[row > 0].sort_values(ascending=False).head(15).index)
df_top_pop = population_df[top_pop]

# top urban population
top_urban = set()
for index, row in urban_df.iterrows():
    top_urban |= set(row[row > 0].sort_values(ascending=False).head(15).index)
df_top_urban = urban_df[top_urban]

# barchart race top population
bcr.bar_chart_race(df=df_top_pop,
                  n_bars=15,
                  sort='desc',
                  title='Country with the Highest Population Since 1955',
                  filename = 'top_population.mp4',
                  figsize=(12,8),
                  period_length=350,
                  cmap ='dark12',
                  dpi = 300)

# barchart race top population
bcr.bar_chart_race(df=df_top_urban,
                  n_bars=15,
                  sort='desc',
                  title='Country with the Highest Urban Population Since 1955',
                  filename = 'top_urban_population.mp4',
                  figsize=(12,8),
                  period_length=350,
                  cmap ='dark12',
                  dpi = 300)