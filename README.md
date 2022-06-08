# ✈️ Your Flightdiary✈️
###### With this python tool you will have the possibility to save all your Flights, so you create your own Flightdiary!

***
## why this project 
There are many flight diaries, but none with the price information. As an airline employee, the flight benefits are an exciting benefit. this project should offer the possibility of a flight diary in which the savings of an airline employee are also recorded.

##### problem definition
> - no recording of the ticket price paid
> - no overview or statistics on the savings with discounted employee tickets

##### solving the problems
with this tool, flights can be recorded with all relevant information. in addition, the paid price as well as the official price (google.com/flights) can be entered. the application automatically calculates the savings. In the statistics section, the interesting and important key figures are then displayed in a low-threshold from. The flight diary can also be imported as a csv file directly from large providers of official flight diaries.

***
## Setup 
The code of this project requires at least python version 3.9.5 or higher.
##### libraries

* Flask
    > Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.
    How to install: pip install Flask
* Datetime
    > Datetime is used to genereate a timestamp of the single flight entry.
    How to install: pip install datetime
* Plotly
    > Plotly provides online graphing, analytics, and statistics tools. This library is used to generate statistics in the project. 
    How to install: pip install plotly
* Pandas
    > pandas is a library for the Python to data manipulation and analysis.
    How to install: pip install pandas
* Random
    > This random library is in place for a funny reason, with the library the application will create different colors which are used in the bars of the plots in the statistics section
    Random is already a part of the python installation. 
* OS
    > OS is used for checking if the csv file already exists. 
    > No installation needed, because it is a default python module. 

##### installation and startup 
- After you cloned at least the code-folder you just have to run the flight.py with python. 
- Open your internet browser an enter http://localhost:5000/ or http://127.0.0.1:5000 (debugger mode is active)
- **first time start:** when you start the application the first time you have to add a flight before you can go to statistics, on the first run, also the csv file will be generated. 
    > Default: in the flight.py on line 15 the filename variable is defined, feel free to change it in whatever you like, it is just important that you still use the .csv fileextension.
    > **Demo Content:** after starting flight.py you can also open http://localhost:5000/demo. This will create random 350 Flights.
#
***
## Architecture
##### _Flow_: 

```mermaid
flowchart TB
    subgraph initialize '/'
    A([Start: run flight.py])--> B{check if *.csv exists}
    B -- Yes --> G
    B -- No --> F
    end
    F[[create new *.csv]] --> G
    G[load *.csv and render in table.html]

    G --  add Flight --> H
    G --  show Statistics --> I
    I -- go to overview --> G
    H -- go to overview --> G
    subgraph addFlight '/add' 
    H[[add flight '/add']]
    end
    I .-> H
    subgraph statistics '/stats'
    I[load stats '/stats']
    end
```
#
***
## Unsolved Problems and Improvements
- Right now, no possibility to modify flights on the web interface, manually possible in the easy reading csv file
- No external API connection to validate flight relevant information (i.e. Airportcodes, Airlinecodes)

***

© schlaepfAIR 
***
_schlaepfAIR is a DBM parttime student @ the FHGR in Chur and learning more interesting python stuff during the spring semester 2022. In addition this guy works for an airline and is travelling around the world with high employe discounts in the fares_
