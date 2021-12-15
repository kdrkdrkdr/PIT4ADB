# PIT4ADB

Papago Image Translation for Android Debug Bridge
파파고 이미지 번역을 ADB 로 컴퓨터에서 구현


# 초기설정 (처음에 한 번만)

1. 녹스(2021/11/25 배포한 7.0.1.9 버전)을 설치합니다.
2. nox_adb.exe 가 있는 폴더를 환경변수에 추가합니다.
3. 디폴트로 깔려있는 Android 7(32bit)를 실행시킵니다.
4. 태블릿 화면 크기를 스마트폰 화면 크기로 설정합니다.
5. initialize.bat 을 실행시킵니다. (파파고, ATX 설치)
6. 파파고 들어가서 팝업창이 뜨면 미리 동의 버튼을 눌러줍니다.
    - 미리 동의 버튼 안 눌러놓으면 프로그램이 작동하지 않을 수도 있습니다.


# 사용법 
PIT4ADB.exe 를 실행시키고, 번역하고 싶은 사진(jpg, png)이 있는 폴더를 선택합니다.

그리고 하단의 번역하기 버튼을 누릅니다.

그럼 번역이 시작됩니다. (이때 휴대폰의 잠금이 풀린 상태로 켜져있어야합니다.)

중간에 중지하려면 번역중지 버튼을 누릅니다.

하단에 언어 설정을 반드시 하시기 바랍니다.

번역된 파일은 선택한 폴더 내에 PAPAGO_TRANSLATED 폴더에 저장됩니다. (로그 창에도 뜸)