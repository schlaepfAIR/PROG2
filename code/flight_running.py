# import required libraries
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime
import plotly.express as px
from plotly.offline import plot
import pandas as pd  # pandas for dataframe manipulation
import random  # to create funny colors for the statistics
import os.path  # to check file exists
from os import path

app = Flask(__name__)

# create a dictionary to map colors to airline for stats


def name_to_colorairline(airline, r_min=125, r_max=255, g_min=125, g_max=255, b_min=125, b_max=255):
    mapping_colorsairline = dict()

    for name in airline.unique():
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = 'rgb({}, {}, {})'.format(red, green, blue)

        mapping_colorsairline[name] = rgb_string

    return mapping_colorsairline

# create a dictionary to map colors to departure for stats


def name_to_color(departure, r_min=0, r_max=124, g_min=0, g_max=124, b_min=0, b_max=124):
    mapping_colors = dict()

    for name in departure.unique():
        red = random.randint(r_min, r_max)
        green = random.randint(g_min, g_max)
        blue = random.randint(b_min, b_max)
        rgb_string = 'rgb({}, {}, {})'.format(red, green, blue)

        mapping_colors[name] = rgb_string

    return mapping_colors

# home page with the overview of flights, sort by flightDate


@app.route('/')
def overview():  # to read and sort the csv file using the pandas library
    if path.exists('newFlights.csv'):  # check if the file exists
        df = pd.read_csv('newFlights.csv', header=0)
        df = df.sort_values(by=['flightDate'])
    else:  # if the file does not exist, create a new one
        df = pd.DataFrame(columns=['created', 'airline', 'flightNumber', 'flightDate',
                                   'departure', 'arrival', 'aircraft', 'staffPrice',
                                   'googlePrice', 'diffPrice',
                                   ])
        df.to_csv(r'newFlights.csv', header=True, index=False)

    # to read and sort the csv file using the pandas library
    df = pd.read_csv('newFlights.csv', header=0)
    df = df.sort_values(by=['flightDate'])
    myData = df.values
    return render_template('table.html', myData=myData)


# add a new flight using get and post methods

@app.route("/add", methods=["get", "post"])
def addFlight():
    filename = 'newFlights.csv'  # define the filename

    if request.method.lower() == "get":
        return render_template('addflight.html')
    if request.method.lower() == "post":
        airline = request.form['airline']
        flight_number = request.form['flight_number']
        flight_date = request.form['flight_date']
        departure = request.form['departure']
        arrival = request.form['arrival']
        aircraft = request.form['aircraft']
        staff_price = request.form['staff_price']
        google_price = request.form['google_price']
        staff_price = float(staff_price)  # convert the string to float
        google_price = float(google_price)  # convert the string to float
        diff_price = google_price - staff_price

        now = datetime.now()  # get the current date and time for timestamp in csv
        with open(filename, "a", encoding="utf8") as open_file:
            open_file.write(
                f"{now},{airline},{flight_number},{flight_date},{departure},{arrival},{aircraft},{staff_price},{google_price},{diff_price}\n",)
        return render_template("addflight.html",
                               airline=airline,
                               flight_number=flight_number,
                               flight_date=flight_date,
                               departure=departure,
                               arrival=arrival,
                               aircraft=aircraft,
                               staff_price=staff_price,
                               google_price=google_price,
                               diff_price=diff_price)

# create some statistics for the flights


@app.route('/stats')
def stats():
    df = pd.read_csv(r'newFlights.csv')  # read the csv file into a dataframe

    # block 1 - simple stats using default calculations
    mean1 = round(df['staffPrice'].mean(), 2)
    sum1 = round(df['staffPrice'].sum(), 2)
    max1 = df['staffPrice'].max()
    min1 = df['staffPrice'].min()
    count1 = df['staffPrice'].count()
    median1 = df['staffPrice'].median()
    std1 = round(df['staffPrice'].std(), 2)
    var1 = df['staffPrice'].var()
    mostaircraft = df['aircraft'].mode()
    mostairline = df['airline'].mode()
    mostdeparture = df['departure'].mode()
    mostarrival = df['arrival'].mode()

    # block 2 - data manipulation to create get in handy format
    mostairline = mostairline.to_string(index=False, header=False)
    mostaircraft = mostaircraft.to_string(index=False, header=False)
    mostdeparture = mostdeparture.to_string(index=False, header=False)
    mostarrival = mostarrival.to_string(index=False, header=False)

    # call departure color function
    mapping_colors = name_to_color(
        df.departure, 125, 255, 0, 185, 0, 185)

    # define dataframe for the plot
    abflug = df['departure'].unique()
    abflugzaehler = df['departure'].value_counts()

    # create a plotly figure
    fig_departure = px.bar(x=abflug, y=abflugzaehler,
                           color=abflug, color_discrete_map=mapping_colors)
    div_dep = plot(fig_departure, output_type="div")

    # call airline color function
    mapping_colorsairline = name_to_color(
        df.airline, 0, 125, 0, 75, 0, 75)

    # define dataframe for the plot
    airline = df['airline']
    diffpreis = df['diffPrice']

    # create a plotly figure
    fig_airline = px.bar(x=airline, y=diffpreis, color=airline,
                         color_discrete_map=mapping_colorsairline)
    div = plot(fig_airline, output_type="div")

    #  return the template with the data
    return render_template('stats.html',
                           mean1=mean1,
                           sum1=sum1,
                           max1=max1,
                           min1=min1,
                           count1=count1,
                           median1=median1,
                           std1=std1,
                           var1=var1,
                           mostaircraft=mostaircraft,
                           mostairline=mostairline,
                           mostdeparture=mostdeparture,
                           mostarrival=mostarrival,
                           div=div,
                           div_dep=div_dep)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)
