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
bool flag_threshold = true;

String outPackage;
char note[7] = {'C', 'D', 'E', 'F', 'G', 'A', 'B'};
String temp;
int threshold = 1000;

void setup() {
  //открытие порта со скоростью 9600 бод
  Serial.begin(9600);
  

}

void loop() {
  if (Serial.available()>0 && flag_threshold){
    temp = Serial.readString();
    threshold = temp.toInt();
//    Serial.print("Init threshold: ");
    Serial.println(threshold);
    flag_threshold = false;
  }
  
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
