#include "stctl.h"
#include "calibration.h" //RUN python ./calibration_data_copier.py first
#include <Wire.h>





#define I2C_ADDR 8 //WHERE I CAN SEND TH_E I2COMMANDS TO SEE PYTHON SCRIPT


stctl stepper_1 = stctl(STEPPER_1_ID,STEPPER_1_STEP_PIN, STEPPER_1_DIR_PIN, STEPPER_1_EN_PIN, A0,STEPPER_1_JITTER_THREASHHOLD,STEPPER_1_INVERT_DIR,STEPPER_1_SKIP_STEP,STEPPER_1_UPPER_LIMIT,STEPPER_1_LOWER_LIMIT);
stctl stepper_2 = stctl(STEPPER_2_ID, STEPPER_2_STEP_PIN, STEPPER_2_DIR_PIN, STEPPER_2_EN_PIN, A1, STEPPER_2_JITTER_THREASHHOLD, STEPPER_2_INVERT_DIR, STEPPER_2_SKIP_STEP, STEPPER_2_UPPER_LIMIT, STEPPER_2_LOWER_LIMIT);
stctl stepper_3 = stctl(STEPPER_3_ID, STEPPER_3_STEP_PIN, STEPPER_3_DIR_PIN, STEPPER_3_EN_PIN, A2, STEPPER_3_JITTER_THREASHHOLD, STEPPER_3_INVERT_DIR, STEPPER_3_SKIP_STEP, STEPPER_3_UPPER_LIMIT, STEPPER_3_LOWER_LIMIT);
stctl stepper_4 = stctl(STEPPER_4_ID, STEPPER_4_STEP_PIN, STEPPER_4_DIR_PIN, STEPPER_4_EN_PIN, A3, STEPPER_4_JITTER_THREASHHOLD, STEPPER_4_INVERT_DIR, STEPPER_4_SKIP_STEP, STEPPER_4_UPPER_LIMIT, STEPPER_4_LOWER_LIMIT);
stctl stepper_5 = stctl(STEPPER_5_ID, STEPPER_5_STEP_PIN, STEPPER_5_DIR_PIN, STEPPER_5_EN_PIN, A4, STEPPER_5_JITTER_THREASHHOLD, STEPPER_5_INVERT_DIR, STEPPER_5_SKIP_STEP, STEPPER_5_UPPER_LIMIT, STEPPER_5_LOWER_LIMIT);

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

     if(i2ccmd[0] == 0x00){
       stepper_1.set_target_degree(i2ccmd[1], i2ccmd[2]);
       stepper_2.set_target_degree(i2ccmd[1], i2ccmd[2]);
       stepper_3.set_target_degree(i2ccmd[1], i2ccmd[2]);
       stepper_4.set_target_degree(i2ccmd[1], i2ccmd[2]);
       stepper_5.set_target_degree(i2ccmd[1], i2ccmd[2]);
     }



     //if(i2ccmd[0] == 0x01){
    //   bool gripper_state = i2ccmd[1];// TODO
    // }
}


const int STATELEN = 15;
int i2cstate[STATELEN] = { 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
void requestEvent() {
  
    i2cstate[0] = stepper_1.get_current_pos(false); // respond with message of 6 bytes
    i2cstate[1] = stepper_2.get_current_pos(false);
    i2cstate[2] = stepper_3.get_current_pos(false);
    i2cstate[3] = stepper_4.get_current_pos(false);
    i2cstate[4] = stepper_5.get_current_pos(false);
/*
     i2cstate[5] = STEPPER_1_LOWER_LIMIT;
    i2cstate[6] = STEPPER_1_UPPER_LIMIT;

    i2cstate[7] = STEPPER_2_LOWER_LIMIT;
    i2cstate[8] = STEPPER_2_UPPER_LIMIT;

    i2cstate[9] = STEPPER_3_LOWER_LIMIT;
    i2cstate[10] = STEPPER_3_UPPER_LIMIT;

    i2cstate[11] = STEPPER_4_LOWER_LIMIT;
    i2cstate[12] = STEPPER_4_UPPER_LIMIT;

    i2cstate[13] = STEPPER_5_LOWER_LIMIT;
    i2cstate[14] = STEPPER_5_UPPER_LIMIT;
*/
     Serial.println("SEND");
    for (int i = 0; i < STATELEN; i++)
    {
      Wire.write(i2cstate[i]); // respond with message of 6 bytes
  }
}


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Wire.begin(I2C_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent); // register event

  stepper_1.set_target_degree(1, stepper_1.get_current_pos(true));
  stepper_2.set_target_degree(2, stepper_2.get_current_pos(true));
  stepper_3.set_target_degree(3, stepper_3.get_current_pos(true));
  stepper_4.set_target_degree(4, stepper_4.get_current_pos(true));
  stepper_5.set_target_degree(5, stepper_5.get_current_pos(true));
}

void loop() {


      
      
    //UPDATE POSITIONS
  stepper_1.update_position();
  stepper_2.update_position();
  stepper_3.update_position();
  stepper_4.update_position();
  stepper_5.update_position();

  for (int j = 0; j < 10; j++)
  {
    stepper_1.do_step_phase_a();
    stepper_2.do_step_phase_a();
    stepper_3.do_step_phase_a();
    stepper_4.do_step_phase_a();
    stepper_5.do_step_phase_a();
    delayMicroseconds(550);
    stepper_1.do_step_phase_b();
    stepper_2.do_step_phase_b();
    stepper_3.do_step_phase_b();
    stepper_4.do_step_phase_b();
    stepper_5.do_step_phase_b();
    delayMicroseconds(550);  
   }
  

  
}
