smart-room-IoT
====================================

Kakao Chatbot 연동 투숙객 편의/보안 제공 스마트객실 IoT 플랫폼 IoT
IoT(Internet of Things) of smart room IoT platform for guest convenience and security interlocking with Kakao Chatbot
<br><br><br>



프로젝트 설명 (Project Description)
====================================

- 객실에 IoT 센서 구성 및 객실 관리자 웹 페이지 제작
- 체크 인 시 온라인 키 발급 (인원 수 제한 X) => Kakao Chatbot 이용
- 객실 무단 침입 발생 시 투숙객에게 즉시 문자 알림 및 실시간 CCTV 모니터링 지원
- 특정 시간 동안 객실 내 투숙객 미감지시 자동 전력 차단
- IoT 서버 불법 접근 방지 위해 MQTT 통신 시 SSL/TLS 보안 프로토콜 적용
<br>
- Each room is comprised of IoT sensors and admin web page for room manager.<br>
- Online keys are issued when guests check in (no limit on the number of keys) => use Kakao Chatbot.<br>
- Guests are notified by sms message and provided with real-time monitoring CCTV when a trespass occurs.<br>
- Power interruption occurs after certain seconds if there was no human detect in room.<br>
- SSL/TLS security protocol during MQTT communications for the prevention of illegal accesses.<br>
<br><br><br>


프로젝트 구성 (Project Composition)
====================================

- smart-room-IoT
- MQTT Broker Server (Mosquitto SSL/TLS)
- [smart-room-WAS] (https://github.com/circleGlasses/smart-room-WAS) (Web Application Server codes) 
<br><br><br>


IoT 구성 (IoT Composition)
====================================

- MQTT Broker Server(Eclipse Mosquitto)
- Raspberry Pi 1(Indoor Human Detection)
  - Infrared PIR Motion Sensor(HC-SR501)
  - Piezo Speaker PC Mount 12mm
  - RGB 10mm LED
  - 3mm LED
- Raspberry Pi 2(Remote Control Door Lock)
  - Servo Motor sg90
  - Photoresistor(or light-dependent resistor)
- Raspberry Pi 3(CCTV)
  - Raspberry Pi Camera Module 5MP
<br><br><br>


IoT 개발 환경 (IoT Development Environment)
====================================

###### MQTT Broker Server
 - Windows 7 Pro, 64-bit
 - Mosquitto Eclipse v1.5.1
 - MQTT Protocol Version v3.1.1
 - OpenSSL v1.1
###### Hardware(Raspberry Pi)
 - Raspbian, NOOBS v2.8.2
 - Paho.mqtt lib, v1.4.0
<br><br><br>

설치 (Install)
====================================
###### MQTT Broker Server
 1. Eclipse Mosquitto 설치
 2. OpenSSL 설치 및 SSL/TLS 통신을 위한 클라이언트와 서버의 디지털 인증서 생성(http://www.steves-internet-guide.com/mosquitto-tls/)
  
###### Hardware
 1. Rasbian OS 설치
 2. Paho-mqtt 라이브러리 설치
 3. Clone Repository
 4. 하드웨어(Raspberry Pi)에 센서 연결
<br>

###### MQTT Broker Server
 1. Install Eclipse Mosquitto
 2. Install OpenSSL and create client and server-side digital certificates for SSL/TLS communications(http://www.steves-internet-guide.com/mosquitto-tls/)
  
###### Hardware
 1. Install Rasbian OS
 2. Install Paho-mqtt library
 3. Clone Repository
 4. Connect sensors to Hardware(Raspberry Pi)
 <br><br><br>
