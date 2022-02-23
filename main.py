import math
from datetime import datetime
import time


# bepaal op basis van de gewenste eindtijd met hoeveel uren en minuten je de wasmachine moet uistellen.
# Als je weet dat de wasmachine er t tijd (bijv. 02:40) over doet.


# functie die de starttijd bepaalt.

def assertTime(time: str):
    assert len(time) == 5, 'Please use the format 00:00 for the time'
    assert time[0:2].isdigit() and time[3:5].isdigit(), 'Please use the format 00:00 for the time'
    assert time[2] == ':', 'Please use the format 00:00 for the time'

def timeToSeconds(time: str):
    """
    >>> timeToSeconds('13:08')
    47280
    """

    assertTime(time)

    ftr = [3600, 60]
    return sum([a * b for a, b in zip(ftr, map(int, time.split(':')))])


def seconds2String(sec: int):
    hours, remainder = divmod(sec, 3600)
    minutes, seconds = divmod(remainder, 60)

    return '{:02}:{:02}'.format(int(hours), int(minutes))


def getStartTime(endTime, duration):
    """
    >>> getStartTime('08:00','02:40')
    '05:20'
    >>> getStartTime('01:00','02:00')
    '23:00'
    """

    import datetime
    endTimeSeconds = timeToSeconds(endTime)
    durationSeconds = timeToSeconds(duration)
    startTimeSeconds = endTimeSeconds - durationSeconds

    if startTimeSeconds < 0:
        startTimeSeconds = 24 * 3600 + startTimeSeconds

    return seconds2String(startTimeSeconds)


def getOffset(endTime: str, duration, now=datetime.now().strftime("%H:%M")):
    """
    >>> getOffset('07:40','02:40','23:00')
    '06:00'
    >>> getOffset('08:00','02:40')
    """

    startTimeSeconds = timeToSeconds(getStartTime(endTime, duration))
    nowSeconds = timeToSeconds(now)

    if nowSeconds > startTimeSeconds:
        offSet = (24 * 3600 - nowSeconds) + startTimeSeconds
    else:
        offSet = nowSeconds - startTimeSeconds

    return seconds2String(offSet)


def getMinutes(minutes: str):
    return int(minutes.split(':')[1])


def getHours(hours: str):
    return int(hours.split(':')[0])


def getOptimalOffset(endTime: str, duration, increment, now=datetime.now().strftime("%H:%M")):
    """
    >>> getOptimalOffset('08:00', '02:40',15)
    """

    offSet = getOffset(endTime, duration, now)
    minutes = getMinutes(now)
    hours = getHours(offSet)

    if math.fabs(minutes - (minutes // increment * increment)) < math.fabs(
            minutes - (minutes // increment * increment + increment)):
        optimalMinutes = (minutes // increment) * increment
    else:
        optimalMinutes = minutes // increment * increment + increment

    return str(hours) + str(':') + str(optimalMinutes)
