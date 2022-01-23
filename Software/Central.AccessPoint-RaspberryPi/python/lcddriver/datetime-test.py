import lcd
from time import time
from time import sleep
from datetime import datetime

lcd = lcd.lcd()

lcd.display_string("LCD", 1)
lcd.display_string("Hello World", 2)

while True:
  dateString = datetime.now().strftime('%b %d %y')
  timeString = datetime.now().strftime('%H:%M:%S')
  lcd.display_string(dateString, 3)
  lcd.display_string(timeString, 4)
  sleep(1)
