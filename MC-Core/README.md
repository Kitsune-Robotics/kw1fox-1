# MC-Core

The core's job is largely to centralize the doing of "stuff"
ALL the major tasks are defined here, and core runs them on a regular schedule
the idea is to do things and check things at regular times, for example, a weather
forecast task might check the weather and make a decision to fold panels

A battery health task that runs every 100 seconds might be tracking the battery health and
request the robot stop to preserve battery life

Core is responsible for ingesting data from `Robot-Connector` and storing it in the DB, as 
well as running other DB tasks.


In short, Core does all the dirty work. But on its own has no direct interface, relying on rest endpoints
for control and instruction.