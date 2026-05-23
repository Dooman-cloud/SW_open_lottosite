# SW_open_lottosite

Django와 Docker를 사용하여 구현한 6/45 Lotto 웹 사이트 프로젝트 과제

일반 사용자의 로또 구매 및 당첨 확인 기능과 관리자의 판매 내역 확인, 추첨 기능, 당첨 내역 확인 기능을 제공

---

## 1. 프로젝트 개요

본 프로젝트의 목표는 Django 웹 프레임워크를 활용하여 6/45 Lotto 웹 서비스를 구현하고, Docker Compose를 사용하여 웹 애플리케이션과 데이터베이스를 multi-container 환경으로 구성

- Django 기반 웹 애플리케이션 구현
- 6/45 로또 수동 번호 구매 기능
- 6/45 로또 자동 번호 구매 기능
- 관리자 추첨 기능
- 사용자 당첨 확인 기능
- 관리자 당첨 내역 확인 기능
- Docker Compose 기반 web/db multi-container 구성

---

## 2. 주요 기능

### 2.1 일반 사용자 기능

- 메인 페이지 접속
- 수동 번호 구매
  - 구매자 이름 입력
  - 1~45 사이의 중복 없는 번호 6개 직접 입력
- 자동 번호 구매
  - 구매자 이름 입력
  - 서버에서 1~45 사이의 중복 없는 번호 6개 자동 생성
- 구매 완료 내역 확인
  - 구매 ID
  - 구매자
  - 구매 방식
  - 선택 번호
  - 구매 일시
- 당첨 확인
  - 구매 ID를 입력하여 최신 추첨 결과 기준으로 당첨 여부 확인

### 2.2 관리자 기능

- Django admin을 통한 판매 내역 확인
- 관리자 추첨 기능
  - 회차 입력
  - 당첨번호 6개 및 보너스 번호 1개 자동 생성
- 추첨 결과 목록 확인
- 당첨 내역 확인
  - 구매 ID
  - 구매자
  - 회차
  - 일치 개수
  - 보너스 번호 일치 여부
  - 당첨 등수

---

## 3. 기술 스택

| 구분 | 사용 기술 |
|---|---|
| Language | Python |
| Web Framework | Django |
| Database(Local) | SQLite |
| Database(Docker) | PostgreSQL |
| Container | Docker |
| Multi-container | Docker Compose |
| Version Control | Git / GitHub |
| IDE | Visual Studio Code |

---

## 4. 프로젝트 구조

```text
SW_open_lottosite/
├─ manage.py #django 명령어 실행 파일 
├─ lotto_project/
│  ├─ settings.py #Django 프로젝트 설정, 앱 등록, DB 설정
│  ├─ urls.py #프로젝트 전체 url 연결
│  ├─ wsgi.py 
│  └─ asgi.py
│
├─ lotto/
│  ├─ admin.py #Django admin에 모델 등록
│  ├─ apps.py #
│  ├─ forms.py #수동 구매, 자동 구매, 추첨, 당첨 확인 Form 정의
│  ├─ models.py #Draw, Ticket, WinningResult 모델 정의
│  ├─ services.py #번호 생성, 번호 검증, 등수 계산 로직
│  ├─ urls.py #lotto 앱 내부 URL 연결
│  ├─ views.py #페이지 요청 처리
│  ├─ migrations/
│  └─ templates/
│     └─ lotto/
│        ├─ home.html
│        ├─ buy_manual.html
│        ├─ buy_auto.html
│        ├─ ticket_detail.html
│        ├─ admin_draw.html
│        ├─ draw_list.html
│        ├─ check_result.html
│        ├─ result_detail.html
│        └─ winning_result_list.html
│
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .gitignore
├─ .dockerignore
└─ README.md

데이터모델

1.Draw

추첨 회차와 당첨번호를 저장하는 모델:
회차 번호
당첨번호 6개
보너스 번호
추첨 일시

2.Ticket

사용자의 로또 구매 정보를 저장하는 모델:
구매자 이름
구매 방식: 수동 / 자동
선택 번호 6개
구매 일시

3.WinningResult

당첨 확인 결과를 저장하는 모델:
구매 티켓
추첨 회차
일치 개수
보너스 번호 일치 여부
당첨 등수
확인 일시