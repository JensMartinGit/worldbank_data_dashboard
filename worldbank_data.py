import requests
from collections import defaultdict
import plotly.graph_objs as go
import plotly.offline as py


def get_data_from_api():
    # Map series to get from worldbank API with respective indicator codes
    series_dict = {'co2_total' : 'EN.ATM.CO2E.KT', 
                   'co2_per_capita' : 'EN.ATM.CO2E.PC'}


    # Define countries and payload for all requests
    payload = {'format': 'json', 'per_page': '500', 'date':'1990:2016'}
    countries = 'cn;us;in;ru;de;id;br;gb;au;pk;no;nz'


    # Define order of countries in graphs
    country_list = ['China', 'United States', 'India', 'Russian Federation', 'Germany', 'Brazil', 
                    'United Kingdom', 'Australia', 'Pakistan', 'Norway', 'New Zealand']


    # Get data from worldbank API and store all series in one dictionary 'my_data'
    my_data = {}
    for series in series_dict:
        # Get series from worldbank API
        indicators = series_dict[series]
        url = f'http://api.worldbank.org/v2/countries/{countries}/indicators/{indicators}'
        r = requests.get(url,params=payload)
        
        # Put json data for series into dictionary and add it to my_data
        my_data[series] = defaultdict(list)
        for entry in r.json()[1]:
            if not entry['country']['value'] in my_data[series]:
                my_data[series][entry['country']['value']] = [[],[]]
            my_data[series][entry['country']['value']][0].append(entry['date'])
            my_data[series][entry['country']['value']][1].append(entry['value'])


    return my_data, country_list

def create_figures():
    
    my_data, country_list = get_data_from_api()
    figures = []

    # Create line graph for 'Developement of Total CO2 Emissions from 1990 to 2016'
    graph_1 = []
    for country in country_list:
        graph_1.append(
            go.Scatter(
            x = my_data['co2_total'][country][0][::-1],
            y = my_data['co2_total'][country][1][::-1],
            mode = 'lines',
            name = country
            )
        )
        
    layout_1 = {'title' : 'Developement of CO2 Emissions per Capita from 1990 to 2016',
                  'xaxis' : {'title' : 'Year'},
                  'yaxis' : {'title' : 'CO2 emissions (kt)'}
                 }

    figures.append({'data' : graph_1, 'layout' : layout_1})


    # Create line graph for 'Developement of Total CO2 Emissions from 1990 to 2016'
    graph_2 = []
    for country in country_list:
        graph_2.append(
            go.Scatter(
            x = my_data['co2_per_capita'][country][0][::-1],
            y = my_data['co2_per_capita'][country][1][::-1],
            mode = 'lines',
            name = country
            )
        )
        
    layout_2 = {'title' : 'Developement of CO2 Emissions per Capita from 1990 to 2016', 
                'xaxis' : {'title' : 'Year'}, 
                'yaxis' : {'title' : 'CO2 emissions (kt)'}
               }

    figures.append({'data' : graph_2, 'layout' : layout_2})


    # Create bar chart for 'Total CO2 Emissions in 2016'
    graph_3 = []
    x_values, y_values = [], []
    for country in country_list:
        x_values.append(country)
        y_values.append(my_data['co2_total'][country][1][0])
    graph_3.append(
        go.Bar(
        x = x_values,
        y = y_values,
        )
    )

    layout_3 = {'title' : 'Total CO2 Emissions in 2016',
               'xaxis' : {'title' : 'Country'},
               'yaxis' : {'title' : 'CO2 emissions (kt)'}
               }

    figures.append({'data' : graph_3, 'layout' : layout_3})


    # Create bar chart for 'CO2 Emissions per Capita in 2016'
    graph_4 = []
    x_values, y_values = [], []
    for country in country_list:
        x_values.append(country)
        y_values.append(my_data['co2_per_capita'][country][1][0])
    graph_4.append(
        go.Bar(
        x = x_values,
        y = y_values,
        )
    )

    layout_4 = {'title' : 'CO2 Emissions per Capita in 2016',
               'xaxis' : {'title' : 'Country'},
               'yaxis' : {'title' : 'CO2 emissions (kt)'}
               }

    figures.append({'data' : graph_4, 'layout' : layout_4})

    return figures