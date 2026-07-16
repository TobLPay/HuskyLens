#include "HUSKYLENS.h"
#include "SoftwareSerial.h"

HUSKYLENS huskylens;
int avail = false;

int red = 6;
int green = 5;
int blue = 4;

int inputPin = 7;
int pirState = LOW;
int val = 0;


void setup() {
    Serial.begin(115200);

    pinMode(red, OUTPUT);
    pinMode(green, OUTPUT);
    pinMode(blue, OUTPUT);
    pinMode(inputPin,INPUT);

    digitalWrite(red, LOW);
    digitalWrite(green, LOW);
    digitalWrite(blue, LOW);

    Wire.begin();
    while (!huskylens.begin(Wire))
    {
        Serial.println(F("실패!"));
        delay(100);
    }
}

void loop() {
  val=digitalRead(inputPin);
  

  if (!huskylens.request()) {
    Serial.println("요청 실패!");
    delay(1000);
    return;
  }

  avail=huskylens.available();
  HUSKYLENSResult result = huskylens.read();
  if (avail) {
    if(result.ID == 0){
      digitalWrite(green, LOW);
      digitalWrite(red, HIGH);
      digitalWrite(blue, LOW); 
    }
    else{
      digitalWrite(green, HIGH);
      digitalWrite(red, LOW);
      digitalWrite(blue, LOW); 
      Serial.print("ID = ");
      Serial.println(result.ID);
    }
  }
  else{ 
    digitalWrite(blue, HIGH);
    digitalWrite(green, LOW);
    digitalWrite(red, LOW);
  }
  delay(1000);
}
