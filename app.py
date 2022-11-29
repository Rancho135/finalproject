from flask import Flask, jsonify, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
import logging

# import all required python Lib
import requests
import time
import pymongo
import json
import pandas as pd
from plotly.graph_objs import Scattergeo, Layout
from plotly.graph_objs import Bar, Layout
from plotly import offline
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import kaleido

app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    client = pymongo.MongoClient(
        "mongodb+srv://BDAT:1004@openweatherdata.8d4derw.mongodb.net/?ss1=true&ss1_cert_reqs=CERT_NONE")
    db = client.get_database('openweatherApi')
    records = db.openweather_db

    data = list(records.find({}, {'_id': False}))

    with open("output.json", "w") as outfile:
        json.dump(data, outfile)

    # Reading the data using load
    filename1 = 'output.json'
    with open(filename1) as file_object:
        all_eq_data = json.load(file_object)

    montreal_dic = {}  # creating a dictionary

    montreal_dic = all_eq_data[1]

    windsppeed = []  # creating a list

    windsppeed = montreal_dic["wind"]["speed"]  # extracting wind and speed


    # creating a gauge chart
    data_mont = [go.Indicator(mode="gauge+number",
                              value=windsppeed, domain={'x': [0, 1], 'y': [0, 1]},
                              title={'text': "Montreal Wind Speed in Km/H "})]

    fig = go.Figure({'data': data_mont})
    fig.write_image("static/images/fig1.png")
    # print(all_eq_data[1])



    weather_descs = []  # opening an empty list
    frequencies = {}  # opening an empty dictionary

    for eq_dict in all_eq_data:
        weather_desc = eq_dict['weather'][0]['description']
        weather_descs.append(weather_desc)
    print(weather_descs)
    for item1 in weather_descs:
        # checking the element in dictionary
        if item1 in frequencies:
            # incrementing the count
            frequencies[item1] += 1
        else:
            # initializing the count
            frequencies[item1] = 1

    # Extracting keys and value of weat and ffee
    key = frequencies.keys()
    value = frequencies.values()

    w, f = [], []
    for keys in key:
        w.append(keys)

    for valuess in value:
        f.append(valuess)

    data_1 = [{
        'type': 'bar',
        'x': w,
        'y': f,
    }]

    my_layout_1 = {
        'title': "Unique Weather Descriptions and frequencies",
        'xaxis': {'title': 'Descriptions of Unique Weather'},
        'yaxis': {'title': 'frequencies'},
    }

    fig = go.Figure({'data':data_1, "layout":my_layout_1})
    fig.write_image("static/images/Weather_Descriptions.png")

    # Building a world map
    temperatures, long, lats = [], [], []
    for eq_dict in all_eq_data:
        # Extracting the location using lons and lats
        temp = eq_dict['main']['temp']
        lon = eq_dict['coord']['lon']
        lat = eq_dict['coord']['lat']
        temperatures.append(temp)
        long.append(lon)
        lats.append(lat)

    print(temperatures)

    my_layout = Layout(title='CITIES TEMPERATURES')

    data = [{
        'type': 'scattergeo',
        'lon': long,
        'lat': lats,
        'marker': {'size': [0.05 * temmp for temmp in temperatures],
                   'color': temperatures,
                   'colorscale': 'Plasma',
                   'reversescale': True,
                   'colorbar': {'title': 'Temperature in Kelvin'},
                   }
    }]
    # using

    fig = go.Figure({'data': data, 'layout': my_layout})
    fig.write_image("static/images/Canada.png")

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
