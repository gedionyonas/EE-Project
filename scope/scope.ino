/*
  The basic function of this sketch is to read
  inputs and broadcast them through the serial port.
  A python program will pick up the signal and use it
  to draw the input. 
*/

//import custom library for toggle switches
#include <ToggleSwitch.h>

int channel_1 = A0; // scope channels
int channel_2 = A1;

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
