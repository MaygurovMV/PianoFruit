/* что на что меняем. не занимает места.
    можно поменять
*/
//#define pin_1 1
//#define pin_2 2
//#define pin_3 3
//#define pin_4 4
//#define pin_5 5
//#define pin_6 6
//#define pin_7 7

int val;
bool isPress[7];

String outPackage;
char note[7] = {'C', 'D', 'E', 'F', 'G', 'A', 'B'};

int threshold = 1000;

void setup() {
  //открытие порта со скоростью 9600 бод
  Serial.begin(9600);
  while (Serial.available()>0){
    threshold = Serial.parseInt();
  }
  Serial.print("Init threshold "); Serial.println(threshold);

}

void loop() {
  for (int i=0; i<=6; i++){
    val = analogRead(i+1);
    if (val  < threshold) {
      if (!isPress[i]){
        outPackage += (String) note[i] + ":" + String(val) + ';' + ' ';
        isPress[i] = true;
      }
    } else {
      if (isPress[i]){
        outPackage += (String) '!' + note[i] + ':' + String(val) + ';' + ' ';
        isPress[i] = false;
      }
    }
  }
  if (outPackage != "") {
    Serial.println(outPackage);
  }
  outPackage = "";
  delay(100);

}
