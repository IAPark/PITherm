import datetime

__author__ = 'Isaac'
from services.air_handler import AirHandler
from services.temp_monitor import TempMonitor
from services import Services


class FakeTempSensor:
    def __init__(self):
        self.temp = 0

    def get_temp(self):
        return self.temp



def test_temp_monitor():

    sensor = FakeTempSensor()
    temp_monitor = TempMonitor(sensor)

    global temp
    temp = -1
    @temp_monitor.temp_changed
    def listener(temperature):
        global temp
        temp = temperature
    temp_monitor.check_temp()

    assert temp == 0  # temp should have been set by the listener

    sensor.temp = 100
    temp_monitor.check_temp()
    assert temp == 100

    sensor.temp = -100
    temp_monitor.check_temp()
    assert temp == -100

    sensor.temp = 0
    temp_monitor.check_temp()
    assert temp == 0

    print("temp_monitor passed")

def test_thermostat():
    class FakePin:

        def __init__(self, name):
            self.name = name
            self.state = False

        def sense(self):
            return False

        def set(self, state):
            self.state = state


        def get(self):
            return self.state

    class FakeDB:
        def log_air_handler_state(self, AC, heater, fan):
            return

    import services
    reload(services)
    Services = services.Services

    sensor = FakeTempSensor()
    Services.TempMonitor = TempMonitor(sensor)

    import services.thermostat
    reload(services.thermostat)
    Thermostat = services.thermostat.Thermostat

    heater = FakePin("heater")
    AC = FakePin("AC")
    fan = FakePin("fan")

    thermostat = Thermostat(AirHandler(fan, heater, AC, FakeDB()), 5)

    thermostat.heat_target = 0
    thermostat.AC_target = 100
    thermostat.AC = True
    thermostat.heater = True

    print("Test temp=0")
    sensor.temp = 0
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=-1")
    sensor.temp = -1
    Services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=5")
    sensor.temp = 5
    Services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=6")
    sensor.temp = 6
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=5")
    sensor.temp = 5
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=-1")
    sensor.temp = -1
    Services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Heating passed testing AC")

    print("Test temp=101")
    sensor.temp = 101
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is True

    print("Test temp=95")
    sensor.temp = 95
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is True

    print("Test temp=94")
    sensor.temp = 94
    Services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Thermostat passed")

def test_database():
    sensor = FakeTempSensor()
    Services.TempMonitor = TempMonitor(sensor)
    from services.database import DB



    db = DB()

    db.repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    db.set_repeating_state_change(10*60**2, 10, 100, False)
    db.set_repeating_state_change(10*60**2 + 1, 10, 100, True)

    print(db.get_repeating_change(now))
    assert db.get_repeating_change(now)["time_delta"] == (-10*60**2 - 1) % (7*24*60**2)
    assert db.get_repeating_change(now)["state"]["fan"] is True
    db.repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    db.set_repeating_state_change(7*24*60**2-1, 10, 100, False)
    db.set_repeating_state_change(0, 10, 100, True)
    assert db.get_repeating_change(now)["state"]["fan"] is True
    db.repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    db.set_repeating_state_change(7*24*60**2, 10, 100, False)
    db.set_repeating_state_change(1, 10, 100, True)
    assert db.get_repeating_change(now)["state"]["fan"] is False
    db.repeating_schedule.remove()


    now = datetime.datetime(2017, 1, 2, 0)
    db.set_repeating_state_change(7*24*60**2, 10, 100, False)
    db.set_repeating_state_change(1, 10, 100, True)
    assert db.get_repeating_change(now)["state"]["fan"] is False
    db.repeating_schedule.remove()





test_temp_monitor()
test_thermostat()
test_database()
