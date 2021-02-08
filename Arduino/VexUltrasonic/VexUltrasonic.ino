#include <NewPing.h>

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

#define TRIGGER_PIN_6  12
#define ECHO_PIN_6     13

#define MAX_DISTANCE 400
 
NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE);
NewPing sonar3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE);
NewPing sonar4(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE);
NewPing sonar5(TRIGGER_PIN_5, ECHO_PIN_5, MAX_DISTANCE);
NewPing sonar6(TRIGGER_PIN_6, ECHO_PIN_6, MAX_DISTANCE);

typedef struct
{
    int8_t dis1;
    int8_t dis2;
    int8_t dis3;
    int8_t dis4;
    int8_t dis5;
    int8_t dis6;
} __attribute__((__packed__)) ultrasonic_Data;

ultrasonic_Data ultrasonicData;
 
void setup() {
  Serial.begin(9600);
}
 
void loop() {
  delay(50);
  ultrasonicData.dis1 = sonar1.ping_cm();
  ultrasonicData.dis2 = sonar2.ping_cm();
  ultrasonicData.dis3 = sonar3.ping_cm();
  ultrasonicData.dis4 = sonar4.ping_cm();
  ultrasonicData.dis5 = sonar5.ping_cm();
  ultrasonicData.dis6 = sonar6.ping_cm();

  Serial.write((byte*)( &ultrasonicData), sizeof ultrasonicData);

  delay(100);
}
