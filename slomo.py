import RPi.GPIO as GPIO
from time import sleep

print(GPIO.VERSION)

BUTTON_CHANNEL = 16

def my_callback(channel):
  if (channel == 16):
    print(f'Event Detected on channel: {channel}')
  
def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  print("Setup Complete")

def loop():
  GPIO.add_event_detect(BUTTON_CHANNEL, GPIO.FALLING, callback=my_callback, bouncetime=1000)
  
  while True:
    pass

def endprogram():
  print()
  print('program shutting down...')
  GPIO.cleanup()

if __name__ == '__main__':
  setup()
  try:
    loop()
  except KeyboardInterrupt:
    endprogram()    