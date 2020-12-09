int motorA1 = 3; // 왼쪽 바퀴 전진
int motorA2 = 6; // 왼쪽 바퀴 후진
int motorB1 = 9;  // 오른쪽 바퀴 전진
int motorB2 = 10; // 오른쪽 바퀴 후진

// initial command
int command = 0;

void setup()
{
  pinMode(motorA1, OUTPUT);
  pinMode(motorA2, OUTPUT);
  pinMode(motorB1, OUTPUT);
  pinMode(motorB2, OUTPUT);
  Serial.begin(115200);

  while (!Serial);

  Serial.println("OpenCV 3SU CAR");
}

void go()
{
  int max = 255;
  char output;
  if (Serial.available())
  {
    //int state = Serial.parseInt();
    int state = Serial.read();    
    switch (state) {
      case 1:
        analogWrite(motorA1, 150);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 200);
        analogWrite(motorB2, 0);
        // Serial.println("Forward");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 2:
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 150);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 200);
        // Serial.println("Reverse");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 3:
        analogWrite(motorA1, 150);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 150);
        // Serial.println("Strong Left");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 4:
        analogWrite(motorA1, 100);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        // Serial.println("Weak Left");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 5:
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 150);
        analogWrite(motorB1, 150);
        analogWrite(motorB2, 0);
        // Serial.println("Strong Right");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 6:
        digitalWrite(motorA1, 0);
        digitalWrite(motorA2, 0);
        digitalWrite(motorB1, 150);
        digitalWrite(motorB2, 0);
        // Serial.println("Weak Right");
        delay(800);
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        delay(400);
        break;
      case 7:
        digitalWrite(motorA1, 0);
        digitalWrite(motorA2, 0);
        digitalWrite(motorB1, 0);
        digitalWrite(motorB2, 0);
        // Serial.println("Stop");
        delay(800);
        break;

    }
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        Serial.write("test\n");      
  }
}
void loop() {
  go();
}
