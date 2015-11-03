# PITherm
A Raspberry PI as a thermostat 

## Database
A Flask based Python script which exposes a restful api to get and set schedule information and get and set temperature

example usage: `sudo python TemperatureMonitor.py [StateController]`


### API
Uses basic auth for all routes

* GET schedule/repeating Lists all scheduled repeating state changes in order of the next to occur
* GET schedule/repeating/next get the next repeating state change to happen
* GET schedule/repeating/current get the current repeating state change active
* POST schedule/repeating Add a scheduled repeating state change `{week_time, /*seconds into the week*/ _id, state: {AC_target, heater_target, fan} } `
* DELETE schedule/repeating Remove a scheduled state change by id

* GET schedule/ Lists all scheduled  state changes in order of the next to occur
* GET schedule/next get the next state change to happen
* GET schedule/current get the current state change active
* POST schedule/ Add a scheduled state change `{start, /*linux time*/ end, _id, state: {AC_target, heater_target, fan} } `
* DELETE schedule/repeating Remove a scheduled state change by id

#### Planned

* POST temp/ informs the system of a temperature change data should be cleaned as much as possible as no modifications will be made by the Database `{time, /*linux time when temp was recorded*/ sensor_id (string), temp: /*temperature in centigrade*/}`
* get temp/ returns the last temperature from each sensor id

# Planned

## TemperatureMonitor
A script to monitor temperature will broadcast this information to the Database and the StateController

example usage: `sudo python TemperatureMonitor.py [Database URL] [StateController URL]`

## StateController
A script to monitor temperature changes and the state change schedule and based on these request a change to the state when needed

### API
* POST temp/ informs the system of a temperature change data should be cleaned as much as possible as no modifications will be made by the Database `{time, /*linux time when temp was recorded*/ sensor_id (string), temp: /*temperature in centigrade*/}`
* POST on_state_change/ inform the controller that the state has been changed


## ForcedAirController
A script to actually control the air handling system

### API

* POST ac/:on_or_off Sets ac state to on_or_off
* POST heater/:on_or_off Sets Heater to on_or_off
* POST fan/:on_or_off Sets fan to on_or_off by default
