/*
  The basic function of this sketch is to read
  inputs and broadcast them through the serial port.
  A python program will pick up the signal and use it
  to draw the input. 
*/
<<<<<<< HEAD

//import custom library for toggle switches
#include <ToggleSwitch.h>

int channel_1 = A0; // scope channels
int channel_2 = A1;

=======
#include <ToggleSwitch.h>

int channel_1 = A0; // scope channels
int channel_2 = A1;

>>>>>>> 329b24bcfdc4d5daaed762e1951f35ec82cb44c7
int vertical = 5; //sensitivity controls
int horizontal = 6;

//toggle switches
ToggleSwitch ch1_toggle(13);  //turns channel 1 on and off
ToggleSwitch ch2_toggle(12);  //turns channel 2 on and off
ToggleSwitch trigger(11);     //switches 'trigger' on and off
void setup(){
  pinMode(channel_1, INPUT);
  pinMode(channel_2, INPUT);
  pinMode(vertical, INPUT);
  pinMode(horizontal,INPUT);
  Serial.begin(9600);
}

void loop(){
  broadcast();
}

/*
  Reads from each defined pin and prints the result to
  serial.
*/
<<<<<<< HEAD
void broadcast(){
  //print state of all pins in one line separated by 
  //spaces
  
  Serial.print(analogRead(channel_1));
  Serial.print(" ");
  Serial.print(analogRead(channel_2));
  Serial.print(" ");
  Serial.print(analogRead(vertical));
  Serial.print(" ");
  Serial.print(analogRead(horizontal));
  Serial.print(" ");
  Serial.print(ch1_toggle.read_state());
  Serial.print(" ");
  Serial.print(ch2_toggle.read_state());
  Serial.print(" ");
  Serial.print(trigger.read_state());
  Serial.print("\n");
  
}
=======
/*
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
 
} */
>>>>>>> 329b24bcfdc4d5daaed762e1951f35ec82cb44c7
