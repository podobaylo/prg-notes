##### CircuitPython 8.2.10 ################
##### https://circuitpython.org/downloads #
###########################################
# http://ur4uqu.com/
# CircuitPython
# rp2040-zero board

# Імпорт необхідних бібліотек
import board
import digitalio
import pwmio
import time

# Список світлодіодів, підключених до відповідних цифрових контактів
leds = [
    pwmio.PWMOut(board.GP0),
    pwmio.PWMOut(board.GP1),
    pwmio.PWMOut(board.GP2),
    pwmio.PWMOut(board.GP3),
    pwmio.PWMOut(board.GP4),
    pwmio.PWMOut(board.GP5),
    pwmio.PWMOut(board.GP6),
    pwmio.PWMOut(board.GP7),
]

# Максимальне значення duty_cycle
#maxpwm = 65535
maxpwm = 32000
mydelay = 0.0006

# Функція для поступового ввімкнення світлодіода
def encender_led(led_index, speed):
  duty = 1  # Початкове значення duty_cycle
  for i in range(maxpwm):
    duty += speed  # Збільшення duty_cycle на величину speed
    if duty < 0:
      duty = 0  # Обмеження duty_cycle мінімальним значенням
    elif duty > maxpwm:
      duty = maxpwm  # Обмеження duty_cycle максимальним значенням
      break  # Вихід із циклу, якщо duty_cycle досягнуто максимуму
    leds[led_index].duty_cycle = duty  # Встановлення duty_cycle для світлодіода
    time.sleep(mydelay)  # Пауза для плавного переходу
  leds[led_index].duty_cycle = maxpwm

# Функція для поступового вимкнення світлодіода
def apagar_led(led_index, speed):
  duty = maxpwm  # Початкове значення duty_cycle (максимальна яскравість)
  for i in range(maxpwm):
    duty -= speed  # Зменшення duty_cycle на величину speed
    if duty < 0:
      duty = 0  # Обмеження duty_cycle мінімальним значенням
      break  # Вихід із циклу, якщо duty_cycle досягнуто мінімуму
    elif duty > maxpwm:
      duty = maxpwm  # Обмеження duty_cycle максимальним значенням
    leds[led_index].duty_cycle = duty  # Встановлення duty_cycle для світлодіода
    time.sleep(mydelay)  # Пауза для плавного переходу
  leds[led_index].duty_cycle = 0

# Головний цикл програми (безкінечний)
while True:

  # Ввімкнення світлодіодів по черзі з певною швидкістю
  for i in range(len(leds)):
    encender_led(i, 1000)

  time.sleep(0.5)  # Пауза між вмиканням та вимиканням

  # Вимкнення світлодіодів по черзі з певною швидкістю
  # for i in range(len(leds) - 1, -1, -1): #️ розкоментувати для зворотного порядку
  for i in range(len(leds)):
    apagar_led(i, 1000)

  time.sleep(0.5)  # Пауза між вимиканням та вмиканням

