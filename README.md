# PITherm
A Raspberry PI as a thermostat 

## Database
A Flask based Python script which exposes a restful api to get and set schedule information and get and set temperature

example usage: `sudo python TemperatureMonitor.py [StateController]`


### API
Uses basic auth for all routes

* GET schedule/repeating Lists all scheduled repeating state changes in order of the next to occur
* POST schedule/repeating Add a scheduled repeating state change `{week_time, /*seconds into the week*/ _id, state: {AC_target, heater_target, fan} } `

* GET schedule/ Lists all scheduled  state changes in order of the next to occur
* POST schedule/ Add a scheduled state change `{start, /*linux time*/ end, _id, state: {AC_target, heater_target, fan} } `

* POST temp/ informs the system of a temperature change data should be cleaned as much as possible as no modifications will be made by the Database `{time, /*linux time when temp was recorded*/ sensor_id (string), temp: /*temperature in centigrade*/}`
* get temp/ returns the last tempurature from each sensor id

## TemperatureMonitor
A script to monitor temperature will broadcast this information to the Database and the StateController

example usage: `sudo python TemperatureMonitor.py [Database URL] [StateController]`

## StateController
A script to monitor temperature changes and schedule changes and based on these request a change to the state when needed

### API
* POST temp/ informs the system of a temperature change data should be cleaned as much as possible as no modifications will be made by the Database `{time, /*linux time when temp was recorded*/ sensor_id (string), temp: /*temperature in centigrade*/}`
* POST setting/ inform the controller that the state has been changed


## ForcedAirController
A script to actual control the air handling system

### API

* POST ac/:on_or_off Sets ac to on_or_off
* POST heater:on_or_off Sets Heater to on_or_off
* POST fan/on_or_off Sets fan to on_or_off by default
