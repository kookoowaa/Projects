# 라즈베리파이4 with Raspbian 활용기
> - `Manjaro ARM xfce` 기반으로 활용하려 하였으나, 여러 이유로 라즈베리파이에 더 적합한 `Raspbian`을 활용하기로 함
> - https://www.raspberrypi.org/downloads/raspbian/ 에서 Kernel version 4.19 `Raspbian Buster` 다운받아서 환경 구축

## 1. `Raspbian` 설치

- 

## 2. Raspbian 환경 설정

> - 다음 5단계에 걸쳐 리눅스 환경 설정
>
> - 와이파이 연결, 패키지 업데이트, 한글 설정, 기타 추가 설정, 고정 IP 설정,  RPI(파이커널) 업데이트

1. 와이파이 연결
   - Wifi 공유기가 5g 지원 시, `wifi-country`를 한국으로 놓고 연결; 아닐 경우 GB로 설정하여야 wifi가 검색됨
   - [Preference] - [Raspberry Pi Configuration] - [Localisation] - [Set WiFi Country] 에서 `wifi-country` 설정 가능
2. 패키지 업데이트
   - 운영체제는 `apt-get`을 사용하기 때문에 다음 명령어로 버전 업데이트 실행 `sudo apt-get update`
   - 업데이트는 저장소 내 패키지 인덱스를 업데이트
   - 업데이트 된 인덱스로 업그레이드는 `sudo apt-get upgrade`로 실행
   - 단, 요새 추세는 `apt-get` 보다는 `apt(Advanced Package Tool)`을 사용한다고 함
3. 한글 설정
   - 리눅스에서는 기본적으로 한글 입력기를 지원하지 않으므로, 별도의 설치를 통해야만 한글 입력이 가능함
   - 입력기 또한 종류가 여러가지이고 (`ibus`, `nabi`, `fcitx` 등) 개인과 잘 맞는 입력기를 선택하면 됨
   - 개인적으로 `nabi` 입력기를 선호하여 `nabi`로 진행
   - 
4. 기타 추가 설정
5. 고정 IP 설정
6. RPI(파이커널) 업데이트

