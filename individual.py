import pandas as pd
import folium
import numpy as np

df = pd.read_csv('data/Cholera.csv')
rmv_front = df['geometry'].map(lambda x : x[20:40])
def remove_tail(x):
    pos = x.find('<')
    return x[:pos]
rmv_tail = rmv_front.map(lambda x : remove_tail(x))
lat = rmv_tail.map(lambda x: x[:x.find(',')])
lon = rmv_tail.map(lambda x: x[x.find(',') + 1:])
df = pd.DataFrame({df.columns[0]:df['count'],'lat':lat,'lon':lon})
df_pumps = df.loc[df['count']==-999]
df = df.loc[df['count']!=-999]

def add_points(map_fol,df,color):
    fil_color = '#000000'
    for lon,lat,count in zip(df['lon'],df['lat'],df['count']):
        if count == -999:
            count = 18
            fil_color = '#ff0000'
        folium.CircleMarker(location = [lon,lat],radius=count,color=color,fill_color=fil_color).add_to(map_fol)

def find_closest(df_pumps,lon,lat,count):
    vals = []
    for x in range(df_pumps.shape[0]):
        vals.append(((float(df_pumps.iloc[x,1])-float(lat))**2+(float(df_pumps.iloc[x,2])-float(lon))**2)**.5)
    idx = np.argmin(vals)
    df_pumps.iloc[idx,3] += count
    return df_pumps.iloc[idx,4]

def closest_by_size_and_color(map_fol,df_pumps):
    for lon,lat,count in zip(df['lon'],df['lat'],df['count']):
        color = find_closest(df_pumps,lon,lat,count)
        fil_color = '#000000'
        folium.CircleMarker(location = [lon,lat],radius=count,color=color,fill_color=fil_color).add_to(map_fol)
    #print("\n\n\n{}\n\n\n").format(df_pumps['total_count'])
    sum_total = np.sum(df_pumps['total_count'])
    for x in range(df_pumps.shape[0]):
        df_pumps.iloc[x,3] = (df_pumps.iloc[x,3]/ sum_total)*60
    for lon,lat,count,color in zip(df_pumps['lon'],df_pumps['lat'],df_pumps['total_count'],df_pumps['colors']):
        fil_color = color
        folium.CircleMarker(location = [lon,lat],radius=count,color=color,fill_color=fil_color).add_to(map_fol)

def set_colors(df):
    col_list = ['#ff0040','#bf00ff','#0000ff','#00ffff','#00ff40','#ffbf00','#ff0000','#ff0066']
    cols = df_pumps.shape[1]
    df_pumps['colors'] = np.zeros(df_pumps['lon'].shape[0]).reshape(df_pumps['lon'].shape[ 0],1)
    for x in range(df_pumps.shape[0]):
        df_pumps.iloc[x,cols] = col_list[x]

if __name__ == '__main__':
    first_map = folium.Map(location = [51.513, -0.137], tiles="Stamen Terrain",zoom_start=16)
    #add_points(first_map,df,'#0000ff')
    #add_points(first_map,df_pumps,'#ff0000')
    df_pumps['total_count'] = np.zeros(df_pumps['lon'].shape[0]).reshape(df_pumps['lon'].shape[ 0],1)
    set_colors(df_pumps)
    closest_by_size_and_color(first_map,df_pumps)
    first_map.save("Cholera.html")
