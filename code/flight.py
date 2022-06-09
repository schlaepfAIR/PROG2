# import required libraries
from flask import Flask
from flask import render_template
from flask import request
from datetime import datetime, timedelta
import plotly.express as px
from plotly.offline import plot
import pandas as pd  # pandas for dataframe manipulation
import random  # to create funny colors for the statistics
import os.path  # to check file exists
from os import path
import csv

app = Flask(__name__)

# feel free to change the filename to something else
filename = 'Flights.csv'

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
    if path.exists(filename):  # check if the file exists
        df = pd.read_csv(filename, header=0)
        df = df.sort_values(by=['flightDate'])
    else:  # if the file does not exist, create a new one
        df = pd.DataFrame(columns=['created', 'airline', 'flightNumber', 'flightDate',
                                   'departure', 'arrival', 'aircraft', 'staffPrice',
                                   'googlePrice', 'diffPrice',
                                   ])
        df.to_csv(filename, header=True, index=False)

    # to read and sort the csv file using the pandas library
    df = pd.read_csv(filename, header=0)
    df = df.sort_values(by=['flightDate'])
    myData = df.values
    return render_template('table.html', myData=myData)


# add a new flight using get and post methods

@app.route("/add", methods=["get", "post"])
def addFlight():
    # filename = 'newFlights.csv'  # define the filename

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
    df = pd.read_csv(filename)  # read the csv file into a dataframe

    # block 1 - simple stats using default calculations
    mean1 = round(df['staffPrice'].mean(), 2)
    sum1 = round(df['diffPrice'].sum(), 2)
    count1 = df['staffPrice'].count()
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
                           color=abflug, color_discrete_map=mapping_colors, title="Airport departure numbers", labels=dict(x="Departure Airport ", y="Amount"))
    fig_departure.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    div_dep = plot(fig_departure, output_type="div")

    # call airline color function
    mapping_colorsairline = name_to_color(
        df.airline, 0, 125, 0, 75, 0, 75)

    # define dataframe for the plot
    airline = df['airline']
    diffpreis = df['diffPrice']

    # create a plotly figure
    fig_airline = px.bar(x=airline, y=diffpreis, color=airline,
                         color_discrete_map=mapping_colorsairline, title="Savings per Airline", labels=dict(x="Airline ", y="Saved money"))
    fig_airline.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    div = plot(fig_airline, output_type="div")

    #  return the template with the data
    return render_template('stats.html',
                           mean1=mean1,  # used
                           sum1=sum1,  # used
                           count1=count1,  # used
                           mostaircraft=mostaircraft,  # used
                           mostairline=mostairline,  # used
                           mostdeparture=mostdeparture,  # used
                           mostarrival=mostarrival,  # used
                           div=div,
                           div_dep=div_dep)


@app.route('/about')
def about():
    return render_template('about.html')

# create demo data for the flights


@app.route('/demo')
def demo():
    records = 350
    fieldnames = ['created', 'airline', 'flightNumber', 'flightDate', 'departure',
                  'arrival', 'aircraft', 'staffPrice', 'googlePrice', 'diffPrice']
    writer = csv.DictWriter(open(filename, "w"), fieldnames=fieldnames)
    airline = ['LX', 'WK', 'LH', 'UA', 'AA', 'B6', 'DL', 'EV', 'F9', 'HA',
               'HP', 'MQ', 'NK', 'OO', 'PA', 'SQ', 'UA', 'VX', 'WN', 'XE', 'YV', 'ZV']
    departure = ['ZRH', 'GVA', 'FRA', 'JFK', 'MUC', 'VIE', 'HKG', 'SIN', 'UIO', 'BOG', 'AMS', 'SCL',
                 'EZE', 'ORD', 'BRU', 'MXP', 'FDH', 'HAM', 'BER', 'LCY', 'OUG', 'SYD', 'IAH', 'IAD', 'SFO']
    arrival = ['ZRH', 'GVA', 'FRA', 'JFK', 'MUC', 'VIE', 'HKG', 'SIN', 'UIO', 'BOG', 'AMS', 'SCL',
               'EZE', 'ORD', 'BRU', 'MXP', 'FDH', 'HAM', 'BER', 'LCY', 'OUG', 'SYD', 'IAH', 'IAD', 'SFO']
    aircraft = ['A320', 'A321', 'A330', 'A340', 'A350', 'A380', 'B747', 'B757',
                'B767', 'B777', 'B787', 'B789', 'A220', 'E90', 'E95', 'DH8', 'AirForceONE']
    min_year = 2003
    max_year = datetime.now().year
    start = datetime(min_year, 1, 1, 00, 00, 00)
    years = max_year - min_year+1
    end = start + timedelta(days=365 * years)

    writer.writerow(dict(zip(fieldnames, fieldnames)))
    for i in range(0, records):
        staffprice = float(random.randint(100, 5000))
        googleprice = staffprice * round(random.uniform(1.1, 1.6), 2)
        googleprice = round(googleprice, 2)
        diffprice = (int(googleprice)) - (int(staffprice))
        writer.writerow(dict([
            ('created', datetime.now()),
            ('airline', random.choice(airline)),
            ('flightNumber', str(random.randint(1, 3000))),
            ('flightDate', start + (end - start) * random.random()),
            ('staffPrice', staffprice),
            ('googlePrice', googleprice),
            ('diffPrice', diffprice),
            ('departure', random.choice(departure)),
            ('arrival', random.choice(arrival)),
            ('aircraft', random.choice(aircraft))]))

    return render_template('demo.html', records=records)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
