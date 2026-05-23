from django.db import models


class Draw(models.Model):
    round_no = models.PositiveIntegerField(unique=True, verbose_name="회차")

    number1 = models.PositiveIntegerField(verbose_name="당첨번호 1")
    number2 = models.PositiveIntegerField(verbose_name="당첨번호 2")
    number3 = models.PositiveIntegerField(verbose_name="당첨번호 3")
    number4 = models.PositiveIntegerField(verbose_name="당첨번호 4")
    number5 = models.PositiveIntegerField(verbose_name="당첨번호 5")
    number6 = models.PositiveIntegerField(verbose_name="당첨번호 6")
    bonus_number = models.PositiveIntegerField(verbose_name="보너스 번호")

    drawn_at = models.DateTimeField(auto_now_add=True, verbose_name="추첨 일시")

    def __str__(self):
        return f"{self.round_no}회차 추첨"


class Ticket(models.Model):
    PURCHASE_TYPE_CHOICES = [
        ("manual", "수동"),
        ("auto", "자동"),
    ]

    buyer_name = models.CharField(max_length=50, verbose_name="구매자 이름")
    draw = models.ForeignKey( #추첨 회차 번호 저장
        Draw,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tickets",
        verbose_name="추첨 회차"
    )

    number1 = models.PositiveIntegerField(verbose_name="선택한 번호 1")
    number2 = models.PositiveIntegerField(verbose_name="선택한 번호 2")
    number3 = models.PositiveIntegerField(verbose_name="선택한 번호 3")
    number4 = models.PositiveIntegerField(verbose_name="선택한 번호 4")
    number5 = models.PositiveIntegerField(verbose_name="선택한 번호 5")
    number6 = models.PositiveIntegerField(verbose_name="선택한 번호 6")

    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        verbose_name="구매 방식"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="구매 날짜")

    def __str__(self):
        return f"{self.buyer_name} - {self.get_purchase_type_display()} 구매"


class WinningResult(models.Model): #당첨 결과 저장 
    RANK_CHOICES = [
        ("1등", "1등"),
        ("2등", "2등"),
        ("3등", "3등"),
        ("4등", "4등"),
        ("5등", "5등"),
        ("낙첨", "낙첨"),
    ]

    ticket = models.OneToOneField(
        Ticket,
        on_delete=models.CASCADE,
        related_name="winning_result",
        verbose_name="구매 티켓"
    )

    draw = models.ForeignKey(
        Draw,
        on_delete=models.CASCADE,
        related_name="winning_results",
        verbose_name="추첨 회차"
    )

    matched_count = models.PositiveIntegerField(verbose_name="일치 개수")
    bonus_matched = models.BooleanField(default=False, verbose_name="보너스 번호 일치 여부")
    rank = models.CharField(max_length=10, choices=RANK_CHOICES, verbose_name="당첨 등수")

    checked_at = models.DateTimeField(auto_now_add=True, verbose_name="확인 일시")

    def __str__(self):
        return f"{self.ticket.buyer_name} - {self.rank}"