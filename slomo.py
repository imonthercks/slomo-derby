import RPi.GPIO as GPIO
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import CircularOutput
from time import sleep
import os
import vlc

print(GPIO.VERSION)

BUTTON_CHANNEL = 16
picam2 = Picamera2()
encoder = H264Encoder()
output = CircularOutput()
capture_file = "capture.h264"

def convert_to_slo_mo(filename, filemp4, frame_rate):
  convertstring = "MP4Box -fps " + str(frame_rate) + " -add " + filename + " " + filemp4
  os.system(convertstring)

def my_callback(channel):
  if (channel == 16):
    print(f'Event Detected on channel: {channel}')
    output.fileoutput = capture_file
    output.start()
    sleep(1)
    output.stop()

    convert_to_slo_mo(capture_file, "test.mp4", 15)

    player = vlc.MediaPlayer('test.mp4')
    player.play()
  
def setup():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(BUTTON_CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  picam2.video_configuration.controls.FrameRate = 90
  picam2.configure("video")
  print("Setup Complete")

def loop():
  GPIO.add_event_detect(BUTTON_CHANNEL, GPIO.FALLING, callback=my_callback, bouncetime=1000)
  
  picam2.start_recording(encoder, output, Quality.HIGH)
  
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