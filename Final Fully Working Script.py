# Smart Dispenser
 #by Daniel Lawton
 #17th/05/2022
 
# All refrences found in file in repository
 
*/
#import libraries
import BlynkLib                                           
import RPi.GPIO as GPIO  #choose module                                 
import time
import signal
import atexit

#User authentication connect to Blynk account
BLYNK_AUTH = "17McbeumaK2cn8OB5oacJXpYqMUwSt_J"

#shutdown handler
atexit.register(GPIO.cleanup)            

//defines sensor and servo pins on Raspberry Pi
sensorpin = 23                           
servopin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin, GPIO.OUT, initial=False)
GPIO.setup(sensorpin,GPIO.IN)
# add rising edge detection on sensorpin
GPIO.add_event_detect(sensorpin, GPIO.RISING)

//servopin = 17   frequency = 50Hz
p = GPIO.PWM(servopin, 50) 

p.start(0)
time.sleep(2)

#Intialiise Blynlk
blynk = BlynkLib.Blynk(BLYNK_AUTH)       

#A basic method which prints and turns the servo motor when motion is detected
def MOTION():
    p.ChangeDutyCycle(10)
    time.sleep(1.2)
    p.ChangeDutyCycle(5)
    time.sleep(1)
    p.ChangeDutyCycle(7.5)
    time.sleep(1.2)
    print( "Motion Detected!" )
    blynk.virtual_write(2, GPIO.input(sensorpin))

#A try if statement only true when motion is detected not utitlised
def move_sensor():

       try:
             while True:
                         
                          MOTION()
                          time.sleep(0.2)
        
      

#register handler for virtual pin V4 write event
@blynk.on("V4")
def v4_write_handler(value):
    buttonValue=value[0]
    print(f'Current button value: {buttonValue}')
    
    #Shares Data with V2 virtual pin (LED)
    
    blynk.virtual_write(2, buttonValue)
    
    #Configures Servo movements
    p.ChangeDutyCycles(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(0)
    time.sleep(0.2)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(0)
    time.sleep(0.2)
    p.ChangeDutyCycle(5)
    time.sleep(0.5)
    p.ChangeDutyCycle(0)
    time.sleep(0.2)

#A try if statement only true when motion is detected
try:
    while True:
        if GPIO.event_detected(sensorpin):
          MOTION()
          time.sleep(0.2)
          
        # infinite loop that waits for event
        blynk.run()
        pass

except KeyboardInterrupt:
        print ("Quit")
        GPIO.cleanup()
        exit()
