#ifndef STCTL_H
#define STCTL_H
class stctl{

  private:

  int curr_position;
  int target_position;

  int min_analog_pos;
  int max_analog_pos;

  int degree_offset;

  int enable_jitter;
 
  int target_reached;

  int step_pin;
  int dir_pin;
  int en_pin;

  int poti_pin;

  int stepper_id;
  bool invert_dir;
  bool do_move;

  int skip_clock;
  int skip_counter  = 0;

  int lower_limit;
  int upper_limit;
  public:
  stctl(int _id,int _step, int _dir, int _en, int _analog_in, int _enable_jitter, bool _invert,int _skip_clock, int _upper_limit,int _intlower_limit);
  

  void stctl_tick(); //wenn schritte gemacht werden müssen hier den treiber toggeln


  void set_step(bool _state);
  void set_dir(bool _state);
  void set_en(bool _state);

  void update_position();//reads analog input and map it to degrees and desieds for dir/enable target_reached

  void set_target_degree(int _id, int _target); //
  
  int STEPPER_MIN_POS;
  int STEPPER_MAX_POS;

  void do_step_phase_a();
  void do_step_phase_b();
  int get_current_pos(bool with_update);
  };
  #endif
