# 라즈베리파이4 활용기
> - 활용 가능한 os는 `Manjaro arm`과 `Raspbian` 2가지가 있는 것으로 확인 됨
> - `Manjaro ARM`은 설치까지는 문제가 없으나, 설치 이후 업데이트 오류가 반복
> - `Manjaro`의 `pacman`이 지원하는 롤링 릴리즈의 강점을 살려, 최대한 아치 리눅스 기반의 환경 구축을 우선시 함 (`Manjaro ARM xfce`)

## 1. `Manjaro ARM` 설치

- Manjaro 설치 자체는 크게 어려울 것이 없음
- https://manjaro.org/download/#arm 에서 KDE, XFCE, Minimal 버전으로 각각 다운로드 가능
- 다운받은 Manjaro는 `Etcher`를 활용하여 sd 카드에 준비하여 라즈베리 파이에 연결 (`Rufus`는 Arch계열 리눅스 설치 때 추가적인 설정이 필요하여 제외)
- 설치 자체는 UI를 따라 차례대로 진행하면 됨
- 설치 후 `sudo pacman -Syu`로 모든 패키지를 롤링 릴리즈 (업데이트)
- <del>현재 업데이트 후 `brcmfmac` 에러 반환 후 os 진입이 안되는 현상이 나타나 디버깅이 필요</del> 불안정한 네트워크로 인해 업데이트가 중단되면서 os 진입이 안되는 현상이 발생했었음

![](Manjaro_error.jpg)

- 작업환경이 윈도우 피씨 외 라즈베리파이를 활용할 예정이고, 물리적 자리 여건 상 [모니터2, 키보드1, 마우스1]을 공유할 방법을 찾던 중 `kvm 스위치`라는 입력기 선택 허브(?) 를 발견

- http://blog.naver.com/PostView.nhn?blogId=lecahel&logNo=221719483747 참조하여 초기 세팅 

  > 1. 설치 (locale은 ko-kr utf-8로)
  > 2. 한글 폰트 설치 `sudo pacman -S noto-fonts-cjk`
  > 3. 시스템 업그레이드 `sudo pacman -Syu`
  > 4. 한글 입력기 설치 (uim)
- https://sensebench.tistory.com/407
- http://www.dorajistyle.pe.kr/2014/04/manjaro-linux.html
## 2. Manjaro 대신 Raspbian 시도

- `Raspbian`은 우분투 계열 os로 라즈베리에 맞춰져 세팅해 놓았기 때문에 오류가 적을 것으로 예상
- https://rightway-park.tistory.com/3
- 설치 후 한글 세팅은 `sudo apt-get fonts-unfonts-core`로 설정 가능
- https://dgkim5360.tistory.com/entry/basic-setup-of-korean-environment-for-arch-linux
- https://blog.gaerae.com/2014/03/raspberrypi-archlinux-vim.html
