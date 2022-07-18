/*
DIY Color Sensor
Michael D'Argenio
mjdargen@gmail.com

Description: Arduino-based proof of concept for a simple, DIY color sensor using an RGB LED.
*/

// data structure for storing colors
struct rgbColor {
  int r;
  int g;
  int b;
};

// define pin numbers
#define LED_R A0
#define LED_G A1
#define LED_B A2
#define BUTTON 2
#define HB_LED 3
#define BUZZER 4
#define DEBOUNCE 50

int buttonState;  // the current reading from the input pin
int lastButtonState = HIGH;  // the previous reading from the input pin
unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled

// put your setup code here, to run once:
void setup() {
  // setup serial port
  Serial.begin(9600);
  // wait for serial port to be ready
  while(!Serial);
  // configure pins
  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(HB_LED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
}

// put your main code here, to run repeatedly:
void loop() {
  // wait for debounced button press
  if (debounce_button_press(BUTTON)) {
    // turn on light source for reading
    digitalWrite(HB_LED, HIGH);
    // perform countdown
    countdown();
    // take readings
    rgbColor reading = rgb_sampling();
    // turn off light source
    digitalWrite(HB_LED, LOW);
    // print results
    print_results(reading);
  }
}


// debounces button set up with a pullup resistor
bool debounce_button_press(int pin) {

  // read the state of the switch into a local variable:
  int reading = digitalRead(BUTTON);

  // check to see if you just pressed the button
  // (i.e. the input went from LOW to HIGH), and you've waited long enough
  // since the last press to ignore any noise:

  // If the switch changed, due to noise or pressing:
  if (reading != lastButtonState) {
    // reset the debouncing timer
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE) {
    // whatever the reading is at, it's been there for longer than the debounce
    // delay, so take it as the actual current state:

    // if the button state has changed:
    if (reading != buttonState) {
      buttonState = reading;
      // for input with pullup resistor, LOW = pressed
      if (!buttonState) {
        lastButtonState = reading;
        return true;
      }
    }
  }
  lastButtonState = reading;
  return false;
}


// provides a countdown letting the user know when the
void countdown() {
  Serial.print("3");
  digitalWrite(BUZZER, HIGH);
  delay(500);
  digitalWrite(BUZZER, LOW);
  delay(500);
  Serial.print(" 2");
  digitalWrite(BUZZER, HIGH);
  delay(500);
  digitalWrite(BUZZER, LOW);
  delay(500);
  Serial.print(" 1");
  digitalWrite(BUZZER, HIGH);
  delay(500);
  digitalWrite(BUZZER, LOW);
  delay(500);
  Serial.println(" GO!");
}

// take 10 samples of the color readings and average them together
rgbColor rgb_sampling() {
  rgbColor detected;
  int r, g, b = 0;
  digitalWrite(BUZZER, HIGH); // turn on buzzer

  // take 10 readings and find the mean
  for (int i=0; i<10; i++) {
    detected.r += analogRead(LED_R);
    detected.g += analogRead(LED_G);
    detected.b += analogRead(LED_B);
    delay(100);
  }
  detected.r /= 10;
  detected.g /= 10;
  detected.b /= 10;

  digitalWrite(BUZZER, LOW); // turn off buzzer
  return detected;
}

// prints results
void print_results(rgbColor reading) {
  Serial.print("R: ");
  Serial.print(reading.r);
  Serial.print(", G: ");
  Serial.print(reading.g);
  Serial.print(", B: ");
  Serial.println(reading.b);
}
