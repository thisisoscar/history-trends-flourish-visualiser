import pandas as pd
import pyperclip

def extract_ip(string):
    full_ip = is_ip(string, return_ip=True)
    ip = full_ip.split('/')[0]
    return ip

def is_ip(string, return_ip=False):
    try:
        if type(string) != str:
            raise ValueError

        if string.startswith('http://'):
            string = string[7:]

        if '/' in string:
            string = string.split('/')[0]

        numbers = string.split('.')
        
        if ':' in string:
            numbers[-1], port = numbers[-1].split(':')
            if 0 <= int(port) <= 65536:
                pass
            else:
                raise ValueError
        
        if len(numbers) != 4:
            raise ValueError
        
        for i in numbers:
            if 0 <= int(i) <= 255:
                pass
            else:
                raise ValueError
        
        if return_ip:
            ip = '.'.join(numbers)
            if ':' in string:
                ip += ':' + port
            return ip
        else:
            return True
    
    except ValueError:
        if return_ip:
            return None
        else:
            return False


def add_non_website_visits(row):
    if row.isna()[2]: # 2 is top domain
        if row['url'].startswith('chrome-extension'):
            row['top domain'] = 'chrome-extension://' + row['full domain']

        elif is_ip(row['url']):
            row['top domain'] = extract_ip(row['url'])
        
        else:
            row['top domain'] = row['url']

    return row


pd.set_option('display.max_columns', None)

directory = input('Enter the directory of the tsv file: ')

if directory.endswith('.tsv'):
    directory = directory[:-4]

df = pd.read_csv(directory+'.tsv', delimiter='\t', header=None)
df.columns = ['url', 'full domain', 'top domain', 'random number', 'datetime', 'another random number', 'transition', 'page title']
df['datetime'] = pd.to_datetime(df['datetime']).dt.date
df = df.set_index('datetime')
df = df.sort_index()

df = df.apply(add_non_website_visits, axis=1)

daily_visits_counts_df = pd.DataFrame()

for date in df.index.unique().to_list():
    this_date = pd.to_datetime(date).date()
    todays_visits = df.loc[this_date, 'top domain']
    todays_visits_counts = todays_visits.value_counts()
    todays_visits_counts.name = this_date
    daily_visits_counts_df = pd.concat([daily_visits_counts_df, todays_visits_counts.to_frame().T])

daily_visits_counts_df = daily_visits_counts_df.fillna(0)

file_name = directory.split('/')[-1]

directory = input('Enter the directory to save the file in: ')

if directory.endswith('/'):
    directory = directory[:-1]

content = daily_visits_counts_df.to_csv(sep='\t')

pyperclip.copy(content)

with open(f'{directory}/{file_name} flourish formatted.tsv', 'w') as file:
    file.write(content)

print(f'tsv dataset copied to clipboard and saved as {file_name} flourish formatted.tsv')