#include "stctl.h"
#include "Arduino.h"


stctl::stctl(int _id,int _step, int _dir, int _en, int _analog_in, int _enable_jitter, bool _invert, int _skip_clock, int _upper_limit,int _intlower_limit){
  step_pin = _step;
  dir_pin = _dir;
  en_pin = _en;
  poti_pin = _analog_in;
  enable_jitter = _enable_jitter;
  pinMode(_step, OUTPUT);
  pinMode(_dir, OUTPUT);
  pinMode(_en,OUTPUT);

 digitalWrite(_step, LOW);
 digitalWrite(_dir, LOW);
 digitalWrite(_en, HIGH);
invert_dir = _invert;
  curr_position = 0;

  STEPPER_MIN_POS = 0;
  STEPPER_MAX_POS = 1023;
  skip_clock = _skip_clock;
  skip_counter = 0;
  stepper_id = _id;

  do_move = false;

  upper_limit =_upper_limit;
  lower_limit = _intlower_limit;
}


void stctl::update_position(){
  delay(7);
  curr_position = analogRead(poti_pin);
  delay(7);
  //curr_position = map(curr_position,0,1024,0,360); //TODO CHANGE

  //CHECK IF A MOVEMENT IS REQUIRED
  if(abs((target_position-curr_position))> enable_jitter){
      digitalWrite(en_pin,LOW);
      do_move = true;
    }else{
      do_move = false;
      digitalWrite(en_pin,HIGH);
      digitalWrite(step_pin, LOW);
      digitalWrite(dir_pin, LOW);
    }

  //CHECK FOR DIRECTION -> SET PIN STATE 
 if(target_position > curr_position){
  if(invert_dir){
     digitalWrite(dir_pin, LOW);
    }else{
       digitalWrite(dir_pin, HIGH);
      }
     
    }else{
      if(invert_dir){
     digitalWrite(dir_pin, HIGH);
    }else{
       digitalWrite(dir_pin, LOW);
      }
    }


  }

 int stctl::get_current_pos(bool with_update){
  if(with_update){
    stctl::update_position();
    }
    return map(curr_position, 0, 1024, 0, 255);
    ;
  }

  void stctl::do_step_phase_a(){
    if(do_move ){//&& skip_counter >= skip_clock-1){
      digitalWrite(step_pin, LOW);
    }
    
  }

  void stctl::do_step_phase_b(){
    if(do_move){
      digitalWrite(step_pin, HIGH);
    }
   // skip_counter++;
   // if(skip_counter >= skip_clock){
   //   skip_counter = 0;
   //   }
  }

  
 void stctl::set_target_degree(int _id, int _target){
 if(_id == stepper_id){

   if (_target > upper_limit)
   {
     _target = upper_limit;
   }

    if (_target > 255)
   {
     _target = 255;
   }


   
  

    if (_target < lower_limit)
    {
      _target = lower_limit;
    }

    if (_target < 0)
    {
      _target = 0;
    }

    target_position = map(_target, 0, 255, 0, 1024);
    // skip_counter = 0;
  }
 }
