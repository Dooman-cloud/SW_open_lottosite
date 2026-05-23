from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('', views.home, name='home'),
    path('buy/manual/', views.buy_manual, name='buy_manual'),
    path('buy/auto/', views.buy_auto, name='buy_auto'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]