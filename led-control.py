import time
import RPi.GPIO as GPIO

print("led control")

GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
pwm = GPIO.PWM(21, 120)  # set frequency as 120Hz
pwm.start(30)  # set duty as 100

try:
    while(True):
        sec = int(time.strftime('%S'))
        min = int(time.strftime('%M'))
        hour = int(time.strftime('%H'))
        # if sec < 5 and not min % 5:
        #     if hour >= 20 and not (hour == 23 and min >= 30):
        #         # GPIO.output(21, GPIO.HIGH) #BCM
        #         pwm.ChangeDutyCycle(100)
        #     elif hour < 4:
        #         # GPIO.output(21, GPIO.LOW)
        #         pwm.ChangeDutyCycle(1 - (hour + min/60) / 4)
        #     elif hour >= 18:
        #         pwm.ChangeDutyCycle((hour - 18 + min/60) / 2)
        #     else:
        #         pwm.ChangeDutyCycle(0)

except KeyboardInterrupt:
    print("ctrl + c:")
    GPIO.cleanup()
