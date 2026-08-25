# Automated Robotic Card Dealer
## Description
Simple robotic card dealer built off of a Raspberry Pi Zero 2 W and Arduino Nano. To deal cards, the stepper motor spins to move to different players, and a servo is used to flick a card from the bottom of the deck. Users select the number of cards and number of players on a display on the Pi.

## System Architecture
**Two Controllers:** Both a Raspberry Pi and Arduino Nano are used to divide labor between the two controllers. The Raspberry Pi handles higher level operations, including recieving user input and updating the live display. The Nano controls the actual movement of the two motors precisely and accurately.\
\
**Power Distribution:** All components are powered by a set of two battery backs in series that each hold 4 AA batteries for a total of 12V. One rail of the breadboard is used to supply 12V to the stepper motor, and a second rail supplies 5V to the Pi and Servo. A buck converter is used to step down from 12V to 5V. Finally, the Nano recieves power from the Pi via a Micro USB to USB-C data cable.\
\
**Communication Protocol:** Data is exchanged between the two controllers using UART protocol over the data cable. Each controller recieves confirmation that data was correctly recieved, and then that information is displayed on the Pi for the user to see.

## Tech Stack and Hardware Components
**Electronics**
+ Rasberry Pi Zero 2 W
+ Waveshare 1.44inch LCD HAT
+ Arduino Nano
+ LM2596 Step Down Module
+ Adafruit TMC2209 Stepper Motor Driver

**Motors**
+ NEMA 14 Bipolar Stepper Motor
+ SG90 Microservo

## Setup Guide
### Microcontroller Firmware
### Single-board Computer Software
### Service/Daemon Configuration

## Engineering Challenges

## Future Implementations
+ Custom PCB to upgrade from the breadboard
+ 3D printed housing to encase the entire device
+ Rechargeable batteries
+ Custom-built ejector arm for servo 