
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

data_path = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'

st.markdown(
'''# COVID-19 Dashboard
This is an app displaying United States COVID-19 data.
Data provided by [The New York Times](https://github.com/nytimes/covid-19-data/blob/master/us-states.csv).
''')

st.sidebar.header('User Input Features')
st.sidebar.markdown(
'''Update the input to view changes on the dashboard.
''')

months = {
    'January': [21,31],
    'February': [1,28],
    'March': [1,31],
    'April': [1,30],
    'May': [1,31],
    'June': [1,30],
    'July': [1,31],
    'August': [1,31]
}

def user_input_features():
    month = st.sidebar.selectbox('Month',('January','February','March', 'April', 'May', 'June', 'July', 'August'))
    searchType = st.sidebar.selectbox('Choose Data to Display', ('cases', 'deaths'))
    days = months[month]
    day = st.sidebar.slider('Day to look at',days[0],days[1],21)

    st.subheader('Total US COVID-19 %s as of %s %i, 2020' % (searchType, month, day))
    
    data = {'Month': month,
            'Day': day, 
            'Display': searchType}
    features = pd.DataFrame(data, index=[0])
    return features

month_conv = {
    'January': '01',
    'February': '02',
    'March': '03',
    'April': '04',
    'May': '05',
    'June': '06',
    'July': '07',
    'August': '08'
}

date_string = ''
type_string = ''
save_month = ''
save_day = ''
input_df = user_input_features()
for index, row in input_df.iterrows():
    save_month = row[0]
    day = row[1]
    save_day = day
    type_string = row[2]
    if day < 10:
        day = '0' + str(day)
        date_string = '2020-' + month_conv[row[0]] + '-' + day
    else:
        date_string = '2020-' + month_conv[row[0]] + '-' + str(day)
    
data = pd.read_csv(data_path)

states_loc = {
    'Wisconsin': [44.500000, -89.500000],
    'West Virginia': [39.000000, -80.500000],
    'Vermont': [44.000000, -72.699997],
    'Texas': [31.000000, -100.000000],
    'South Dakota': [44.500000, -100.000000],
    'Rhode Island':	[41.700001, -71.500000],
    'Oregon': [44.000000, -120.500000],
    'New York':	[43.000000, -75.000000],
    'New Hampshire': [44.000000, -71.500000],
    'Nebraska': [41.500000,	-100.000000],
    'Kansas': [38.500000, -98.000000],
    'Mississippi': [33.000000, -90.000000],
    'Illinois': [40.000000,	-89.000000],
    'Delaware': [39.000000,	-75.500000],
    'Connecticut': [41.599998, -72.699997],
    'Arkansas': [34.799999,	-92.199997],
    'Indiana': [40.273502, -86.126976],
    'Missouri':	[38.573936,	-92.603760],
    'Florida': [27.994402, -81.760254],
    'Nevada': [39.876019, -117.224121],
    'Maine': [45.367584, -68.972168],
    'Michigan': [44.182205,	-84.506836],
    'Georgia': [33.247875, -83.441162],
    'Hawaii': [19.741755, -155.844437],
    'Alaska': [66.160507, -153.369141],
    'Tennessee': [35.860119, -86.660156],
    'Virginia': [37.926868,	-78.024902],
    'New Jersey': [39.833851, -74.871826],
    'Kentucky': [37.839333,	-84.270020],
    'North Dakota': [47.650589,	-100.437012],
    'Minnesota': [46.392410, -94.636230],
    'Oklahoma': [36.084621,	-96.921387],
    'Montana': [46.965260, -109.533691],
    'Washington': [47.751076, -120.740135],
    'Utah': [39.419220,	-111.950684],
    'Colorado': [39.113014,	-105.358887],
    'Ohio': [40.367474,	-82.996216],
    'Alabama': [32.318230, -86.902298],
    'Iowa':	[42.032974,	-93.581543],
    'New Mexico': [34.307144, -106.018066],
    'South Carolina': [33.836082, -81.163727],
    'Pennsylvania': [41.203323,	-77.194527],
    'Arizona': [34.048927, -111.093735],
    'Maryland': [39.045753,	-76.641273],
    'Massachusetts': [42.407211, -71.382439],
    'California': [36.778259, -119.417931],
    'Idaho': [44.068203, -114.742043],
    'Wyoming': [43.075970, -107.290283],
    'North Carolina': [35.782169, -80.793457],
    'Louisiana': [30.391830, -92.329102],
    'District of Columbia': [38.907200, -77.036900],
    'Puerto Rico': [18.220800, -66.590100],
    'Virgin Islands': [18.335800, -64.896300],
    'Guam': [13.444300, 144.793700],
    'Northern Mariana Islands': [15.007900, 145.673900]
}

database = []

for index, row in data.iterrows():
    cur_data = [item for item in row]
    
    cur_state = row.state
    
    coords = states_loc[cur_state]

    lat = coords[0]
    lon = coords[1]
    cur_data.append(lat)
    cur_data.append(lon)

    database.append(cur_data)

df = pd.DataFrame(database, columns=['date', 'state', 'fips', 'cases', 'deaths', 'lat', 'lon']) 
df['date'] = pd.to_datetime(df['date'])
df_map = df.copy()

df_map = df_map[df_map.date == date_string]

midpoint = (np.average(df['lat']), np.average(df['lon']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 2.6,
        "pitch": 55,
    },
    layers=[
        pdk.Layer(
            "ColumnLayer",
            data=df_map,
            get_position=["lon", "lat"],
            get_elevation=type_string,
            radius=50000,
            color='red',
            elevation_scale=2.5,
            pickable=True,
            extruded=True,
        ),
    ],
))

states = []
cases = []
deaths = []
date = ''

for index, row in df_map.iterrows():
    date = row[0]
    states.append(row[1])
    cases.append(row[3])
    deaths.append(row[4])

latest = df.tail(n=55)
total_cases = latest.cases.sum()
total_deaths = latest.deaths.sum()

if type_string == 'cases':
    p = figure(x_range=states, plot_width=700, plot_height=500, title='Breakdown of Total US COVID-19 Cases by State. Displaying total as of {} {}, 2020'.format(save_month, save_day), toolbar_location=None, tools='')
    p.vbar(x=states, top=cases, width=0.9)
    p.xaxis.major_label_orientation = 'vertical'
    st.write(p)

    st.markdown('\t***Total US COVID-19 cases since January 21st, 2020: %i***' % (total_cases))

else:
    p = figure(x_range=states, plot_width=700, plot_height=500, title='Breakdown of Total US COVID-19 Deaths by State. Displaying total as of {} {}, 2020'.format(save_month, save_day), toolbar_location=None, tools='')
    p.vbar(x=states, top=deaths, width=0.9)
    p.xaxis.major_label_orientation = 'vertical'
    st.write(p)

    st.markdown('\t***Total US COVID-19 deaths since January 21st, 2020: %i***' % (total_deaths))
