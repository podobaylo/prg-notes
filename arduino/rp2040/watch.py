##### CircuitPython 8.2.10 ################
##### https://circuitpython.org/downloads #
###########################################
# http://ur4uqu.com/
# CircuitPython
# rp2040-zero board
# http://ur4uqu.com/cam/user/Main/tmp/v2024-06-15_11-48-58.jpg
# http://ur4uqu.com/cam/user/Main/tmp/v2024-06-15_23-03-44.jpg

import time
import board
import busio
import digitalio
import TM1637
import adafruit_ds1307
from   adafruit_bme280 import basic as adafruit_bme280
from   lcd.lcd import LCD, CursorMode
from   lcd.i2c_pcf8574_interface import I2CPCF8574Interface

ldisplay = TM1637.TM1637(board.GP1, board.GP0); ldisplay.brightness(0)

i2c = busio.I2C(board.GP15, board.GP14)

bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)
rtc = adafruit_ds1307.DS1307(i2c)


### globals
hourly_beep_played = False
curent_time = rtc.datetime

### beeper #######
beep = digitalio.DigitalInOut(board.GP12)
beep.direction = digitalio.Direction.OUTPUT

def beeper(bcount=1, tbeep=0.1, tdelay=0 ):
    for _ in range(bcount):
        beep.value = True
        time.sleep(tbeep)
        beep.value = False
        time.sleep(tdelay)
###
def morse_transmitter(message, wpm=12):
 
    morse_dict = {
        'A': '.-',
        'B': '-...',
        'C': '-.-.',
        'D': '-..',
        'E': '.',
        'F': '..-.',
        'G': '--.',
        'H': '....',
        'I': '..',
        'J': '.---',
        'K': '-.-',
        'L': '.-..',
        'M': '--',
        'N': '-.',
        'O': '---',
        'P': '.--.',
        'Q': '--.-',
        'R': '.-.',
        'S': '...',
        'T': '-',
        'U': '..-',
        'V': '...-',
        'W': '.--',
        'X': '-..-',
        'Y': '-.--',
        'Z': '--..',
        '0': '-----',
        '1': '.----',
        '2': '..---',
        '3': '...--',
        '4': '....-',
        '5': '.....',
        '6': '-....',
        '7': '--...',
        '8': '---..',
        '9': '----.',
        '.': '.-.-.-',
        ',': '--..--',
        '?': '..--..',
        ';': '-.-.-',
        ':': '---...',
        '-': '-....-',
        '(': '-.--.',
        ')': '-.--.-',
        '@': '.--.-.',
        '!': '-.-.--',
        '&': '.-...',
        '=': '-...-',
        '+': '.-.-.',
        '$': '...-..-',
        '/': '-..-.'
    }

    dot_duration = 1.2 / wpm

    morse_message = ''.join(morse_dict.get(char.upper(), ' ') + ' ' for char in message)

    for symbol in morse_message:
        if symbol == '.':
            beeper(1, dot_duration, dot_duration)
        elif symbol == '-':
            beeper(1, 3 * dot_duration, dot_duration)
        else:
            time.sleep(3 * dot_duration)  # пауза
############


### set zero altimetr
#bme280.sea_level_pressure = 1013.25
bme280.sea_level_pressure = bme280.pressure

###### set time #####
if False:  # change to True if you want to set the time!
    #                     year,   mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2024,   6,   14,   23,   46,  30,  5,    -1,   -1))
    print("Setting time to:", t)
    rtc.datetime = t
    print()
###################

interface = I2CPCF8574Interface(i2c, 0x27)
lcd = LCD(interface, num_rows=2, num_cols=16)
lcd.set_cursor_mode(CursorMode.HIDE)
lcd.clear()

### variant-1
def myshow():
    t = curent_time

    ldisplay.show("{:02}{:02}".format(t.tm_hour, t.tm_min))

    st  = "{:04}-{:02}-{:02} {} {:02}:{:02}:{:02} {} {} {} {} ".format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_wday, t.tm_hour, t.tm_min, t.tm_sec, "%0.2fC" % bme280.temperature, "%0.1f%%" % bme280.relative_humidity, "%0.1fhP" % bme280.pressure, "%0.2fm" % bme280.altitude)
    st1 = "{}  {}        ".format("%0.2fC" % bme280.temperature, "%0.1f%%" % bme280.relative_humidity)
    st2 = "{} {}         ".format("%0.1fhP" % bme280.pressure, "%0.2fm" % bme280.altitude)

    lcd.set_cursor_pos(0, 0); lcd.print(st1[:16])
    lcd.set_cursor_pos(1, 0); lcd.print(st2[:16])

    print(st)

### variant-2 (time-profiled)
def mmyshow():
    t = curent_time

    hour = "{:02}".format(t.tm_hour)
    minute = "{:02}".format(t.tm_min)
    ldisplay.show(hour + minute)

    temp = bme280.temperature
    humidity = bme280.relative_humidity
    pressure = bme280.pressure
    altitude = bme280.altitude

    st1 = "{:0.2f}C  {:0.1f}%".format(temp, humidity)
    st2 = "{:0.1f}hP {:0.2f}m".format(pressure, altitude)

    lcd.set_cursor_pos(0, 0); lcd.print(st1[:16])
    lcd.set_cursor_pos(1, 0); lcd.print(st2[:16])

    st = "{:04}-{:02}-{:02} {} {}:{:02}:{:02} {:0.2f}C {:0.1f}% {:0.1f}hP {:0.2f}m".format(
        t.tm_year, t.tm_mon, t.tm_mday, t.tm_wday, hour, t.tm_min, t.tm_sec, temp, humidity, pressure, altitude)
    print(st)

###
def check_alarm(alarm_hour, alarm_minute):
    t = curent_time
    if t.tm_hour == alarm_hour and t.tm_min == alarm_minute:
        beeper(1, 0.05, 0)

###
def check_hourly_beep():
    global hourly_beep_played
    t = curent_time
    if t.tm_min == 0 and not hourly_beep_played:
        if t.tm_hour > 8 and t.tm_hour < 22: ######## set silece...
            beeper(1, 0.3, 0)
        hourly_beep_played = True
    elif t.tm_min != 0:
        hourly_beep_played = False


### Init proc ###
myshow()
morse_transmitter("{:02}/{:02}".format(curent_time.tm_hour,curent_time.tm_min), 18)


#### Main Loop ####
while True:
    curent_time = rtc.datetime
    mmyshow()
    check_hourly_beep()

### set alarms ###
    check_alarm(  9, 0 )
    check_alarm( 13, 0 )
    check_alarm( 14, 0 )
    check_alarm( 18, 0 )
##################

    time.sleep(0.5)
###################
