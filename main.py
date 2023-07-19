import pandas as pd
import pyperclip

pd.set_option('display.max_columns', None)

directory = input('Enter the directory of the tsv file: ')

df = pd.read_csv(directory + '.tsv', delimiter='\t', header=None)
df.columns = ['url', 'full domain', 'top domain', 'random number', 'datetime', 'another random number', 'transition', 'page title']
df['datetime'] = pd.to_datetime(df['datetime']).dt.date
df = df.set_index('datetime')
df = df.sort_index()

df_daily = pd.DataFrame()

for date in df.index.unique().to_list():
    this_date = pd.to_datetime(date).date()
    domain = df.loc[this_date, 'top domain']
    all_domain = domain.value_counts()
    all_domain.name = this_date
    df_daily = pd.concat([df_daily, all_domain.to_frame().T])

df_daily = df_daily.fillna(0)

pyperclip.copy(df_daily.to_csv(sep='\t'))

print('tsv dataset copied to the clipboard.')