int motorA1 = 5;
int motorA2 = 6;
int motorB1 = 9;
int motorB2 = 10;

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
  char output;
  if (Serial.available())
  {
    //int state = Serial.parseInt();
    int state = Serial.read();    
    switch (state) {
      case 1:
        analogWrite(motorA1, 150);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 150);
        analogWrite(motorB2, 0);
        // Serial.println("Forward");
        delay(400);
        break;
      case 2:
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 100);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 100);
        // Serial.println("Reverse");
        delay(400);
        break;
      case 3:
        analogWrite(motorA1, 100);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 100);
        // Serial.println("Strong Left");
        delay(400);
        break;
      case 4:
        analogWrite(motorA1, 150);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);
        // Serial.println("Weak Left");
        delay(400);
        break;
      case 5:
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 150);
        analogWrite(motorB1, 150);
        analogWrite(motorB2, 0);
        // Serial.println("Strong Right");
        delay(400);
        break;
      case 6:
        digitalWrite(motorA1, 0);
        digitalWrite(motorA2, 0);
        digitalWrite(motorB1, 150);
        digitalWrite(motorB2, 0);
        // Serial.println("Weak Right");
        delay(400);
        break;
      case 7:
        digitalWrite(motorA1, 0);
        digitalWrite(motorA2, 0);
        digitalWrite(motorB1, 0);
        digitalWrite(motorB2, 0);
        // Serial.println("Stop");
        delay(400);
        break;
      default:
        analogWrite(motorA1, 0);
        analogWrite(motorA2, 0);
        analogWrite(motorB1, 0);
        analogWrite(motorB2, 0);   
        return;
    }
        Serial.write("test\n");      
  }
}
void loop() {
  go();
}