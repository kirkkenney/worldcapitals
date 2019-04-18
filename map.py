import folium
import pandas
import numpy as np

data = pandas.read_excel('capital-cities.xls')

lat = list(data['Latitude'])
lon = list(data['Longitude'])
cap = list(data['Capital City'])
country = list(data['Country or area'])
pop = list(data['Population'])
pop = list(np.around(np.array(pop), 2)) # round floats to 2 decimal places
cap_type = list(data['Capital Type'])


html = """<b>Country:</b> %s<br><b>Capital:</b> %s<br>
<b>Population:</b> %s million<br>
<b>Capital Type:</b> %s"""
# HTML for capital popup info boxes


legend_html = '''<div style="position:fixed; bottom: 50px; left: 50px; width: 400px;
height: 200px; border: solid black 2px; z-index: 999; font-size: 15px;
background-color:rgba(215,215,215, 0.6); padding:5px 15px; color:black;">
<h4 style='text-align:center;'>The World's Capitals</h4> <br>
<span style='color:black; font-weight:bold'>Black:</span> Population less than 1 million<br>
<span style='color:orange; font-weight:bold'>Orange:</span> Population between 1 and 5 million<br>
<span style='color:red; font-weight:bold'>Red:</span> Population between 5 and 10 million<br>
<span style='color:green; font-weight:bold'>Green:</span> Population greater than 10 million<br>
<br><span style="color:black;">Source: <a href="https://esa.un.org/unpd/wup/cd-rom/...XLS_CD.../WUP2014-F13-Capital_Cities.xls"
target="_blank">United Nations</a></span>
 </div>
'''
# HTML and styling for legend box


def marker_color(pop):
    if pop < 1:
        return 'black'
    elif 1 <= pop < 5:
        return 'orange'
    elif 5 <= pop < 10:
        return 'red'
    elif 10 < pop:
        return 'green'
    else:
        return 'rgba(255,255,255,0)'
# generate marker colours based on population data


def marker_rad(pop):
    if pop < 1:
        return 2
    elif 1 <= pop:
        return pop*1
    #elif 1 <= pop < 5:
        #return 4
    #elif 5 <= pop < 10:
        #return 5
    #elif 10 < pop:
        #return 6
    else:
        return 0
# generate size of markers based on population data

map = folium.Map(location=[0, 0], zoom_start=2)
# generate map with world in view

fg_markers = folium.FeatureGroup(name='Capitals')
# generate details as a grouping

for lt, ln, cap, coun, pop, cap_type in zip(lat, lon, cap, country, pop, cap_type):
    # iterate through variables to populate popup boxes (zip keyword required for multiple)
    iframe = folium.IFrame(html=html % (coun, cap, pop, cap_type), width=250, height=100)
    # generate popup iframe, assign html var, populate with data
    fg_markers.add_child(folium.CircleMarker(location=[lt, ln],
    # define marker type, assign latitude/longitude for each iteration of data
    popup=folium.Popup(iframe), fill=True, color=marker_color(pop), fill_color=marker_color(pop),
    # assign iframe to popup, refer to functions to dynamically alter colour/size of markers
    fill_opacity=0.6, radius=marker_rad(pop)))


map.add_child(fg_markers)
# add fg_markers grouping to the map
map.get_root().html.add_child(folium.Element(legend_html))
# add legend_html to the map

map.save('index.html')
# save script in an HTML file for browser display
