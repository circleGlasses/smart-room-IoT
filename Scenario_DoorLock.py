import paho.mqtt.client as paho # mqtt
import RPi.GPIO as GPIO
import time # sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

'''

Token Definition

    - Subscribe

    Sensor 1 - Door(Servo Motor) 
        Topic For Subscribe : '/rooms/202/door' - open the door

'''

# initialize variables for MQTT
Topic_For_Sub_Door ='/rooms/202/door'
broker = '163.152.223.99' # 사용하기 위해 인증서 Common Name 과 맞춰줘야 함 *중요
port = 8883 # SSL/TLS default version tlsv1.2

# initialize variables for Light Sensor
light_sensor = 4

# initialize variables Servo Motor
servo_motor = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_motor, GPIO.OUT)
lock_angle = 3.8
unlock_angle = 11.0

p = GPIO.PWM(servo_motor, 50)
p.start(7.5)
p.ChangeDutyCycle(lock_angle)
servo_motor_status = 1 # Door Status 1 = Unlocked, 0 = Locked



# Light Sensor
def rc_time(light_sensor):
    count = 0
    
    # Output on the pin for
    GPIO.setup(light_sensor, GPIO.OUT) # 4번 핀을 입력으로 설정
    GPIO.output(light_sensor, GPIO.LOW) # 4번 핀의 디지털 출력 설정
    
    time.sleep(0.1) # sleep 0.1 sec
    
    # 4번 핀을 input으로 변경
    GPIO.setup(light_sensor, GPIO.IN)
    
    # 4번 핀으로부터 읽은 값이 HIGH가 될 때까지 count 수행
    # 센서 주변이 어두울 수록 카운트 값이 크다.
    while (GPIO.input(light_sensor) == GPIO.LOW):
        count += 1
        
        if(count >250000):
            return count
        
    return count

# Servo Motor
def control_global_variables(value):
    global servo_motor_status
    servo_motor_status = value

# Servo Motor
def setAngle(angle):
    p.ChangeDutyCycle(angle)
    time.sleep(1)

# MQTT
def on_message(client, userdata, message):
    #message.topic = message.topic.decode("utf-8")
    #message.payload = message.payload.decode("utf-8")
    msg = str(message.topic)
    payload = str(message.payload)
    print(msg)
    print(payload)
 
    # Lock/Unlock the door by the value of user
    if(message.topic == Topic_For_Sub_Door):
        if(message.payload.decode("utf-8") == 'open'):
            print("Door Unlocked by MQTT")
            
            
            setAngle(unlock_angle)
            
            time.sleep(2)
            
            while True:
                print('test')
                if(rc_time(light_sensor) >= 250000):
                    setAngle(lock_angle)
                    break



# Establish connection with broker over SSL/TLS protocol
client = paho.Client()
client.tls_set("/home/pi/sw_contest/Scenario_DoorLock/ca_pl.crt", tls_version=2) # tls_version=2 is refered to tlsv1.2
client.tls_insecure_set(True) # Enable client to overlap its ip addr to connect to mqtt broker server
client.connect(broker, port) # Request connection to mqtt broker server over SSL/TLS
time.sleep(2)
client.loop_start() # Start looping for publishing / subscribing
client.on_message = on_message # Register callback method for subscription

# Register topic with .subscribe method
client.subscribe(Topic_For_Sub_Door)



# 스크립트가 인터럽트 될때 catch하고, 올바르게 cleanp
try:
    # 메인 루프
    while True:
        res = rc_time(light_sensor)
        print(str(res)) # 조도 센서의 값 출력
        
        #if(res < 1000000):
        #    print("Door Unlocked by Light Sensor")
        #    setAngle(unlock_angle)
        #else:
        #    print("Door Locked by Light Sensor")
        #    setAngle(lock_angle)
    
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup() # 사용했던 모든 포트에 대해서 정리