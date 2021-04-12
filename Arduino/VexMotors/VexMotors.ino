#include <Servo.h>
#include <Wire.h>
#include <I2CEncoder.h>

int right_motors_speed = 0;
int left_motors_speed = 0;

int motors_platform_speed = 0;

int motor_right_1_Pin = 7;
int motor_right_2_Pin = 6;
int motor_right_3_Pin = 5;

int motor_left_1_Pin = 4;
int motor_left_2_Pin = 3;
int motor_left_3_Pin = 2;

Servo motor_right_1;
Servo motor_right_2;
Servo motor_right_3;

Servo motor_left_1;
Servo motor_left_2;
Servo motor_left_3;

int right_motors_platform_speed = 0;
int left_motors_platform_speed = 0;

int motor_right_platform_1_Pin = 13;
int motor_right_platform_2_Pin = 12;
int motor_right_platform_3_Pin = 11;

int motor_left_platform_1_Pin = 10;
int motor_left_platform_2_Pin = 9;
int motor_left_platform_3_Pin = 8;

Servo motor_right_platform_1;
Servo motor_right_platform_2;
Servo motor_right_platform_3;

Servo motor_left_platform_1;
Servo motor_left_platform_2;
Servo motor_left_platform_3;

Servo motor_up;
Servo motor_down;

I2CEncoder leftEncoder;
I2CEncoder rightEncoder;

int motor_up_Pin = 8;
int motor_down_Pin = 7;

typedef struct
{
    int8_t r;
    int8_t l;
    int8_t p;
    int16_t u;
    int16_t d;
} __attribute__((__packed__)) myS;

myS s;

void setup() {
  pinMode(motor_right_1_Pin, OUTPUT);
  pinMode(motor_right_2_Pin, OUTPUT);
  pinMode(motor_right_3_Pin, OUTPUT);

  pinMode(motor_left_1_Pin, OUTPUT);
  pinMode(motor_left_2_Pin, OUTPUT);
  pinMode(motor_left_3_Pin, OUTPUT);

  pinMode(motor_right_platform_1_Pin, OUTPUT);
  pinMode(motor_right_platform_2_Pin, OUTPUT);
  pinMode(motor_right_platform_3_Pin, OUTPUT);

  pinMode(motor_left_platform_1_Pin, OUTPUT);
  pinMode(motor_left_platform_2_Pin, OUTPUT);
  pinMode(motor_left_platform_3_Pin, OUTPUT);
  
  motor_right_1.attach(motor_right_1_Pin);
  motor_right_2.attach(motor_right_2_Pin);
  motor_right_3.attach(motor_right_3_Pin);

  motor_left_1.attach(motor_left_1_Pin);
  motor_left_2.attach(motor_left_2_Pin);
  motor_left_3.attach(motor_left_3_Pin);

  motor_right_platform_1.attach(motor_right_platform_1_Pin);
  motor_right_platform_2.attach(motor_right_platform_2_Pin);
  motor_right_platform_3.attach(motor_right_platform_3_Pin);

  motor_left_platform_1.attach(motor_left_platform_1_Pin);
  motor_left_platform_2.attach(motor_left_platform_2_Pin);
  motor_left_platform_3.attach(motor_left_platform_3_Pin);

  motor_up.attach(motor_up_Pin);
  motor_down.attach(motor_down_Pin);
  
  Serial.begin(9600);
}

//void loop() {
//  if (Serial.available() > 0) {
////    myS s;
////    Serial.readBytes((byte*)(&s), sizeof(s));
//    char command = Serial.read();
//    Serial.println("ABC");
//  }
//}

int16_t up_motor_needed = 0;
int16_t down_motor_needed = 0;

void loop() {
  if (Serial.available() > 0) {
//    char command = Serial.read();
      
      Serial.readBytes((byte*)(&s), sizeof(myS));    

      right_motors_speed = s.r;
      left_motors_speed = s.l;

      motors_platform_speed = s.p;

      up_motor_needed = s.u;
      down_motor_needed = s.d;
  }
  move_right_motors(right_motors_speed);
  move_left_motors(left_motors_speed);
  move_motors_platform(motors_platform_speed);
  move_camera_motors(100*(up_motor_now < up_motor_needed), 
//  myS ass {0x12, 0x34};
//  Serial.write((byte*)( &s), sizeof s);
//  uint16_t loh = 0x1234;
//  Serial.write((byte*)&loh, sizeof loh);

//  Serial.print(String(s.r));
//  Serial.print(String(s.l));
  
//  delay(1000);
}

void move_right_motors(int angle) {
//  Serial.println(angle);
  motor_right_1.write(map(angle, -100, 100, 1000, 2000));
  motor_right_2.write(map(angle, -100, 100, 1000, 2000));
  motor_right_3.write(map(angle, -100, 100, 1000, 2000));
}

void move_left_motors(int angle) {
  motor_left_1.write(map(angle, -100, 100, 1000, 2000));
  motor_left_2.write(map(angle, -100, 100, 1000, 2000));
  motor_left_3.write(map(angle, -100, 100, 1000, 2000));
}

void move_motors_platform(int angle) {
  motor_right_platform_1.write(map(angle, -100, 100, 1000, 2000));
  motor_right_platform_2.write(map(angle, -100, 100, 1000, 2000));
  motor_right_platform_3.write(map(angle, -100, 100, 1000, 2000));
  
  motor_left_platform_1.write(map(angle, -100, 100, 1000, 2000));
  motor_left_platform_2.write(map(angle, -100, 100, 1000, 2000));
  motor_left_platform_3.write(map(angle, -100, 100, 1000, 2000));
}

void move_camera_motors(int angleUp, int angleDown) {
  analogWrite(3, map(angleUp, -100, 100, 0, 250));
  analogWrite(2, map(angleDown, -100, 100, 0, 250));
}
