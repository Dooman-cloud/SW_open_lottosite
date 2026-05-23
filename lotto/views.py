from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .forms import ManualTicketForm, AutoTicketForm, DrawForm, CheckResultForm
from .models import Ticket, Draw, WinningResult
from .services import (
    generate_lotto_numbers,
    generate_draw_numbers,
    calculate_rank,
    get_ticket_numbers,
    get_draw_numbers,
)

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

#당첨확인 서비스 - 사용자가 구매 번호 입력 -> 가장 최신 추첨 회차 기준으로 당첨 확인 -> 결과 저장 및 상세 페이지로 이동
def check_result(request):
    if request.method == "POST":
        form = CheckResultForm(request.POST)

        if form.is_valid():
            ticket_id = form.cleaned_data["ticket_id"]

            try:
                ticket = Ticket.objects.get(id=ticket_id)
            except Ticket.DoesNotExist:
                return render(
                    request,
                    "lotto/check_result.html",
                    {
                        "form": form,
                        "error_message": "해당 구매 id의 티켓이 존재하지 않습니다.",
                    },
                )

            # 현재는 가장 최신 추첨 회차 기준으로 당첨 확인
            latest_draw = Draw.objects.order_by("-round_no").first()

            if latest_draw is None:
                return render(
                    request,
                    "lotto/check_result.html",
                    {
                        "form": form,
                        "error_message": "아직 추첨 결과가 없습니다. 관리자 추첨을 먼저 실행해주세요.",
                    },
                )

            ticket_numbers = get_ticket_numbers(ticket)
            winning_numbers = get_draw_numbers(latest_draw)

            matched_count, bonus_matched, rank = calculate_rank(
                ticket_numbers,
                winning_numbers,
                latest_draw.bonus_number,
            )

            result, created = WinningResult.objects.update_or_create(
                ticket=ticket,
                defaults={
                    "draw": latest_draw,
                    "matched_count": matched_count,
                    "bonus_matched": bonus_matched,
                    "rank": rank,
                },
            )

            return render(
                request,
                "lotto/result_detail.html",
                {
                    "ticket": ticket,
                    "draw": latest_draw,
                    "ticket_numbers": ticket_numbers,
                    "winning_numbers": winning_numbers,
                    "result": result,
                    "created": created,
                },
            )
    else:
        form = CheckResultForm()

    return render(request, "lotto/check_result.html", {"form": form})


@staff_member_required
def winning_result_list(request):
    results = WinningResult.objects.select_related("ticket", "draw").order_by(
        "-checked_at"
    )

    return render(
        request,
        "lotto/winning_result_list.html",
        {"results": results},
    )