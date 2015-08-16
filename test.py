import datetime
from database.state_change import StateChange
from services.thermostat import Thermostat

__author__ = 'Isaac'
from services.air_handler import AirHandler
from services.temp_monitor import TempMonitor
import services


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

    sensor = FakeTempSensor()
    services.TempMonitor = TempMonitor(sensor)

    heater = FakePin("heater")
    AC = FakePin("AC")
    fan = FakePin("fan")

    thermostat = Thermostat(AirHandler(fan, heater, AC), 5)

    thermostat.heat_target = 0
    thermostat.AC_target = 100
    thermostat.AC = True
    thermostat.heater = True

    print("Test temp=0")
    sensor.temp = 0
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=-1")
    sensor.temp = -1
    services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=5")
    sensor.temp = 5
    services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=6")
    sensor.temp = 6
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=5")
    sensor.temp = 5
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Test temp=-1")
    sensor.temp = -1
    services.TempMonitor.check_temp()
    assert heater.get() is True
    assert fan.get() is False
    assert AC.get() is False

    print("Heating passed testing AC")

    print("Test temp=101")
    sensor.temp = 101
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is True

    print("Test temp=95")
    sensor.temp = 95
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is True

    print("Test temp=94")
    sensor.temp = 94
    services.TempMonitor.check_temp()
    assert heater.get() is False
    assert fan.get() is False
    assert AC.get() is False

    print("Thermostat passed")

def test_repeating_schedule():
    from database.state_change_repeating import StateChangeRepeating
    from database import repeating_schedule

    repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    StateChangeRepeating(10 * 60 ** 2, 10, 100, False).save()
    StateChangeRepeating(10 * 60 ** 2 + 1, 10, 100, True).save()

    assert StateChangeRepeating.get_current(now).fan is True
    repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    StateChangeRepeating(7 * 24 * 60 ** 2 - 1, 10, 100, False).save()
    StateChangeRepeating(0, 10, 100, True).save()
    assert StateChangeRepeating.get_current(now).fan is True
    repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 1)
    StateChangeRepeating(7 * 24 * 60 ** 2 + 1, 10, 100, False).save()
    StateChangeRepeating(60*60+1, 10, 100, True).save()
    assert StateChangeRepeating.get_current(now).fan is False
    repeating_schedule.remove()

    now = datetime.datetime(2017, 1, 2, 0)
    StateChangeRepeating(7 * 24 * 60 ** 2, 10, 100, False).save()
    StateChangeRepeating(1, 10, 100, True).save()
    assert StateChangeRepeating.get_current(now).fan is False
    repeating_schedule.remove()

    print("repeating schedule passed")

def test_schedule():
    from database import schedule
    start = datetime.datetime(2017, 1, 1, 1)
    end = datetime.datetime(2017, 1, 2, 1)
    StateChange(start, end, 0, 0, True).save()

    start = datetime.datetime(2017, 1, 2, 1)
    end = datetime.datetime(2017, 1, 2, 1)
    StateChange(start, end, 0, 0, False).save()

    now = datetime.datetime(2017, 1, 1, 1)
    assert StateChange.get_current(now).fan is True
    schedule.remove()

    start = datetime.datetime(2017, 1, 2, 1)
    end = datetime.datetime(2017, 1, 2, 1)
    StateChange(start, end, 0, 0, False).save()

    start = datetime.datetime(2017, 1, 1, 1)
    end = datetime.datetime(2017, 1, 2, 1)
    StateChange(start, end, 0, 0, True).save()

    now = datetime.datetime(2017, 1,  1, 1)
    assert StateChange.get_current(now).fan is True
    schedule.remove()
    print("schedule passed")


def test_temp_log():
    sensor = FakeTempSensor()
    services.TempMonitor = TempMonitor(sensor)
    from database import temps
    temps.remove()
    from database.temp_log import TempLog
    sensor.temp = 12
    services.TempMonitor.check_temp()

    assert TempLog.get_all()[0].temp == 12

    sensor.temp = 3
    services.TempMonitor.check_temp()

    assert TempLog.get_all()[0].temp == 12
    assert TempLog.get_all()[1].temp == 3
    print("temp log passed")


def test_state_log():
    sensor = FakeTempSensor()
    services.TempMonitor = TempMonitor(sensor)
    from database import states
    states.remove()
    from database.state_log import StateLog
    now = datetime.datetime(2017, 1,  1, 1)
    StateLog(now, False, False, False).save()
    assert StateLog.get_all()[0].fan is False
    print("state log passed")




test_temp_monitor()
test_thermostat()
test_repeating_schedule()
test_schedule()
test_temp_log()
test_state_log()