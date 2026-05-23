from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('', views.home, name='home'),
    path('buy/manual/', views.buy_manual, name='buy_manual'),
    path('buy/auto/', views.buy_auto, name='buy_auto'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('staff/draw/', views.admin_draw, name='admin_draw'), #관리자 추첨 기능 추가
    path('draws/', views.draw_list, name='draw_list'), #추첨 회차 목록 페이지 추가
]