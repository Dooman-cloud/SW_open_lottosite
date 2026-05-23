from django.contrib import admin
from .models import Draw, Ticket, WinningResult

#관리자가 판매 내역, 추첨 결과, 당첨 내역을 확인할 수 있도록 Draw, Ticket, WinningResult를 admin에 등록

@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    list_display = (
        "round_no",
        "number1",
        "number2",
        "number3",
        "number4",
        "number5",
        "number6",
        "bonus_number",
        "drawn_at",
    )
    ordering = ("-round_no",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer_name",
        "purchase_type",
        "draw",
        "number1",
        "number2",
        "number3",
        "number4",
        "number5",
        "number6",
        "created_at",
    )
    list_filter = ("purchase_type", "draw")
    search_fields = ("buyer_name",)


@admin.register(WinningResult)
class WinningResultAdmin(admin.ModelAdmin):
    list_display = (
        "ticket",
        "draw",
        "matched_count",
        "bonus_matched",
        "rank",
        "checked_at",
    )
    list_filter = ("rank", "draw")