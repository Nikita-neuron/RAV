#include <Servo.h>
#include <Wire.h>
#include <I2CEncoder.h>
#include <math.h>

int pwm_convert(int speed) {
  return map(speed, -100, 100, 1000, 2000);
}

class CameraMotor {
public:
  I2CEncoder encoder;
  Servo motor;
  int speed;
  float needed;
  float min_angle;
  float max_angle;
  int move_direction;
public:
  CameraMotor(float min_angle = -INFINITY, float max_angle = INFINITY) {
//    this->speed = speed;
    this->min_angle = min_angle;
    this->max_angle = max_angle;
  }
  void attach(int pin) {
    motor.attach(pin);
    motor.write(0);
    encoder.init(MOTOR_269_ROTATIONS, MOTOR_269_TIME_DELTA);
  }
  void set_needed(float needed) {
//    this->needed = constrain(needed, min_angle, max_angle);
    if (needed > max_angle) {
      needed = max_angle;
    } else if (needed < min_angle) {
      needed = min_angle;
    }
    this->needed = needed;
//    this->needed = needed;
    float now = encoder.getPosition();
    int delta = sign(needed - now);
//    Serial.print("NEEDED ");
//    Serial.print(needed);
//    Serial.print(' ');
//    Serial.print(now);
//    Serial.print(' ');
//    Serial.println(delta);
    
    move_direction = delta;
  }
  void set_speed(int8_t speed) {
    this->speed = speed;
  }
  void update() {
    if (min_angle <= needed && needed <= max_angle) {
      motor.write(pwm_convert(speed));
    } else {
      motor.write(pwm_convert(0));
    }
//    if (move_direction) {
//      float now = encoder.getPosition();
//      
//      int delta = sign(needed - now);
//      
////      Serial.print("MOVE ");
////      Serial.print(needed - now);
////      Serial.print(' ');
////      Serial.println(delta);
//      this.write(speed*delta);
////      motor.write(1700);
//      if (delta != move_direction) {
//        // Serial.println("GAVDUINO");
//        needed = 0;
//        move_direction = 0;
//      }
//    } else {
//      // Serial.println("DONE");
//      motor.write(0);
//    }
  }
};

int right_motors_speed = 0;
int left_motors_speed = 0;

int motors_platform_speed = 0;

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

CameraMotor motor_camera_up;
CameraMotor motor_camera_right(-45/360.0, 45/360.0);

typedef struct
{
    int8_t r;
    int8_t l;
    int8_t p;
    int8_t lr;
    int8_t ud;
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

  Serial.begin(9600);
}


float right_motor_needed = 0;
float up_motor_needed = 0;

float max_right_motor_angle = 80;
float max_up_motor_angle = 80;

bool first_loop = true;

void loop() {
  if (Serial.available() > 0) {
      Serial.readBytes((byte*)(&s), sizeof(myS));
//    s.r = Serial.parseInt();
//    s.l = Serial.parseInt();
//    s.p = Serial.parseInt();
//    s.u = Serial.parseInt();
//    s.d = Serial.parseInt();
//    Serial.read();
//    Serial.print("DONE ");
//    Serial.print(s.r);
//    Serial.print(' ');
//    Serial.print(s.l);
//    Serial.print(' ');
//    Serial.print(s.p);
//    Serial.print(' ');
//    Serial.print(s.u);
//    Serial.print(' ');
//    Serial.println(s.d);
    
    
    right_motors_speed = s.r;
    left_motors_speed = s.l;

    motors_platform_speed = s.p;

//    up_motor_needed = s.u;
//    right_motor_needed = s.d;
    
//    right_motor_needed /= 360;
//    up_motor_needed /= 360;
    
//    motor_camera_up.set_needed(up_motor_needed);
//    motor_camera_right.set_needed(right_motor_needed);
    motor_camera_up.set_speed(s.ud);
    motor_camera_right.set_speed(s.lr);
  }
  motor_camera_up.update();
  motor_camera_right.update();
  
  
//  return

//  if (up_motor_needed > max_up_motor_angle) {
//    up_motor_needed = max_up_motor_angle;
//  }
//  if (up_motor_needed < max_up_motor_angle*-1) {
//    up_motor_needed = max_up_motor_angle*-1;
//  }
//  if (right_motor_needed > max_right_motor_angle) {
//    right_motor_needed = max_right_motor_angle;
//  }
//  if (right_motor_needed < max_right_motor_angle*-1) {
//    right_motor_needed = max_right_motor_angle*-1;
//  }


  
//  move_camera_motors(right_motor_needed, up_motor_needed);

  move_platform(motors_platform_speed);
  move_tracks(left_motors_speed, right_motors_speed);
  
}



void move_platform(int speed) {
  motor_platform.write(pwm_convert(speed));
}

void move_tracks(int left, int right) {  
  motor_left.write(pwm_convert(left));
  motor_right.write(pwm_convert(right));
}

void move_camera_motors(int right, int up) {
  motor_camera_right.set_needed(right);
  motor_camera_up.set_needed(up);
}
