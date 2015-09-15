from pymongo import MongoClient


client = MongoClient()
db = client.PITherm
temps = db.temps
states = db.states
repeating_schedule = db.repeating_schedule
schedule = db.schedule