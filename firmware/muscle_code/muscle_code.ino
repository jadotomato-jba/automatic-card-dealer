#include "Arduino.h"
#include <Servo.h>
#include <AccelStepper.h>

// Servo stuff
#define SERVO_PIN 6
#define SERVO_UP_LIMIT 180
#define SERVO_DOWN_LIMIT 70
#define SERVO_START_ANGLE SERVO_UP_LIMIT
#define SERVO_END_ANGLE SERVO_DOWN_LIMIT
static Servo cardFlicker;

// Stepper things
#define DIR_PIN 3
#define STEP_PIN 4
#define STARTING_POSITION 0
#define MAX_STEP 1600
#define MAX_SPEED 2000
#define ACCELERATION 1500
AccelStepper dealerStepper(AccelStepper::DRIVER, STEP_PIN, DIR_PIN);

// Solid State Machine Things
#define DEALING 2
#define LISTENING 1
int state;
int players_to_deal;
int cards_to_deal;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  while (!Serial) { ; }

  cardFlicker.attach(SERVO_PIN);
  cardFlicker.write(SERVO_START_ANGLE);

  dealerStepper.setMaxSpeed(MAX_SPEED);
  dealerStepper.setAcceleration(ACCELERATION);
  dealerStepper.setCurrentPosition(STARTING_POSITION);

}

void loop() {
  // put your main code here, to run repeatedly:
  switch (state) {
    case LISTENING:
      if (Serial.available() > 0) {
        if (Serial.find("DEAL")) {
          state = DEALING;
        }
      }
      break;
    case DEALING: {
      players_to_deal = Serial.parseInt();
      cards_to_deal = Serial.parseInt();

      if (players_to_deal == 0 || cards_to_deal == 0) {
        state = LISTENING;
        break;
      }

      int result = deal_cards(players_to_deal,cards_to_deal);
      if (result) {
        Serial.println("STOPPED");
      } else {
        Serial.println("DEALT");
      }

      while (Serial.available() > 0) {Serial.read();}

      state = LISTENING;      
      break;
    }
    default:
      state = LISTENING;
      break;
  }
}

void flick_card() {
  cardFlicker.write(SERVO_END_ANGLE);
  delay(300);
  cardFlicker.write(SERVO_START_ANGLE);
  delay(300);
  return;
}

int deal_cards(int num_players, int num_cards) {
  int steps_between_players = MAX_STEP/num_players;
  int positions[12] = {0};
  for (int i = 1; i < num_players; i++) {
    positions[i] = positions[i-1] + steps_between_players;
  }
  for (int i = 0; i < num_cards; i++) {
    int result = deal_one_round(positions, num_players);
    if (result) {
      return result;
    }
    dealerStepper.moveTo(STARTING_POSITION);
    result = move_stepper();
    if (result) {
      return result;
    }
    dealerStepper.setCurrentPosition(STARTING_POSITION);
  }
  return 0;
}

int deal_one_round(int * positions, int num_players) {
  for(int player = 0; player < num_players; player++) {
    dealerStepper.moveTo(positions[player]);
    int result = move_stepper();
    if (result) {
      return result;
    }
    flick_card();
  }
  return 0;
}

int move_stepper() {
  static String incomingCommand = "";
  while (dealerStepper.distanceToGo() != 0) {
    dealerStepper.run();
    if (Serial.available() > 0) {
      char c = Serial.read();
      if (c == '\n' || c == '\r') {
        if (incomingCommand == "STOP") {
          incomingCommand = "";
          return 1;
        }
        incomingCommand = "";
      } else {
        incomingCommand += c;
      }
    }
  }
  return 0;
}