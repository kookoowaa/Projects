## 설치 전 참조사항

- 남는 HDD, SSD를 활용할 수 있다면 best, 아니라면 파티션을 나눠서 듀얼부팅 가능
- 남는 HDD, SSD 설치 시 SATA 슬롯이 없다면 SATA-E 슬롯을 활용 가능 
- SATA-E 슬롯은 SATA 슬롯 2개+@로 구성되어 있으며, 일반 SATA 슬롯 2개로도 활용 가능

___

## 리눅스 선택

- 가장 많이 사용되는 리눅스는 Manjaro 라고 하지만, 한국에서 보편적이진 않음 (아치 리눅스 기반)
- *정정 - 알고 보니 2019년 12월 기준 MX Linux가 1위에 위치 - 데비안 기반의 가벼운 미들웨어 os*
- Manjaro 이후 많이 사용되는 리눅스는 Linux Mint로 Ubuntu 계열임 (우분투 기반, 데비안 기반은 LMDE)
- 공식적으로 지원되는 Ubuntu를 사용하는 것도 좋은 선택
- Manjaro에 도전 (Manjaro는 라즈베리파이 용 os도 지원, Rufus로 세팅이 되지 않아 Etcher 사용)
- **PACMAC**의 불편함으로 인해 Ubuntu 20.04 LTS로 전향

___

## 데스크톱 환경 선택

- 데스크탑도 종류가 많음
- 무게 순으로 KDE > GNOME > XFCE > LXDE > OPENBOX 등이 있다고 함
- XFCE로 설치

___
## Manjaro 설치 및 기본 세팅
- 리눅스, 특히 아치 리눅스의 경우 하나하나 다 찾아서 세팅해 주어야 하는 불편함이 있음

- 몇가지 주요 세팅에 대해 알아보자:

  > 1. `pacman` 업데이트
  > 2. 한글 입력기
  > 3. 그래픽 드라이버
  > 4. 구글 크롬
  > 5. 

### 1. `pacman` 업데이트
- `pacman`은 아치 리눅스의 패키지 관리자로 우분투의 `apt-get`과 유사한 역할을 함

> 리눅스/유닉스의 주요 패키지 관리자를 다시 한번 소개하면 다음과 같습니다.
>
> 데비안 : apt-get (Advanced Packaging Tool)
> 페도라(redhat 계열, CentOS) : yum, rpm
> 아치 리눅스 : pacman
> MAC OS : homebrew, MacPorts
>
> 출처: https://erider.co.kr/137 [시간을 달리는 e라이더 <전기 자전거 여행, IT 스토리>]

- 몇가지 중요한 명령어를 살펴보면:

  > - `sudo pacman -Syu` : 시스템의 모든 패키지를 업그레이드
  > - `sudo pacman -Ss[또는 Qs]` : 패키지를 검색 [설치가 되어있는 패키지 검색]
  > - `sudo pacman -S` : **패키지 설치**
  > - `sudo pacman -Rs` : 패키지 삭제

- manjaro 설치 후 세팅할 내용은 1) 서버 업데이트 변경, 2) `yay`, `debtap`설치

https://kkamagui.tistory.com/m/909 - NVIDIA

https://m.blog.naver.com/wdhyup/221683615856 - 한글입력기

http://ders45.blogspot.com/2017/03/manjaro-linux-17.html?m=1 - 기타 세팅 가이드

https://withjeon.com/2017/11/07/arch-linux-install-guide/#0403 - 세팅가이드

http://sun30812.blog.me/221431933809 - 세팅가이드 (KDE)

 https://palpit.tistory.com/765  - 듀얼부팅

 http://blog.naver.com/PostView.nhn?blogId=angelkim88&logNo=221702038231  - 듀얼부팅
