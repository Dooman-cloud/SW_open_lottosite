from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .forms import ManualTicketForm, AutoTicketForm, DrawForm
from .models import Ticket, Draw
from .services import generate_lotto_numbers, generate_draw_numbers


def home(request):
    return render(request, 'lotto/home.html')


def buy_manual(request):
    if request.method == "POST":
        form = ManualTicketForm(request.POST)

        if form.is_valid():
            ticket = Ticket.objects.create(
                buyer_name=form.cleaned_data["buyer_name"],
                number1=form.cleaned_data["number1"],
                number2=form.cleaned_data["number2"],
                number3=form.cleaned_data["number3"],
                number4=form.cleaned_data["number4"],
                number5=form.cleaned_data["number5"],
                number6=form.cleaned_data["number6"],
                purchase_type="manual",
            )

            return redirect("lotto:ticket_detail", ticket_id=ticket.id)
    else:
        form = ManualTicketForm()

    return render(request, "lotto/buy_manual.html", {"form": form})


def buy_auto(request):
    if request.method == "POST":
        form = AutoTicketForm(request.POST)

        if form.is_valid():
            numbers = generate_lotto_numbers()

            ticket = Ticket.objects.create(
                buyer_name=form.cleaned_data["buyer_name"],
                number1=numbers[0],
                number2=numbers[1],
                number3=numbers[2],
                number4=numbers[3],
                number5=numbers[4],
                number6=numbers[5],
                purchase_type="auto",
            )

            return redirect("lotto:ticket_detail", ticket_id=ticket.id)
    else:
        form = AutoTicketForm()

    return render(request, "lotto/buy_auto.html", {"form": form})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    numbers = [
        ticket.number1,
        ticket.number2,
        ticket.number3,
        ticket.number4,
        ticket.number5,
        ticket.number6,
    ]

    context = {
        "ticket": ticket,
        "numbers": numbers,
    }

    return render(request, "lotto/ticket_detail.html", context)

@staff_member_required


def admin_draw(request):
    """
admin_draw
- 관리자만 접근 가능
- 회차 번호 입력
- 중복 회차 검사
- 당첨번호/보너스 번호 생성
- Draw 모델에 저장 후 draw_list로 리다이렉트
draw_list
- 저장된 추첨 결과 목록 표시
"""
    if request.method == "POST":
        form = DrawForm(request.POST)

        if form.is_valid():
            round_no = form.cleaned_data["round_no"]

            if Draw.objects.filter(round_no=round_no).exists():
                form.add_error("round_no", "이미 존재하는 회차입니다.")
            else:
                winning_numbers, bonus_number = generate_draw_numbers()

                draw = Draw.objects.create(
                    round_no=round_no,
                    number1=winning_numbers[0],
                    number2=winning_numbers[1],
                    number3=winning_numbers[2],
                    number4=winning_numbers[3],
                    number5=winning_numbers[4],
                    number6=winning_numbers[5],
                    bonus_number=bonus_number,
                )

                return redirect("lotto:draw_list")
    else:
        form = DrawForm()

    return render(request, "lotto/admin_draw.html", {"form": form})


@staff_member_required
def draw_list(request):
    draws = Draw.objects.all().order_by("-round_no")

    return render(request, "lotto/draw_list.html", {"draws": draws})