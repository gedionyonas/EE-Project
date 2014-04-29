/*
  Defines toggle switch object with debounce functionality.
  Inspired by: http://www.arduino.cc/en/Tutorial/Switch#
*/

#ifndef ToggleSwitch_h
#define ToggleSwitch_h

#include "Arduino.h"

class ToggleSwitch{
  public:
    ToggleSwitch(int in_pin); //constructor
    int read_state();
  private:
    int pin;                //switch pin
    int previous;     //previous reading from input
    int current;            //current reading form input
    long time;          // last time for successful toggle
    long debounce;     //minimum delay to debounce switch
    int state ;        //state for the circuit controled by this switch
                           
};

#endif

