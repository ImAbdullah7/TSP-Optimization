from numpy import double
import pandas as pd
from convert_numbers import arabic_to_english

# data_xls = pd.read_excel('a.xlsx', 'Sheet1', index_col=None)
# data_xls.to_csv('a.csv', encoding='utf-8-sig')

map = {}
d = {}

def read(path: str):
    df = pd.read_excel(path)
    rows_count = df.shape[0]
   
    for i in range(rows_count):
        row = list(df.loc[i])
        name = row[0].strip()
        
        connected_places_list = row[1].split('،')
        path_cost_list = str(row[2]).split('.')
        path_cost_list = [arabic_to_english(item) for item in path_cost_list]

        lat = double(row[4])
        lon = double(row[3])
        d[name] = (lat, lon)

        if len(connected_places_list) != len(path_cost_list):
            print(name)
            print('ERROR: connected places and path costs lists\'s length does not match')
            continue
        
        place_and_cost_list = []
        for i in range(len(connected_places_list)):
            place_and_cost_list.append((connected_places_list[i].strip(), int(path_cost_list[i])))


        # print(place_and_cost_list)
        map[name] = place_and_cost_list
    
def get_options():
    return [name for name in map.keys()]

def initial_state_exist(initial):
    return initial in map

def successors_of(name: str): 
    v = map.get(name)
    return v if v else []

def get_coordinate_of(name):
    return d.get(name)