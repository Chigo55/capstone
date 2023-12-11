#include <MsTimer2.h>
#include <Wire.h>

// 오른쪽 모터 핀
#define motorRightEnc 2
#define motorRightEnable 4
#define motorRightPwm 5
#define motorRightDir 8
// 오른쪽 모터 핀
#define motorLeftEnc 3
#define motorLeftEnable 7 
#define motorLeftPwm 6
#define motorLeftDir 9
// 모터 관련 변수
int enc_pulse_right = 0;
int enc_cnt_right = 0;
int enc_pulse_left = 0;
int enc_cnt_left = 0;

// pid제어기 변수
// 오른쪽용 PID제어기 제어 이득
double right_proportion = 0.2;
double right_integral = 0.3;
double right_derivative = 0.15;
// 오른쪽용 PID제어기 제어 이득
double left_proportion = 0.2;
double left_integral = 0.3;
double left_derivative = 0.15;

// PID 오차값 전역변수로 선언
// 오른쪽 모터용
float err_right_P = 0;
float err_right_I = 0;
float err_right_D = 0;
float err_right_B = 0;
// 왼쪽 모터용
float err_left_P = 0;
float err_left_I = 0;
float err_left_D = 0;
float err_left_B = 0;

// 기타 변수
int speed = 0;
int target_right = 0;
int target_left = 0;
int right_pid_val = 0;
int left_pid_val = 0;

char cmd;

// 외부 인터럽스 서비스 루틴
// 오른쪽 모터 인코더 펄스 카운트 함수
void motorRightEncoderPulseRead()
{
  enc_pulse_right++;
}
// 왼쪽 모터 인코더 펄스 카운트 함수
void motorLeftEncoderPulseRead()
{
  enc_pulse_left++;
}

// 펄스 초기화 함수
void encoderRightInitial()
{
  enc_cnt_right = enc_pulse_right;
  enc_pulse_right = 0;
}
void encoderLeftInitial()
{
  enc_cnt_left = enc_pulse_left;
  enc_pulse_left = 0;
}

// 스피드-목표값 함수
void speedToTargetR(int speed)
{
  target_right = speed;
}
void speedToTargetL(int speed)
{
  target_left = speed;
}

// PID 함수
void motorRightEncoderToPID()
{
  // PID 에러 계산
  err_right_P = enc_cnt_right - target_right;
  err_right_I += err_right_P;
  err_right_D = err_right_B - err_right_P;
  err_right_B = err_right_P;

  // PID 제어기
  right_pid_val = ((err_right_P * right_proportion) + (err_right_I * right_integral) + (err_right_D * right_derivative));

  // PID 제어기 한계값 지정
  // -255 ~ 255
  if (right_pid_val >= 255)
    right_pid_val = 255;
  if (right_pid_val <= -255)
    right_pid_val = -255;

  // PID값을 이용하여 모터 제어

  PIDToMotorR(right_pid_val);
}
void motorLeftEncoderToPID()
{
  // PID 에러 계산
  err_left_P = enc_cnt_left - target_left;
  err_left_I += err_left_P;
  err_left_D = err_left_B - err_left_P;
  err_left_B = err_left_P;

  // PID 제어기
  left_pid_val = ((err_left_P * left_proportion) + (err_left_I * left_integral) + (err_left_D * left_derivative));

  // PID 제어기 한계값 지정
  // -255 ~ 255
  if (left_pid_val >= 255)
    left_pid_val = 255;
  if (left_pid_val <= -255)
    left_pid_val = -255;

  // PID값을 이용하여 모터 제어

  PIDToMotorL(left_pid_val);
}

// 모터 제어 함수
void PIDToMotorR(int motor_right_speed)
{
  if (motor_right_speed < 0)
  {
    digitalWrite(motorRightEnable, LOW);
    analogWrite(motorRightPwm, abs(motor_right_speed));
  }
  else
  {
    digitalWrite(motorRightEnable, LOW);
    analogWrite(motorRightPwm, 0);
  }
}
void PIDToMotorL(int motor_left_speed)
{
  if (motor_left_speed < 0)
  {
    digitalWrite(motorLeftEnable, LOW);
    analogWrite(motorLeftPwm, abs(motor_left_speed));
  }
  else
  {
    digitalWrite(motorLeftEnable, HIGH);
    analogWrite(motorLeftPwm, 0);
  }
}

// 타이머 인터럽트 서비스 루틴 함수
void timerInterrupt()
{
  encoderRightInitial();
  encoderLeftInitial();
  motorRightEncoderToPID();
  motorLeftEncoderToPID();
}

// 전진
void forward()
{
  digitalWrite(motorRightDir, LOW);
  digitalWrite(motorLeftDir, LOW);
  speedToTargetR(speed);
  speedToTargetL(speed);
}
// 후진
void backward()
{
  digitalWrite(motorRightDir, HIGH);
  digitalWrite(motorLeftDir, HIGH);
  speedToTargetR(speed);
  speedToTargetL(speed);
}
// 좌회전
void turnLeft()
{
  digitalWrite(motorRightDir, LOW);
  digitalWrite(motorLeftDir, HIGH);
  speedToTargetR(speed);
  speedToTargetL(speed);
}
// 우회전
void turnRight()
{
  digitalWrite(motorRightDir, HIGH);
  digitalWrite(motorLeftDir, LOW);
  speedToTargetR(speed);
  speedToTargetL(speed);
}
// 정지
void stop()
{
  digitalWrite(motorRightDir, LOW);
  digitalWrite(motorLeftDir, LOW);
  speedToTargetR(0);
  speedToTargetL(0);
  PIDToMotorR(0);
  PIDToMotorL(0);
}

// 셋업
void setup()
{
  // 시리얼 115200
  Serial.begin(9600);

  // 외부 인터럽트 0, 1 설정
  // 라이징 엣지 마다 인터럽트 발생
  // 외부 인터럽트 서비스 루틴 실행 -> motorRightEncoderPulseRead/motorLeftEncoderPulseRead
  attachInterrupt(digitalPinToInterrupt(motorRightEnc), motorRightEncoderPulseRead, RISING);
  attachInterrupt(digitalPinToInterrupt(motorLeftEnc), motorLeftEncoderPulseRead, RISING);

  // 타이머 2 설정
  // 0.1초마다 타이머 인터럽트 발생
  // 타이머 인터럽트 서비스 루틴 실행 -> timerInterrupt
  MsTimer2::set(100, timerInterrupt);
  MsTimer2::start();

  // 핀모드 설정
  // R 모터 핀절성
  pinMode(motorRightPwm, OUTPUT);
  pinMode(motorRightEnable, OUTPUT);
  pinMode(motorRightDir, OUTPUT);
  pinMode(motorRightEnc, INPUT_PULLUP);
  // L 모터 핀절성
  pinMode(motorLeftPwm, OUTPUT);
  pinMode(motorLeftEnable, OUTPUT);
  pinMode(motorLeftDir, OUTPUT);
  pinMode(motorLeftEnc, INPUT_PULLUP);

  speed = 40;
}

// 루프
void loop()
{  
  if (Serial.available()) 
  {
    cmd = Serial.read();

    if (cmd == 'f') 
    {
      forward();
      delay(100);
    }
    else if (cmd == 'r') 
    {
      turnRight();
      delay(100);
    }
    else if (cmd == 'l') 
    {
      turnLeft();
      delay(100);
    }
    else if (cmd == 'b') 
    {
      backward();
      delay(100);
    }
    else if (cmd == 's') 
    {
      stop();
      delay(100);
    }
  }
}
