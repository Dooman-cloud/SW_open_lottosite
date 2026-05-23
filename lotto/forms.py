from django import forms
from .services import validate_lotto_numbers

#사용자가 수동 구매 시 1~45 사이의 중복 없는 번호 6개인지 검사하도록 clean() 메서드를 작성

class ManualTicketForm(forms.Form):
    buyer_name = forms.CharField(
        max_length=50,
        label="구매자 이름"
    )

    number1 = forms.IntegerField(label="번호 1", min_value=1, max_value=45)
    number2 = forms.IntegerField(label="번호 2", min_value=1, max_value=45)
    number3 = forms.IntegerField(label="번호 3", min_value=1, max_value=45)
    number4 = forms.IntegerField(label="번호 4", min_value=1, max_value=45)
    number5 = forms.IntegerField(label="번호 5", min_value=1, max_value=45)
    number6 = forms.IntegerField(label="번호 6", min_value=1, max_value=45)

    def clean(self):
        cleaned_data = super().clean()

        numbers = [
            cleaned_data.get("number1"),
            cleaned_data.get("number2"),
            cleaned_data.get("number3"),
            cleaned_data.get("number4"),
            cleaned_data.get("number5"),
            cleaned_data.get("number6"),
        ]

        if None in numbers:
            return cleaned_data

        if not validate_lotto_numbers(numbers):
            raise forms.ValidationError("로또 번호는 1~45 사이의 중복 없는 숫자 6개여야 합니다.")

        return cleaned_data


class AutoTicketForm(forms.Form):
    buyer_name = forms.CharField(
        max_length=50,
        label="구매자 이름"
    )