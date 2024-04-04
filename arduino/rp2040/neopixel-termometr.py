# CircuitPython
# rp2040-zero board
 
import neopixel
import analogio
import digitalio
import board
import time
import math
 
# Диапазон напряжений
min_voltage = 1.2
max_voltage = 1.7
 
# Количество светодиодов
num_leds = 12
deltaleds=num_leds*3
 
delta=((max_voltage-min_voltage)/(num_leds*3))
 
ventilator = False
 
# Настройка аналогового входа
analog_in = analogio.AnalogIn(board.A0)
 
# Настройка WS2812B
pixels = neopixel.NeoPixel(board.GP11, num_leds, brightness=0.02,auto_write=True, pixel_order=neopixel.GRB)
 
########
leds = [
    digitalio.DigitalInOut(board.GP0),
    digitalio.DigitalInOut(board.GP1)
]
 
for led in leds:
    led.direction = digitalio.Direction.OUTPUT
########
 
# Функция для преобразования значения ADC в напряжение
def get_voltage(adc_value):
    return (adc_value * 3.3) / 65536
 
def yy(x):
  return -22.74 * x**2 + 72.82 * x - 10.34
 
def y(x):
  """
  Вычисляет значение y (температуру) по формуле:
 
  y = T1 = 1 / ((ln(R1) – ln(R2)) / B + 1 / T2)
 
  Args:
    x: значение напряжения на аналоговом входе (в вольтах)
 
  Returns:
    значение температуры T1 (в градусах Цельсия)
  """
 
  # Константы
  R25 = 22000  # Сопротивление NTC-термистора при 25°C (в Ом)
  B = 2000  # Температурный коэффициент (в К 2060..4300 )
  T25 = 298  # 25°C (в К)
  R_divider = 22000  # Сопротивление резистора делителя (в Ом)
 
  # Вычисление сопротивления NTC-термистора
  R1 = x * (R_divider + R25) / (3.3 - x)
 
  # Вычисление T1
  T1 = 1 / ((math.log(R1) - math.log(R25)) / B + 1 / T25)
 
  # Преобразование из Кельвинов в Цельсии
  T1_celsius = T1 - 273.15
 
  return T1_celsius+20
###########################
 
###########################
# Function to display a number on the pixel strip
def display_number(n, pixels, num_pixels):
  """
  Displays a number on the pixel strip.
 
  Args:
    n: The decimal number to display (1 - 3 * num_pixels).
    pixels: The NeoPixel object.
    num_pixels: The number of pixels.
  """
  # Clear all pixels
  pixels.fill((0, 0, 0))
 
  # Check if the number is in the valid range
  if not 1 <= n <= 3 * num_pixels:
    print(f"Error: Number must be in the range from 1 to {3 * num_pixels}.")
    return
 
  # Calculate the pixel index and color
  pixel_index = (n - 1) // 3
  color_index = (n - 1) % 3
 
 
  # Turn on a single LED
  if color_index == 0:
    pixels[pixel_index] = (255, 0, 0)  # Red
  elif color_index == 1:
    pixels[pixel_index] = (0, 255, 0)  # Green
  else:
    pixels[pixel_index] = (0, 0, 255)  # Blue
 
  # Show the color
#  pixels.show()
##########################
 
 
# Количество циклов
iterations = 0
# Время начала
start_time = time.monotonic()
 
# Цикл обновления
while True:
    # Считывание значения ADC # SIMPLE
#    adc_value = analog_in.value
 
###### Считывание значения ADC good ##########
# Количество замеров
    num_measurements = 8000
 
# Сумма значений ADC
    adc_value_sum = 0
 
# Цикл считывания значений ADC
    for i in range(num_measurements):
        time.sleep(0.0001)
        adc_value_sum += analog_in.value
 
# Среднее значение ADC
    adc_value = adc_value_sum / num_measurements
 
    # Преобразование ADC в напряжение
    voltage = get_voltage(adc_value)
 
    nn=(max_voltage-voltage)//delta
    if nn>deltaleds : nn=deltaleds
    if nn<1 : nn=1
 
 
    # Увеличение счетчика циклов
    iterations += 1
 
    # Обновление индикатора
    display_number(int(nn), pixels, num_leds)
 
    # Проверка времени
    if time.monotonic() - start_time >= 1:
 
        # Печать частоты обновления
 
#        print(f"F: {iterations} ")
 
        print(voltage)
 
        print(f"C = {y(voltage)}") #1.54
 
        print(f"nn={nn}")
 
#        print(f"delta={delta}")
 
        # Сброс счетчика циклов
        iterations = 0
 
        # Обновление времени начала
        start_time = time.monotonic()
 
################# rele ventilator ###
        if voltage > 1.45:
            ventilator = True
 
        if voltage < 1.44:
            ventilator = False
 
#        leds[0].value = ventilator
#################
