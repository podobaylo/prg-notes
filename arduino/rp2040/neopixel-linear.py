# CircuitPython
# rp2040-zero board
# http://ur4uqu.com/
 
import time
import board
import neopixel
 
# Number of pixels
num_pixels = 12
 
# Create NeoPixel object
pixels = neopixel.NeoPixel(board.GP11, num_pixels, brightness=0.008, auto_write=False)
 
##############################################
# Function to display a number on the pixel strip
def display_number(n, pixels, num_pixels):
  """
  Displays a number on the pixel strip.
 
  Args:
    n: The decimal number to display (1 - 3 * num_pixels).
    pixels: The NeoPixel object.
    num_pixels: The number of pixels.
  """
 
  # Check if the number is in the valid range
  if not 1 <= n <= 3 * num_pixels:
    print(f"Error: Number must be in the range from 1 to {3 * num_pixels}.")
    return
 
  # Calculate the pixel index and color
  pixel_index = (n - 1) // 3
  color_index = (n - 1) % 3
 
  # Clear all pixels
  pixels.fill((0, 0, 0))
 
  # Turn on a single LED
  if color_index == 0:
    pixels[pixel_index] = (255, 0, 0)  # Red
  elif color_index == 1:
    pixels[pixel_index] = (0, 255, 0)  # Green
  else:
    pixels[pixel_index] = (0, 0, 255)  # Blue
 
  # Show the color
  pixels.show()
####################################
 
 
while True:
 
  # Loop to automatically display numbers
  for n in range(1, 3 * num_pixels + 1):
 
    # Display the number
    display_number(n, pixels, num_pixels)
 
    # Delay
    time.sleep(0.333)
