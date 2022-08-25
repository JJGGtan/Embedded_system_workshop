// Assign each LED to the connected digital I/O port
int led1 = 13; 
int led2 = 12;
int led3 = 11;
int led4 = 10;
int led5 = 9; 

void setup() {
  Serial.begin(9600);
  // Define the digital ports' mode
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  pinMode(led3, OUTPUT);
  pinMode(led4, OUTPUT);
  pinMode(led5, OUTPUT);

  // Initially set all port to start the program with low signal
  digitalWrite(led1, LOW);
  digitalWrite(led2, LOW);
  digitalWrite(led3, LOW);
  digitalWrite(led4, LOW);
  digitalWrite(led5, LOW);
}

// start on/off loop pattern
void loop() {
  digitalWrite(led1, HIGH); // Turn on the first LED
  delay(1000); // Wait for 1000 milliseconds (1 second) 
  digitalWrite(led1, LOW); // Turn off the first LED

  digitalWrite(led2, HIGH); // Turn on the second LED
  delay(1000); // Wait for 1000 milliseconds (1 second) 
  digitalWrite(led2, LOW); // Turn off the second LED

  digitalWrite(led3, HIGH); // Turn on the third LED
  delay(1000); // Wait for 1000 milliseconds (1 second) 
  digitalWrite(led3, LOW); // Turn off the third LED

  digitalWrite(led4, HIGH); // Turn on the fourth LED
  delay(1000); // Wait for 1000 milliseconds (1 second) 
  digitalWrite(led4, LOW); // Turn off fourth first LED

  digitalWrite(led5, HIGH); // Turn on the fifth LED
  delay(1000); // Wait for 1000 milliseconds (1 second) 
  digitalWrite(led5, LOW); // Turn off the fifth LED
}
