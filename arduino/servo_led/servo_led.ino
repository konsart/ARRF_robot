
#include <Servo.h>

#define SERVO_PIN 3
#define LED_PIN 4

Servo servo;
int cur_angle = 0;
String _sbuf = "";

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  servo.attach(SERVO_PIN);
}

void loop() {
  while (Serial.available() > 0) {
    int nl_ind = _sbuf.indexOf('\n');
    while (nl_ind != -1) {
      String msg = _sbuf.substring(0, nl_ind);
      _sbuf = _sbuf.substring(nl_ind+1);

      int sep_ind = msg.indexOf(':');

      if (sep_ind == -1) continue;

      String cmd = msg.substring(0, sep_ind);

      if (cmd == "set_angle") {
        cur_angle = msg.substring(sep_ind+1).toInt();
        cur_angle = constrain(cur_angle, 0, 180);
        
        digitalWrite(LED_PIN, HIGH);

        servo.write(cur_angle);
        Serial.write(String("current angle:").concat(String(cur_angle)));

        digitalWrite(LED_PIN, LOW);
      }
    }
  }
}
