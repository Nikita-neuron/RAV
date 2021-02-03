 #include <Servo.h>

int right_motors_speed = 0;
int left_motors_speed = 0;

int motor_right_1_Pin = 8;
int motor_right_2_Pin = 7;
int motor_right_3_Pin = 6;

int motor_left_1_Pin = 5;
int motor_left_2_Pin = 4;
int motor_left_3_Pin = 3;

Servo motor_right_1;
Servo motor_right_2;
Servo motor_right_3;

Servo motor_left_1;
Servo motor_left_2;
Servo motor_left_3;

void setup() {
  pinMode(motor_right_1_Pin, OUTPUT);
  pinMode(motor_right_2_Pin, OUTPUT);
  pinMode(motor_right_3_Pin, OUTPUT);

  pinMode(motor_left_1_Pin, OUTPUT);
  pinMode(motor_left_2_Pin, OUTPUT);
  pinMode(motor_left_3_Pin, OUTPUT);
  
  motor_right_1.attach(motor_right_1_Pin);
  motor_right_2.attach(motor_right_2_Pin);
  motor_right_3.attach(motor_right_3_Pin);

  motor_left_1.attach(motor_left_1_Pin);
  motor_left_2.attach(motor_left_2_Pin);
  motor_left_3.attach(motor_left_3_Pin);
  
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == 'w') {
      right_motors_speed = 100;
      left_motors_speed = 100;
    }
    if (command == 's') {
      right_motors_speed = -100;
      left_motors_speed = -100;
    }
    if (command == 'a') {
      right_motors_speed = 100;
      left_motors_speed = -100;
    }
    if (command == 'd') {
      right_motors_speed = -100;
      left_motors_speed = 100;
    }
    if (command == 'f' or command == 't') {
      right_motors_speed = 0;
      left_motors_speed = 0;
    }
  }
  move_right_motors(right_motors_speed);
  move_left_motors(left_motors_speed);
  delay(1000);
  
//  int value = 100;
//  motor_right_1.write(map(value, -100, 100, 1000, 2000));
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
