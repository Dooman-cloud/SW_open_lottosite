# SW_open_lottosite

Django와 Docker를 사용하여 구현하는 6/45 Lotto 웹 사이트 과제

## 프로젝트 개요

본 프로젝트는 Django 웹 프레임워크와 Docker 기반 multi-container 환경을 활용하여 로또 웹 서비스를 구현하는 것이 목표

## 주요 기능

### 일반 사용자 기능

- 수동 번호로 로또 구매
- 자동 번호로 로또 구매
- 로또 당첨 여부 확인

### 관리자 기능

- 로또 판매 내역 확인
- 로또 추첨
- 당첨 내역 확인

## 기술 스택

- Python
- Django
- SQLite
- Docker
- Docker Compose
- Git / GitHub

## 현재 진행 상황

- GitHub Repository 생성
- Python 가상환경 구성
- Django 프로젝트 생성
- `lotto` 앱 생성
- 기본 메인 페이지 구성

## 프로젝트 구조

```text
open_source_lotto/
├─ manage.py
├─ lotto_project/
│  ├─ settings.py
│  ├─ urls.py
│  └─ ...
├─ lotto/
│  ├─ admin.py
│  ├─ models.py
│  ├─ views.py
│  ├─ urls.py
│  ├─ forms.py
│  ├─ services.py
│  └─ templates/
├─ requirements.txt
├─ README.md
├─ .gitignore
└─ venv/
