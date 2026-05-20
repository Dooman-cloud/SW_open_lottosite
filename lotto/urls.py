from django.urls import path
from . import views

app_name = 'lotto'

#urls.py에서 URL 패턴과 view 함수를 연결함
#로또사이트 home 페이지로 이동하는 URL 패턴을 정의함
urlpatterns = [
    path('', views.home, name='home'),
]