#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import math
import rospy

s2 = 23
s3 = 24
signal = 25
NUM_CYCLES = 10

lambda_r = 0
lambda_g = 0
lambda_b = 0
hsv_r = 0
hsv_g = 0
hsv_b = 0

rospy.init_node('colorpal_sensor')

def convert_rgb_vals(red,green,blue):
    global lambda_r,lambda_g,lambda_b
    global hsv_r,hsv_g,hsv_b
    lambda_r = red/10
    lambda_g = green/10
    lambda_b = blue/10
    hsv_r = math.fabs((lambda_r-620)/(130*255))*10000
    hsv_g = math.fabs((lambda_g-495)/(75*255))*10000
    hsv_b = math.fabs((lambda_b-450)/(45*255))*10000
    rospy.set_param("/colorpal/lambda/r",lambda_r)
    rospy.set_param("/colorpal/lambda/g",lambda_g)
    rospy.set_param("/colorpal/lambda/b",lambda_b)
    hsv_r = hsv_r if hsv_r<255 else 255
    hsv_g = hsv_g if hsv_g<255 else 255
    hsv_b = hsv_b if hsv_b<255 else 255


def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(s2,GPIO.OUT)
  GPIO.setup(s3,GPIO.OUT)
  print("\n")
  

def loop():
  temp = 1
  while(1):
    global lambda_r,lambda_g,lambda_b
    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.LOW)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start      #seconds to run for loop
    red  = NUM_CYCLES / duration   #in Hz
    print("red value - ",red)

    GPIO.output(s2,GPIO.LOW)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    blue = NUM_CYCLES / duration
    print("blue value - ",blue)

    GPIO.output(s2,GPIO.HIGH)
    GPIO.output(s3,GPIO.HIGH)
    time.sleep(0.3)
    start = time.time()
    for impulse_count in range(NUM_CYCLES):
      GPIO.wait_for_edge(signal, GPIO.FALLING)
    duration = time.time() - start
    green = NUM_CYCLES / duration
    print("green value - ",green)
    time.sleep(2)  
    convert_rgb_vals(red,green,blue)
    print("Lambda : ",lambda_r,lambda_g,lambda_b)
    print("hsv : ",hsv_r,hsv_g,hsv_b)
    rospy.set_param("/colorpal/r",hsv_r)
    rospy.set_param("/colorpal/g",hsv_g)
    rospy.set_param("/colorpal/b",hsv_b)


def endprogram():
    GPIO.cleanup()

if __name__=='__main__':
    
    setup()

    try:
        loop()

    except KeyboardInterrupt:
        endprogram()
