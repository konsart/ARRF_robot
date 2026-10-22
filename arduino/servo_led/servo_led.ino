
#include <Servo.h>

#define SERVO_PIN 3
#define LED_PIN 4

Servo servo;
int current_angle = 0;
String _sbuf = "";

bool isNumeric(String str) {
  if (str.length() < 1) return false;

  for (int i = 0; i < str.length(); i++) {
    if (!isDigit(str.charAt(i))) return false;
  }
  return true;
}

void setup() {
  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  servo.attach(SERVO_PIN);
}

void loop() {
  while (Serial.available() > 0) {
    _sbuf += (char) Serial.read();
    int nl_ind = _sbuf.indexOf('\n');
    while (nl_ind != -1) {
      String msg = _sbuf.substring(0, nl_ind);
      _sbuf = _sbuf.substring(nl_ind+1);
      nl_ind = _sbuf.indexOf('\n');

      int sep_ind = msg.indexOf(':');

      if (sep_ind == -1) continue;
      if (msg.substring(0, sep_ind) != "set_angle") continue;
      
      String data = msg.substring(sep_ind+1);

      if (!isNumeric(data)) continue;

      int angle = constrain(data.toInt(), 0, 180);

      digitalWrite(LED_PIN, HIGH);
      servo.write(angle);
      
      current_angle = angle;

      Serial.print("current_angle:");
      Serial.println(current_angle);

      digitalWrite(LED_PIN, LOW);
    }
  }
}
