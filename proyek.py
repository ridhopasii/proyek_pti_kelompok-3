#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>


#define SS_PIN 10 
#define RST_PIN 9 
#define SERVO_PIN 2


MFRC522 mfrc522(SS_PIN, RST_PIN);
LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo myServo;

// UID CARD
const char* authorizedUIDs[] = {
  "85 3F D6 05",   
  "86 47 96 04"  
};
const int NUM_AUTH = sizeof(authorizedUIDs) / sizeof(authorizedUIDs[0]);


const int SERVO_OPEN = 90; 
const int SERVO_CLOSED = 0; 
const unsigned long OPEN_TIME = 3000;

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();


  lcd.init();   
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scan Kartu RFID");
  lcd.setCursor(0, 1);
  lcd.print("Menunggu...");

 
  myServo.attach(SERVO_PIN);
  myServo.write(SERVO_CLOSED);

  Serial.println("Sistem Siap - Tempelkan Kartu RFID");
}

void loop() {
  if (!mfrc522.PICC_IsNewCardPresent()) return;
  if (!mfrc522.PICC_ReadCardSerial()) return;


  String uidStr = uidToString(mfrc522.uid.uidByte, mfrc522.uid.size);
  Serial.print("UID Terdeteksi: ");
  Serial.println(uidStr);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("UID:");
  lcd.setCursor(0, 1);
  lcd.print(uidStr);

  // CEK KARTU
  if (isAuthorized(uidStr)) {
    Serial.println("Akses Diterima");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Akses Diterima");
    lcd.setCursor(0, 1);
    lcd.print("Selamat Datang");

    myServo.write(SERVO_OPEN);
    delay(OPEN_TIME);
    myServo.write(SERVO_CLOSED);

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Pintu Tertutup");
  } else {
    Serial.println("Akses Ditolak ");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Akses Ditolak!");
    lcd.setCursor(0, 1);
    lcd.print("Kartu Tidak Dikenal");
  }

  delay(1500);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Scan Kartu RFID");
  lcd.setCursor(0, 1);
  lcd.print("Menunggu...");
}

String uidToString(byte *buffer, byte bufferSize) {
  String uid = "";
  for (byte i = 0; i < bufferSize; i++) {
    if (buffer[i] < 0x10) uid += "0";
    uid += String(buffer[i], HEX);
    if (i < bufferSize - 1) uid += " ";
  }
  uid.toUpperCase();
  return uid;
}

bool isAuthorized(String uid) {
  uid.toUpperCase();
  for (int i = 0; i < NUM_AUTH; i++) {
    String auth = String(authorizedUIDs[i]);
    auth.toUpperCase();
    if (uid == auth) return true;
  }
  return false;
}
