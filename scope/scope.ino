
void setup(){
  
  Serial.begin(9600);
}

void loop(){
  
 
}

/*
  Defines push buttons and adds debounce functionality.
  Inspired by: http://www.arduino.cc/en/Tutorial/Switch#
*/

class ToggleSwitch{
  public:
    ToggleSwitch(int in_pin); //constructor
    int read_state();
  private:
    int pin;                //switch pin
    int previous = LOW;     //previous reading from input
    int current;            //current reading form input
    long time = 0;          // last time for successful toggle
    long debounce = 200;     //minimum delay to debounce switch
    int state = LOW;        //state for the circuit
                            //controled by this switch
};

ToggleSwitch :: ToggleSwitch(int in_pin){
    pin = in_pin;
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
