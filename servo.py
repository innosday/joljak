import RPi.GPIO as GPIO
import time


class Servo:
    def __init__(self,pin,maxDuty=12,minDuty=3):
        self.pin = pin
        self.maxDuty = maxDuty
        self.minDuty= minDuty
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin,GPIO.OUT)
        self.servo = GPIO.PWM(self.pin,50)
        self.servo.start(0)

    def servoPos(self,degree,delay=1):
        if degree >180:
            degree = 180

        duty = self.maxDuty+(degree*(self.maxDuty-self.minDuty)/180.0)
        self.servo.ChangeDutyCycle(duty)
        time.sleep(delay)

    def cleanup(self):
        self.servo.stop()
        GPIO.cleanup(self.pin)
