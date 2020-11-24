# share-places-naver2kakao-selenium

## 네이버맵 -> 카카오맵 즐겨찾기 폴더 공유하기

<p align="center"><img width="80%" src="img/map.png" /></p>

네이버 길찾기앱의 즐겨찾기 표시한 장소들을 카카오맵으로 옮기고 싶은데 그런 기능이 없어 불편해서 만들었습니다.

## To-do

- [x] command를 통해 카카오맵 폴더 새로 생성, 마커 모양 및 색깔 지정 가능
- [x] 네이버 길찾기앱 즐겨찾기 폴더 여러개를 한번에 카카오맵 즐겨찾기 폴더 하나에 넣기 가능
- [ ] 구글맵 <-> 카카오맵 <-> 네이버 맵
- [ ] 다른 사람들의 폴더도 서로 공유할 수 있도록 하기
- [ ] 장소 공유 빈도 수 관련 데이터 수집

## Usage

    $ python3 main.py --naver_id=NAVER_ID \
                      --naver_pw=NAVER_PW
                    --naver_folder=NAVER_FOLDER_NAME
                    --kakao_id=KAKAO_ID
                    --kakao_pw=KAKAO_PW
                    --kakao_folder=KAKAO_FOLDER_NAME
                    --shape=MARKER_SHAPE
                    --color=MARKER_COLOR
                    --os=YOUR_OS

To see all options, run:

    $ python3 main.py --help

which will print:

    usage: main.py [-h] --naver_id NAVER_ID --naver_pw NAVER_PW --naver_folder NAVER_LIST --kakao_id KAKAO_ID
               --kakao_pw KAKAO_PW [--kakao_folder KAKAO_FOLDER] [--shape SHAPE] [--color COLOR] --os OS

    optional arguments:
    -h, --help            show this help message and exit
    --naver_id NAVER_ID
    --naver_pw NAVER_PW
    --naver_folder NAVER_LIST
    --kakao_id KAKAO_ID
    --kakao_pw KAKAO_PW
    --kakao_folder KAKAO_FOLDER
    --shape SHAPE         star, heart, thunder, check, eye, smile, shine, clover, rect, like
    --color COLOR         red, yellow, orange, light green, green, purple, pink
    --os OS               mac, window

## Author

Sooyoung Moon / [@symoon94](https://www.facebook.com/msy0128)
