from django.shortcuts import render

#HTTP 요청받아 응답 반환
def home(request):
    return render(request, 'lotto/home.html')

