import pandas as pd

state_abbr= {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

abbr_state = dict(map(reversed, state_abbr.items()))

def county_pop_data():
    df = pd.read_csv('county_pop.csv')

    df['Geographic Region'] = df['Geographic Region'].str.replace('.','', n=1)

    new = df['Geographic Region'].str.split(',', n=1, expand=True)

    df['County'] = new[0]
    df['State'] = new[1]
    df.drop(columns=['Geographic Region'], inplace=True)

    county = df.pop('County')
    state = df.pop('State')
    df.insert(0, 'County', county)
    df.insert(1, 'State', state)

    df['State'] = df["State"].str.replace(' ', '', n=1)

    return df

def count_code_data():
    df = pd.read_csv('county_codes.txt', sep='|')
    df = df.drop(['COUNTYNS', 'CLASSFP', 'FUNCSTAT'], axis=1)
    df = df.rename(columns={'STATE':'State', 'STATEFP':'State Code', 'COUNTYFP':'County Code', 'COUNTYNAME': 'County'})
    df['State'] = df['State'].map(abbr_state)

    df['County Code'] = df["County Code"].astype(str)
    df['State Code'] = df["State Code"].astype(str)

    return df

def merge():
    df = pd.merge(county_pop_data(), count_code_data(), how='outer', )
    return df

merge().to_csv('county_population.csv')