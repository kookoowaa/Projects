# 라즈베리파이4 with Raspbian 활용기
> - `Manjaro ARM xfce` 기반으로 활용하려 하였으나, 여러 이유로 라즈베리파이에 더 적합한 `Raspbian`을 활용하기로 함
> - https://www.raspberrypi.org/downloads/raspbian/ 에서 Kernel version 4.19 `Raspbian Buster` 다운받아서 환경 구축

## 1. `Raspbian` 설치

- 최신 버전의 Raspbian은 https://www.raspberrypi.org/downloads/raspbian/ 에서 다운로드 가능
- 다운받은 이미지와 SD카드로 Raspbian을 플래싱 하려면 별도의 프로그램이 요구되면 `Etcher`가 가장 무난했었음
- 플래싱 된 SD카드로 라즈비안을 부팅하면 기본 세팅을 위한 설정을 진행
- 유난히 주의할 점은 없으나, 개인적으로 locale은 영어로 하는 것이 자료를 찾아보기 용이했었음 (+ 부팅시 한글 폰트가 없어 깨져보이기도 함)

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
   - 개인적으로 `ibus` & `nabi` 입력기를 선호하여 둘의 조합으로 진행: `sudo apt install ibus ibus-hangul nabi`
   - 설치 후 [Preference] - [Input Method]에서 입력기를 `hangul`로 설정
   - 한글 출력을 위한 폰트도 별도로 설정 필요: `sudo apt install fonts-unfonts-core`
4. 기타 추가 설정 [Raspberry Pi Configuration]
   - `System` 탭에서 `Overscan`을 disable하여 화면 크기 맞추기 옵션을 해제
   - `Interfaces` 탭에서 필요한 포트를 개방: `SSH`, `VNC`, `Remote GPIO`, `Camera`
   - `Performance` 탭에서 `GPU Memory`를 256MB로 설정
5. 고정 IP 설정
   
   - 라즈베리파이를 일반 PC 사용하듯이 사용하는 것이 목적이라면, 공유기를 통해 동적으로(DHCP를 이용하여) IP 주소를 할당받아 사용하는 것이 별 문제가 되지 않음
   
   - 하지만 파일서버나 (NAS) DB 등으로 활용하기 위해서는 고정 IP를 사용하는 것이 편리함
   
   - 데비안에서 해당 설정은 `dhcpcd.conf`를 통해 수정 `sudo nano /etc/dhcpcd.conf`
   
   - 파일 끝에 다음 코드를 추가:
   
     ```
     interface wlan0
     static ip_address=192.168.0.80
     static routers=192.168.0.1
     static domain_name_servers=8.8.8.8
     ```
   
   - 재부 팅 후 `ifconfig`로 고정된 ip를 확인하면 `wlan0`의 `inet`이 `192.168.0.80`으로 설정된 것을 확인 할 수 있음
6. RPI(파이커널) 업데이트
   
   - 커널 업데이트는 `sudo rpi-update`로 수행
   
7. VNC 설정

   - 기본 설치되어 있는 RealVNC로 연결을 시도해 보았으나 (5번에서 설정한 고정IP로), 외부망에 속해 있는지 연결이 안됨
   - 윈도우 피씨는 유선으로 잡혀있고, 라즈베리파이는 무선으로 잡혀 있는데, 하나의 공유기에서 분리된 회선인지 확인 해 볼 필요가 있음
   - 아닐 시 네트워크 관련 지식이 필요할 것으로 보임

