#include "Arduino.h"
#include "ToggleSwitch.h"

ToggleSwitch :: ToggleSwitch(int in_pin){
    pin = in_pin;
    previous = LOW;     //previous reading from input
    time = 0;          // last time for successful toggle
    debounce = 200;     //minimum delay to debounce switch
    state = LOW;        //state for the circuit controlled by switch
                   
    pinMode(pin,INPUT);
     
}

int ToggleSwitch :: read_state(){
   current = digitalRead(pin);
   // toggle conditions
   if(current == HIGH && previous == LOW && millis() - time > debounce){
       if(state == HIGH)
         state = LOW;
        else
         state = HIGH;
        time = millis(); // get the current time
   }
   
   previous = current;
   return state;
 
} 
