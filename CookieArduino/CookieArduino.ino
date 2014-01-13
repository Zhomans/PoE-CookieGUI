//Setup
#include <Servo.h> 
#include <AccelStepper.h>
 
Servo dispenserServo;
Servo cutterServo;

int dispenserPin = 9;
int cutterPin = 2;
int trayPinStep = 3;        
int trayPinDirection = 4;
int gantryPinStep = 5;
int gantryPinDirection = 6;

AccelStepper trayStepper(1,trayPinStep,trayPinDirection);
AccelStepper gantryStepper(1,gantryPinStep,gantryPinDirection);

int DispensingMode;
int traySize;
int trayPos;
int gantryPos;
int cookieSize;

int nextdigit;
int nextPos;
int i;

int dispenserAngle = 0;


void setup() {
  // Dispensing things
  dispenserServo.attach(dispenserPin);
  //cutServo.attach(cutterPin);
  dispenserServo.write(dispenserAngle);  
    
  // Positioning things
  trayStepper.setMaxSpeed(2000);            // speed in 1/8th steps/second by default (?)
  trayStepper.setAcceleration(1000);
  gantryStepper.setMaxSpeed(2000);
  gantryStepper.setAcceleration(1000);
  
  
  // Get initial user inputs (manual/automatic mode, tray size)
  Serial.begin(9600);
  establishConnection();
}

//Main loop. Changes depending on mode.
void loop() {
    if (DispensingMode == '1'){ //Manual Mode
    
      trayPos = getPositionInfo();      // get these number in steps. Our motors are 400 steps/revolution
      gantryPos = getPositionInfo();
      cookieSize = getSizeInfo();
      
      if (trayPos == 999) {
        dispenserServo.write(0);
        delay(20);
      }
      else{
      moveToPosition(trayPos,gantryPos); 
      dispenseCookiePiece(cookieSize);
      }
    }
    
    else{ //Automatic Mode
    /*
    if (automaticCounter >= (4)) { //Make sure that this number is consistent with Python.
      while (1==1) {
      delay(50); //Stops the servos and waits for user input.
        if (Serial.read()==71) {
          break; //Breaks out of loop if a "G" is detected.
        }
      }
      automaticCounter=0;
    }
    */
    
    //moveToPosition(x,y);
    //dispenseCookie(cookieSize);    
    //cutDough();
    }
}



void moveToPosition(int trayPos, int gantryPos){
    trayStepper.moveTo(trayPos);
    gantryStepper.moveTo(gantryPos);
    trayStepper.run();
    gantryStepper.run();
}

void dispenseCookiePiece(int cookieSize){
  dispenserAngle += 5*cookieSize;
  dispenserServo.write(dispenserAngle);
  delay(20);
}

// Gets cookie size (integer 1-9)
int getSizeInfo(){                      
  while(Serial.available()==0){
    delay(10);
  }
  cookieSize = Serial.read() - 48;
  Serial.println(cookieSize);
  return cookieSize;
}

// Gets next set of coordinates for putting cookie 
int getPositionInfo(){                      // known bug: this fails if you send something other than 3 digits to the serial port
  while(Serial.available()==0){
    delay(10);
    nextPos = 0;
  }
  for (i = 0; i<3; i++) {
    nextdigit = Serial.read();
    nextPos = nextPos*10 + (nextdigit - 48);
  }
  Serial.println(nextPos);
  return nextPos;
}

// Delays main loop until mode is confirmed.
void establishConnection() {
  while(Serial.available()==0){
    delay(10);
  }
  DispensingMode = Serial.read();
  Serial.println(DispensingMode);
}

