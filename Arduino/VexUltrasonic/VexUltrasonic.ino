#include <NewPing.h>
#include <Servo.h>

#define TRIGGER_PIN_1  2
#define ECHO_PIN_1     3

#define TRIGGER_PIN_2  4
#define ECHO_PIN_2     5

#define TRIGGER_PIN_3  6
#define ECHO_PIN_3     7

#define TRIGGER_PIN_4  8
#define ECHO_PIN_4     9

#define TRIGGER_PIN_5  10
#define ECHO_PIN_5     11

#define MAX_DISTANCE 400

int up_motors_speed = 0;
int down_motors_speed = 0;

int motor_up_Pin = 8;
int motor_down_Pin = 7;

Servo motor_up;
Servo motor_down;
 
NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE);
NewPing sonar3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE);
NewPing sonar4(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE);
NewPing sonar5(TRIGGER_PIN_5, ECHO_PIN_5, MAX_DISTANCE);

typedef struct
{
    int16_t dis1;
    int16_t dis2;
    int16_t dis3;
    int16_t dis4;
    int16_t dis5;
} __attribute__((__packed__)) ultrasonic_Data;

ultrasonic_Data ultrasonicData;

typedef struct
{
    int8_t u;
    int8_t d;
} __attribute__((__packed__)) myS;

myS s;
 
void setup() {
  pinMode(motor_up_Pin, OUTPUT);
  pinMode(motor_down_Pin, OUTPUT);

  motor_up.attach(motor_up_Pin);
  motor_down.attach(motor_down_Pin);
  
  Serial.begin(9600);
}
 
void loop() {
  if (Serial.available() > 0) {
      
      Serial.readBytes((byte*)(&s), sizeof(myS));    

      up_motors_speed = s.u;
      down_motors_speed = s.d;
  }
  move_camera_motors(up_motors_speed, down_motors_speed);
  
  ultrasonicData.dis1 = sonar1.ping_cm();
  ultrasonicData.dis2 = sonar2.ping_cm();
  ultrasonicData.dis3 = sonar3.ping_cm();
  ultrasonicData.dis4 = sonar4.ping_cm();
  ultrasonicData.dis5 = sonar5.ping_cm();

  Serial.write((byte*)( &ultrasonicData), sizeof ultrasonicData);

//  delay(100);
}

void move_camera_motors(int angleUp, int angleDown) {
  motor_up.write(map(angleUp, -100, 100, 1000, 2000));
  motor_down.write(map(angleDown, -100, 100, 1000, 2000));
}
