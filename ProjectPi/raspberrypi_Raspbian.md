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
   - 확인 결과 데스크탑은 인터넷 회선에서 바로 유선으로 연결 (공유기 거치지 않음), 무선 인터넷은 공유기를 거치기 때문에 외부 IP주소가 다름
   - 공유기에서 포트포워딩을 설정하여 **<외부IP>:포트**를 통해 VNC 접속 필요
   - 일반적으로 192.168.0.1로 접속하면 iptime, tplink 등 공유기 설정 가능하고, 포트포워딩 설정도 여기에서 가능
   - 포트포워딩 항목에 들어가서 서비스포트와 내부포트(default:5900)를 설정해 주고, IP 주소는 위에서 설정한 고정 IP 주소를 기입하여 설정 완료 (https://soulslip.tistory.com/99)

8. SSH 연결
   - putty 설치 후 VNC 처럼 **<외부IP>:포트**를 통해 접속을 사도하면 "Fatal error: remote side unexpectedly closed network connection"와 함께 실패를 맛보게 됨
   - SSH는 VNC와 다른 내부포트(default:22)를 사용하기 때문에, 위와 같이 네트워크 장비에서 포트포워딩을 추가로 설정해 주어야 함
   - 설정 후 putty를 통해 접속 시도하면 아이디(default:pi)와 비밀번호(default:raspberry)를 입력하고 터미널 접속이 가능함
   
9. `docker/container` 구축
   - `docker/container`라는 개념 자체가 간단히 집고 넘어갈 개념은 아니지만, 사용자 입장에서 쉽게 설명하자면 컴퓨터를 영역 별로 분리하여 활용하기 위한 방법임
   - 기존에는 가상화라는 방법도 많이 사용하였지만 가상화를 대체하는 훨씬 가벼운 방식 (https://www.slideshare.net/pyrasis/docker-fordummies-44424016)
   - 다음 명령어로 리눅스 배포판 종류를 자동으로 인식, 이후 도커를 설치 가능
   ```shell
   $ sudo wget -qO- https://get.docker.com/ | sh
   ```
   - 112pg
