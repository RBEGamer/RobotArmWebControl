#define STEPPER_1_EN_PIN 39
#define STEPPER_1_DIR_PIN 35
#define STEPPER_1_STEP_PIN 37
#define STEPPER_1_ID 1
#define STEPPER_1_JITTER_THREASHHOLD 1
#define STEPPER_1_INVERT_DIR true
#define STEPPER_1_SKIP_STEP  3
#define STEPPER_1_UPPER_LIMIT 0
#define STEPPER_1_LOWER_LIMIT 360

#include "stctl.h"


#include <Wire.h>
#define I2C_ADDR 8 //WHERE I CAN SEND TH_E I2COMMANDS TO SEE PYTHON SCRIPT


stctl stepper_1 = stctl(STEPPER_1_ID,STEPPER_1_STEP_PIN, STEPPER_1_DIR_PIN, STEPPER_1_EN_PIN, A0,STEPPER_1_JITTER_THREASHHOLD,STEPPER_1_INVERT_DIR,STEPPER_1_SKIP_STEP,STEPPER_1_UPPER_LIMIT,STEPPER_1_LOWER_LIMIT);


volatile int cmd_rec = false;
volatile int target_pos = 0;
volatile int stepper_id = 0;

const int CMDLEN = 4;
int i2ccmd[CMDLEN] = { 0,0,0,0 };
int cmd_counter = 0;
int cmd_read = 0;
void receiveEvent (int numBytes)
{
  cmd_counter = 0;
  while(Wire.available()<1){}   // warte auf  byte(s) im Buffer
  //Serial.print("byte count=");
  //  Serial.println(numBytes);
    
    while(Wire.available()) {
        i2ccmd[cmd_counter] = -1;
        cmd_read = Wire.read();
     //   Serial.println(cmd_read); //TODO REMOVE
        if(cmd_counter >= CMDLEN){
          }else{
            i2ccmd[cmd_counter] = cmd_read; 
            }
        cmd_counter++;
     }

     if(i2ccmd[0] == 0){
      for(int i = 0; i <1; i++){
          stepper_1.set_target_degree(i2ccmd[1],i2ccmd[2]);
        }
     }
}


const int STATELEN = 10;
int i2cstate[STATELEN] = { 0,0,0,0,0,0,0,0,0,0};
void requestEvent() {
  for(int i = 0; i<1;i++){
    i2cstate[i] = stepper_1.get_current_pos(false); // respond with message of 6 bytes
  }
  Serial.println("sEND");
  for(int i = 0; i<STATELEN;i++){
    Wire.write(i2cstate[i]); // respond with message of 6 bytes
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin(I2C_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent); // register event
  
}

void loop() {


      
      
    //UPDATE POSITIONS
  stepper_1.update_position();

  //DO STEPS
  for(int i = 0; i <1; i++){
    for(int j = 0; j <100; j++){
      stepper_1.do_step_phase_a();
      delayMicroseconds(550);
      stepper_1.do_step_phase_b();
      delayMicroseconds(550);  
    }
  }

  
}
