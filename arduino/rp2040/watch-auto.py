$ cat code.py 
import time
import board
import busio
import digitalio
import TM1637
import adafruit_ds1307
from myalarms import alarms
import microcontroller
import struct

# Переменные для корректировки времени
SECONDS_TO_ADD_PER_WEEK = 3
DAYS_BEFORE_ADJUSTMENT = 10

# Глобальные переменные для конфигурирования
I2C_SDA_PIN = board.GP15
I2C_SCL_PIN = board.GP14
TM1637_CLK_PIN = board.GP1
TM1637_DIO_PIN = board.GP0
BEEPER_PIN = board.GP6
RTC_ADDRESS = 0x68
CHECK_ADJUSTMENT_INTERVAL = 18000  # 300 минут
HOURLY_BEEP_START_HOUR = 8
HOURLY_BEEP_END_HOUR = 22
MORSE_WPM = 18
#PRESSURE_CORRECTION = 32.5
MAIN_LOOP_DELAY = 0.9


# Функция для проверки готовности устройства I2C
def wait_for_i2c_device(i2c, address, timeout=5):
    start_time = time.monotonic()
    while time.monotonic() - start_time < timeout:
        try:
            i2c.try_lock()
            if address in i2c.scan():
                i2c.unlock()
                return True
            i2c.unlock()
        except Exception as e:
            print(f"Ошибка при проверке I2C устройства: {e}")
        time.sleep(1)
    return False

# Инициализация I2C
try:
    i2c = busio.I2C(I2C_SDA_PIN, I2C_SCL_PIN)
except Exception as e:
    print(f"Ошибка при инициализации I2C: {e}")
    print(f"Используемые пины: SCL={I2C_SCL_PIN}, SDA={I2C_SDA_PIN}")
    i2c = None

# Инициализация TM1637 отдельно от I2C
try:
    ldisplay = TM1637.TM1637(TM1637_CLK_PIN, TM1637_DIO_PIN)
    ldisplay.brightness(0)
except Exception as e:
    print(f"Ошибка при инициализации TM1637: {e}")
    print(f"Используемые пины: CLK={TM1637_CLK_PIN}, DIO={TM1637_DIO_PIN}")
    ldisplay = None

# Проверка и инициализация RTC
rtc = None
if i2c and wait_for_i2c_device(i2c, RTC_ADDRESS):
    try:
        rtc = adafruit_ds1307.DS1307(i2c)
    except Exception as e:
        print(f"Ошибка при инициализации RTC: {e}")
else:
    print("RTC не обнаружен")

# Глобальные переменные
hourly_beep_played = False
curent_time = rtc.datetime if rtc else time.localtime()
cached_last_adjustment = None
last_nvm_read_time = 0


# Инициализация beeper
try:
    beep = digitalio.DigitalInOut(BEEPER_PIN)
    beep.direction = digitalio.Direction.OUTPUT
except Exception as e:
    print(f"Ошибка при инициализации beeper: {e}")
    beep = None

# Функция для сохранения даты последней корректировки в NVM
def save_last_adjustment_date():
    global cached_last_adjustment, last_nvm_read_time
    current_time = rtc.datetime if rtc else time.localtime()
    date_bytes = struct.pack('>HBB', current_time.tm_year, current_time.tm_mon, current_time.tm_mday)
    microcontroller.nvm[0:4] = date_bytes
    cached_last_adjustment = current_time
    last_nvm_read_time = time.time()

# Функция для загрузки даты последней корректировки из NVM
def load_last_adjustment_date():
    global cached_last_adjustment, last_nvm_read_time
    current_time = time.time()

    if cached_last_adjustment is None or (current_time - last_nvm_read_time) > 3600:  # 1 час
        try:
            date_bytes = microcontroller.nvm[0:4]
            unpacked_date = struct.unpack('>HBB', date_bytes)
            cached_last_adjustment = time.struct_time((unpacked_date[0], unpacked_date[1], unpacked_date[2], 0, 0, 0, 0, 0, -1))
            last_nvm_read_time = current_time
        except Exception as e:
            print(f"Ошибка при загрузке даты корректировки: {e}")
            cached_last_adjustment = rtc.datetime if rtc else time.localtime()
            last_nvm_read_time = current_time

    return cached_last_adjustment

# Функция для корректировки времени
def adjust_time(seconds_to_add):
    if rtc:
        current_time = rtc.datetime
        time_list = list(current_time)
        time_list[5] += seconds_to_add  # Добавляем секунды
        new_time = time.struct_time(tuple(time_list))
        rtc.datetime = new_time
        print(f"Время скорректировано на +{seconds_to_add} секунд")
        save_last_adjustment_date()
    else:
        print("RTC не инициализирован, корректировка времени невозможна")

# Функция для проверки необходимости корректировки времени
def check_time_adjustment():
    print("============check_adj==============")
    if rtc:
        t = rtc.datetime
        last_adjustment_date = load_last_adjustment_date()
        days_since_last_adjustment = (time.mktime(t) - time.mktime(last_adjustment_date)) // 86400  # 86400 секунд = 1 день
        if days_since_last_adjustment >= DAYS_BEFORE_ADJUSTMENT:
            weeks_passed = days_since_last_adjustment // DAYS_BEFORE_ADJUSTMENT
            seconds_to_add = weeks_passed * SECONDS_TO_ADD_PER_WEEK
            adjust_time(seconds_to_add)
    else:
        print("RTC не инициализирован, проверка корректировки времени невозможна")


# Функция для отображения данных
def myshow():
    t = curent_time

    year = "{:04}".format(t.tm_year)
    moth = "{:02}".format(t.tm_mon)
    day = "{:02}".format(t.tm_mday)
    wday = "{:01}".format(t.tm_wday)
    hour = "{:02}".format(t.tm_hour)
    minute = "{:02}".format(t.tm_min)
    seconds = "{:02}".format(t.tm_sec)

    if ldisplay:
        ldisplay.show(hour + minute)

    last_adjustment = load_last_adjustment_date();last_adj_str = "{:04}-{:02}-{:02}".format(last_adjustment.tm_year, last_adjustment.tm_mon, last_adjustment.tm_mday)


    print(f"{year}-{moth}-{day} - {wday} - {hour}:{minute}:{seconds}  Last_corr({SECONDS_TO_ADD_PER_WEEK}s): {last_adj_str}")

# Функция для beeper
def beeper(bcount=1, tbeep=0.1, tdelay=0):
    if beep:
        for _ in range(bcount):
            beep.value = True
            time.sleep(tbeep)
            beep.value = False
            time.sleep(tdelay)
    else:
        print("Beeper не инициализирован")

# Функция для передачи морзянки
def morse_transmitter(message, wpm=MORSE_WPM):
    morse_dict = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', '.': '.-.-.-', ',': '--..--', '?': '..--..',
        ';': '-.-.-', ':': '---...', '-': '-....-', '(': '-.--.', ')': '-.--.-',
        '@': '.--.-.', '!': '-.-.--', '&': '.-...', '=': '-...-', '+': '.-.-.',
        '$': '...-..-', '/': '-..-.'
    }

    dot_duration = 1.2 / wpm
    morse_message = ''.join(morse_dict.get(char.upper(),' ') + ' ' for char in message)

    for symbol in morse_message:
        if symbol == '.':
            beeper(1, dot_duration, dot_duration)
        elif symbol == '-':
            beeper(1, 3 * dot_duration, dot_duration)
        else:
            time.sleep(3 * dot_duration)  # пауза

# Функция для проверки будильников
def check_alarms():
    t = curent_time
    current_time = (t.tm_hour, t.tm_min)
    current_day = t.tm_wday

    for alarm in alarms:
        if current_time == alarm["time"]:
            if alarm["days"] is None or current_day in alarm["days"]:
                beeper(1, 0.05, 0)
                print(f"! Alarm {alarm['time'][0]:02d}:{alarm['time'][1]:02d}")

# Функция для проверки ежечасного сигнала
def check_hourly_beep():
    global hourly_beep_played
    t = curent_time
    if t.tm_min == 0 and not hourly_beep_played:
        if HOURLY_BEEP_START_HOUR < t.tm_hour < HOURLY_BEEP_END_HOUR:
            morse_transmitter("{:02}".format(t.tm_hour))
        hourly_beep_played = True
    elif t.tm_min != 0:
        hourly_beep_played = False


def nvm_fake():
    t = time.struct_time((2024, 7, 23, 0, 0, 0, 0, 0, 0))
    date_bytes = struct.pack('>HBB', t.tm_year, t.tm_mon, t.tm_mday)
    microcontroller.nvm[0:4] = date_bytes
    time.sleep(1)


### Init proc ###
print("\n---\n")
#nvm_fake()

curent_time = rtc.datetime
myshow()

# Корректировка времени при включении, если прошло DAYS_BEFORE_ADJUSTMENT дней
check_time_adjustment()

adjustment_check_counter = 0

#beeper()
morse_transmitter("{:02} {:02}".format(curent_time.tm_hour, curent_time.tm_min))



#### Main Loop ####
while True:
    if rtc:
        curent_time = rtc.datetime
    else:
        curent_time = time.localtime()

    myshow()
    check_hourly_beep()
    time.sleep(MAIN_LOOP_DELAY) # sleep !!!
    check_alarms()

    # Проверяем необходимость вызова check_time_adjustment()
    adjustment_check_counter += 1
    if adjustment_check_counter * MAIN_LOOP_DELAY >= CHECK_ADJUSTMENT_INTERVAL:
        check_time_adjustment()
        adjustment_check_counter = 0  # Сбрасываем счетчик
