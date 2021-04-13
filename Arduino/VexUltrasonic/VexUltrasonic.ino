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
#define ECHO_PIN_4     9

// right
#define TRIGGER_PIN_5  10 // input
#define ECHO_PIN_5     11 // output

#define MAX_DISTANCE 400
 
NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE); // up left
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE); // up right
NewPing sonar3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE); // down
NewPing sonar4(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE); // left
NewPing sonar5(TRIGGER_PIN_5, ECHO_PIN_5, MAX_DISTANCE); // right

typedef struct
{
    int16_t dis1;
    int16_t dis2;
    int16_t dis3;
    int16_t dis4;
    int16_t dis5;
} __attribute__((__packed__)) ultrasonic_Data;

ultrasonic_Data ultrasonicData;
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  ultrasonicData.dis1 = sonar1.ping_cm();
  ultrasonicData.dis2 = sonar2.ping_cm();
  ultrasonicData.dis3 = sonar3.ping_cm();
  ultrasonicData.dis4 = sonar4.ping_cm();
  ultrasonicData.dis5 = sonar5.ping_cm();

  Serial.write((byte*)( &ultrasonicData), sizeof ultrasonicData);
}
