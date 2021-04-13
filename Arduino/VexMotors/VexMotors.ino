#include <Servo.h>
#include <Wire.h>
#include <I2CEncoder.h>

int right_motors_speed = 0;
int left_motors_speed = 0;

int motor_platform_speed = 0;

enum PINS {
  PIN_MOTOR_PLATFORM = 2,
  PIN_MOTOR_LEFT = 4,
  PIN_MOTOR_RIGHT = 3,
  PIN_MOTOR_CAMERA_UP = 5,
  PIN_MOTOR_CAMERA_RIGHT = 6,
};


Servo motor_platform;
Servo motor_left;
Servo motor_right;

Servo motor_camera_up;
Servo motor_camera_right;

I2CEncoder encoder_up;
I2CEncoder encoder_right;

typedef struct
{
    int8_t r;
    int8_t l;
    int8_t p;
    int16_t u;
    int16_t d;
} __attribute__((__packed__)) myS;

myS s;


int sign(float n) {
  return (n > 0) - (n < 0);
}

void setup() {
  Wire.begin();

  pinMode(PIN_MOTOR_PLATFORM, OUTPUT);
  pinMode(PIN_MOTOR_LEFT, OUTPUT);
  pinMode(PIN_MOTOR_RIGHT, OUTPUT);
  pinMode(PIN_MOTOR_CAMERA_UP, OUTPUT);
  pinMode(PIN_MOTOR_CAMERA_RIGHT, OUTPUT);
  
  motor_platform.attach(PIN_MOTOR_PLATFORM);
  motor_left.attach(PIN_MOTOR_LEFT);
  motor_right.attach(PIN_MOTOR_RIGHT);
  motor_camera_up.attach(PIN_MOTOR_CAMERA_UP);
  motor_camera_right.attach(PIN_MOTOR_CAMERA_RIGHT);

  encoder_up.init(MOTOR_269_ROTATIONS, MOTOR_269_TIME_DELTA);
  encoder_right.init(MOTOR_269_ROTATIONS, MOTOR_269_TIME_DELTA);
  
  Serial.begin(9600);
}


float right_motor_needed = 0.1;
float up_motor_needed = 0;
int move_direction_right = 1;
int move_direction_up = 0;

float max_right_motor_angle = 120;
float max_up_motor_angle = 120;


void loop() {
//  if (Serial.available() > 0) {
////    char command = Serial.read();
//      
//      Serial.readBytes((byte*)(&s), sizeof(myS));    
//
//      right_motors_speed = s.r;
//      left_motors_speed = s.l;
//
//      motors_platform_speed = s.p;
//
//      up_motor_needed = s.u;
//      right_motor_needed = s.d;
//      done_moving_motors = true;
//  }

//  move_right_motors(right_motors_speed);
//  move_left_motors(left_motors_speed);
//  move_motors_platform(motors_platform_speed);
//  move_camera_motors(25, 25);

//  move_platform(30);
//  move_tracks(30, 30);
//  move_camera(0, 0);

  
  if (move_direction_right) {
    float right_motor_now = encoder_right.getPosition();
    float up_motor_now = encoder_up.getPosition();

    

    int right_dir = sign(right_motor_needed - right_motor_now);
    int up_dir = sign(up_motor_needed - up_motor_now);
    
    Serial.print("MOVE ");
    Serial.print(right_motor_needed - right_motor_now);
    Serial.print(' ');
    Serial.println(up_motor_needed - up_motor_now);
    Serial.print(' ');
    Serial.println(right_dir);
    move_camera(25*right_dir, 25*up_dir);
    if (right_dir != move_direction_right) {
      Serial.println("GAVDUINO");
      right_motor_needed *= -1;
      move_direction_right *= -1;
    }
  } else {
    Serial.println("DONE");
    move_camera(0, 0);
  }
  
//  myS ass {0x12, 0x34};
//  Serial.write((byte*)( &s), sizeof s);
//  uint16_t loh = 0x1234;
//  Serial.write((byte*)&loh, sizeof loh);

//  Serial.print(String(s.r));
//  Serial.print(String(s.l));
  
//  delay(1000);
}

int pwm_convert(int speed) {
  return map(speed, -100, 100, 1000, 2000);
}

void move_platform(int speed) {
  motor_platform.write(pwm_convert(speed));
}

void move_tracks(int left, int right) {
  motor_left.write(pwm_convert(left));
  motor_right.write(pwm_convert(right));
}

void move_camera(int right, int up) {
  motor_camera_up.write(pwm_convert(up));
  motor_camera_right.write(pwm_convert(right));
}
