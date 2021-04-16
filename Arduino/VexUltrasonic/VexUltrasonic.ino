#include <NewPing.h>
#include <Servo.h>

// up left
#define TRIGGER_PIN_1  2 // input
#define ECHO_PIN_1     3 // output

// up right
#define TRIGGER_PIN_2  4 // input
#define ECHO_PIN_2     5 // output

// down
#define TRIGGER_PIN_3  6 // input
#define ECHO_PIN_3     7 // output

// left
#define TRIGGER_PIN_4  8 // input
#define ECHO_PIN_4     9 // output

// right
#define TRIGGER_PIN_5  10 // input
#define ECHO_PIN_5     11 // output

#define MAX_DISTANCE 400
 
NewPing sonarUpLeft(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE); // up left
NewPing sonarUpRight(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE); // up right
NewPing sonarDown(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE); // down
NewPing sonarLeft(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE); // left
NewPing sonarRight(TRIGGER_PIN_5, ECHO_PIN_5, MAX_DISTANCE); // right

typedef struct
{
    int16_t upLeft;
    int16_t upRight;
    int16_t down;
    int16_t left;
    int16_t right;
} __attribute__((__packed__)) ultrasonic_Data;

ultrasonic_Data ultrasonicData;
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  ultrasonicData.upLeft = sonarUpLeft.ping_cm();
  ultrasonicData.upRight = sonarUpRight.ping_cm();
  ultrasonicData.down = sonarDown.ping_cm();
  ultrasonicData.left = sonarLeft.ping_cm();
  ultrasonicData.right = sonarRight.ping_cm();

//  ultrasonicData.upLeft = 1;
//  ultrasonicData.upRight = 2;
//  ultrasonicData.down = 3;
//  ultrasonicData.left = 4;
//  ultrasonicData.right = 5;

  Serial.write((byte*)( &ultrasonicData), sizeof ultrasonicData);
}
