import RPi.GPIO as GPIO
import paho.mqtt.client as paho # mqtt
import threading
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

'''

Token Definition

    - Publish

        Description : Sending human detection state to Node Red Server through MQTT Broker Server
        Topic For Publish : '/rooms/202/humanDetect'
        # 0 : Not detect , 1 : Detect
        
        Description : If rule violation ocurred then send this state to Node Red Server through MQTT Broker Server
        Topic For Publish : '/rooms/202/ruleViolation'
        # 0 : Intrusion, 1 : Unoccupied
            
    - Subscribe
        Description : Getting room state from Node Red Server through MQTT Broker Server
        Topic For Subscribe : '/rooms/202/roomState'
        # 0 : Available, 1 : Occupied, 2 : Unoccupied
'''
# initialize global variables to decide whether Intrusion is occured
roomState= 0 # 0 : Available, 1 : Occupied, 2 : Unoccupied
humanState = 0 # 0 : Not detect , 1 : Detect

# initialize variables for MQTT
Topic_For_Pub_ruleViolation = '/rooms/202/ruleViolation'
Topic_For_Pub_humanDetect = '/rooms/202/humanDetect'
Topic_For_Sub_roomState = '/rooms/202/roomState'
broker = '163.152.223.99' # 사용하기 위해 인증서 Common Name 과 맞춰줘야 함 *중요
port = 8883 # SSL/TLS default version tlsv1.2

# initialize variables for HumanDectection Sensor HC-SR501
humanDetection_sensor = 23
GPIO.setup(humanDetection_sensor, GPIO.IN)

# initialize RGB LED
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, 1)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, 1)

# initialize Single Color LED, variables for Timer Function
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, False)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, False)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, False)
GPIO.setup(19, GPIO.OUT)
GPIO.output(19, False)

time_count = 0
reset_ctl = 0 # 0 : Led On, 1 : Led Off

# initialize variables for Piezo Sensor
piezo_sensor = 25
GPIO.setup(piezo_sensor, GPIO.OUT)
p = GPIO.PWM(piezo_sensor, 100)

c4 = 262
d4 = 294
e4 = 330
f4 = 349
g4 = 392
a4 = 440
b4 = 494
c5 = 523.25

speed = 0.25



def start_timer(count):
    global time_count
    
    if(reset_ctl == 1):
        change_global_variables_reset_ctl(0)
        time_count = 0
    
    time_count += 1
    print('time_count : ' + str(time_count))
    timer=threading.Timer(1, start_timer, args=[count])
    timer.start()
    
    if time_count==15: # 15 sec
        print('Indoor light Off')
        client.publish(Topic_For_Pub_ruleViolation, 1)
        time_count = 0
        timer.cancel()

def change_global_variables_reset_ctl(value):
    global reset_ctl
    reset_ctl = value

def change_global_variables_roomState(value):
    global roomState
    roomState = value

def on_message(client, userdata, message):
    #message.topic = message.topic.decode("utf-8")
    #message.payload = message.payload.decode("utf-8")
    msg = str(message.topic)
    payload = str(message.payload)
    print(msg)
    print(payload)
 
    # Set temperature or humidity to the value of user
    if(message.topic == Topic_For_Sub_roomState):
        if(message.payload.decode("utf-8") == '0' or message.payload.decode("utf-8") == '1' or message.payload.decode("utf-8") == '2'):
            change_global_variables_roomState(int(message.payload))

            if(str(roomState) == '1'): # If guest is at hotel then turn on indoor light
                start_timer(0) # 0 : no action, 1 : reset
                GPIO.setup(5, GPIO.OUT)
                GPIO.output(5, True)
                GPIO.setup(6, GPIO.OUT)
                GPIO.output(6, True)
                GPIO.setup(13, GPIO.OUT)
                GPIO.output(13, True)
                GPIO.setup(19, GPIO.OUT)
                GPIO.output(19, True)
                
            else: # If guest is outside of hotel or no guest in hotel then turn off indoor light
                GPIO.setup(5, GPIO.OUT)
                GPIO.output(5, False)
                GPIO.setup(6, GPIO.OUT)
                GPIO.output(6, False)
                GPIO.setup(13, GPIO.OUT)
                GPIO.output(13, False)
                GPIO.setup(19, GPIO.OUT)
                GPIO.output(19, False)
            
            
            
# Establish connection with broker over SSL/TLS protocol
client = paho.Client()
client.tls_set("/home/pi/sw_contest/Scenario_MotionDetection/ca_pl.crt", tls_version=2) # tls_version=2 is refered to tlsv1.2
client.tls_insecure_set(True) # Enable client to overlap its ip addr to connect to mqtt broker server
client.connect(broker, port) # Request connection to mqtt broker server over SSL/TLS
time.sleep(2)
client.loop_start() # Start looping for publishing / subscribing
client.on_message = on_message # Register callback method for subscription

# Register topic with .subscribe method
client.subscribe(Topic_For_Sub_roomState)

print("Waiting for sensor to settle")
time.sleep(2)
print("Detecting motion")

try:
    while True:
        humanState = GPIO.input(humanDetection_sensor)
        print('Human Detection State : ' + str(humanState))
        if(humanState):
            
            client.publish(Topic_For_Pub_humanDetect, 1) # if human detected then send detection state '1' to server
            time.sleep(2)
            
            if(str(roomState) == '1'): # If anything not detected on Motion Sensor within 15 sec, roomState changed 1(Occupied) to 2(Unoccupied)
                print('Start timer')
                #start_timer(0) # 0 : no action, 1 : reset
                change_global_variables_reset_ctl(1)
            
                print("Motion Detected")
               
                # Turn on RGB Led
                GPIO.output(17, True)
                GPIO.output(27, False)
                GPIO.output(22, True)
                
                time.sleep(2)
                
                # Turn off RGB LED
                GPIO.output(17, 1)
                GPIO.output(27, 1)
                GPIO.output(22, 1)
                
            elif(str(roomState) == '2'):
                print("Intrusion occured!!!")
            
                # Turn on RGB Led
                GPIO.output(17, True)
                GPIO.output(27, True)
                GPIO.output(22, False)
                
                 # Turn on Piezo sensor
                GPIO.output(piezo_sensor, True) 
                p.start(10)
                for i in range(5):
                    p.ChangeFrequency(c4)
                    time.sleep(speed)
                    p.ChangeFrequency(b4)
                    time.sleep(speed)
                
                # Turn off RGB LED
                GPIO.output(17, 1)
                GPIO.output(27, 1)
                GPIO.output(22, 1)
                
                # Turn off Peizo Sensor
                GPIO.output(piezo_sensor, False)
                p.stop()
                
                
                client.publish(Topic_For_Pub_ruleViolation, 0)
                
        else:
            client.publish(Topic_For_Pub_humanDetect, 0) # if human not detected then send detection state '0' to server
            
        time.sleep(2)
except:
    print("Interrupt Occured")
    GPIO.cleanup()