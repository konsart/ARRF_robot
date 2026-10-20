
#include <Servo.h>

#define SERVO_PIN 3
#define LED_PIN 4

Servo servo;
int tmp_angle = 0, cur_angle = 0;

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  servo.attach(SERVO_PIN);
}

void loop() {
  while (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    int sep_ind = msg.indexOf(':');

    if (sep_ind == -1) continue;

    String cmd = msg.substring(0, sep_ind);

    if (cmd == "set_angle") {
      cur_angle = msg.substring(sep_ind+1).toInt();
      cur_angle = constrain(cur_angle, 0, 180);
      
      digitalWrite(LED_PIN, cur_angle - tmp_angle > 0);

      servo.write(cur_angle);

      tmp_angle = cur_angle;
    }
  }
}
