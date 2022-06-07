# ✈️ myFlights ✈️

### by 🐣 schlaepfAIR

With this python tool you wil have the possibility to save all your Flights, so you create your own Flightdiary!
In addition to your Flightdiary you will see your savings for each fliht

## Idea of Features

##### Flight Form:

![Add Flight Form](/img/AddFlight.jpg)

- Entering all the relevant Flightinformation

##### Overview / Statistic:

![Flight Overview](/img/FlightOverview.jpg)

- Chronological list view of entered flights, including savings
- Filterfunctionality (Date, Airline, Departure)
- Overview for all savings, filtering per year, airline, etc

##### _Optional_:

- Get Airline and/or Airport detailed information from a external source (openAPI)
- Share your diary via export or link

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

_schlaepfAIR is a DBM parttime student @ the FHGR in Chur and learning more interesting python stuff during the spring semester 2022. In addition this guy works for an airline and is travelling around the world with high employe discounts in the fares_

## Components and Installation

##