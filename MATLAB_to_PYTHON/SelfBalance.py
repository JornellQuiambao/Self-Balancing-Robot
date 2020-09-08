import RPi.GPIO as GPIO
import time
import math
from pidcontroller import PIDController

GPIO.setmode(GPIO.BCM)

# *** Change these variables ***
# GPIO pins
g0 = 1
g1 = 1
g2 = 1
g3 = 1

# pwm frequency
PWM_freq = 100 # wheel speed

# PID values
set_Kp = 1
set_Ki = 1
set_Kd = 1

# Desired Angle
set_theta = 0

# *** Setup for GPIO pins and PWM ***

GPIO.setup(g0,GPIO.OUT) # back
GPIO.setup(g1,GPIO.OUT) # forward
GPIO.setup(g2,GPIO.OUT) # back
GPIO.setup(g3,GPIO.OUT) # forward

PWM1 = GPIO.PWM(g0, PWM_freq)
PWM2 = GPIO.PWM(g1, PWM_freq)
PWM3 = GPIO.PWM(g2, PWM_freq)
PWM4 = GPIO.PWM(g3, PWM_freq)

PWM1.start(0)
PWM2.start(0)
PWM3.start(0)
PWM4.start(0)

# *** Functions for driving motors ***
def driveBack(v):
    PWM1.ChangeDutyCycle(v) 
    GPIO.output(g1, GPIO.LOW)
    PWM3.ChangeDutyCycle(v)
    GPIO.output(g3, GPIO.LOW)

def driveForward(v):
    GPIO.output(int1, GPIO.LOW)
    PWM2.ChangeDutyCycle(v)
    GPIO.output(int3, GPIO.LOW)
    PWM4.ChangeDutyCycle(v)

def driveStop():
	# turn motors off
    GPIO.output(g0, GPIO.LOW)
    GPIO.output(g1, GPIO.LOW)
    GPIO.output(g2, GPIO.LOW)
    GPIO.output(g3, GPIO.LOW)

# *** Helper Functions for math and trig ***

def distance(a,b):
	# d^2 = a^2 + b^2
	d = math.sqrt((a*a)+(b*b))
	return d


while True:

	# *** Setup and get sensor data ***

	sensor_value = 0

	# *** Setup and update PID feedback controller ***

	PID = PIDController(P=set_Kp, I=set_Ki, D=set_Kd, theta=set_theta)
	drive_value = PID.update(sensor_value)

	if (drive_value < 0):
		driveBack(drive_value)
	elif (drive_value > 0):
		driveForward(drive_value)
	else:
		driveStop()

	time.sleep(0.1)

























