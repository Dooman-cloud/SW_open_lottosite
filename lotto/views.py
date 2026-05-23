from django.shortcuts import render, redirect, get_object_or_404
from .forms import ManualTicketForm, AutoTicketForm
from .models import Ticket
from .services import generate_lotto_numbers


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