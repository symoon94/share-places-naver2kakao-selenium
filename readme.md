# share-places-naver2kakao-selenium

## 네이버맵 -> 카카오맵 즐겨찾기 폴더 공유하기

<p align="center"><img width="80%" src="img/map.png" /></p>

Selenium을 이용하여 네이버에 저장해둔 즐겨찾기 장소들을 카카오맵 폴더에 공유 가능하도록 했습니다.

## To-do

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
