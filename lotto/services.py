import random

#views.py에 모든 로직을 넣지 않고, 별도 모듈을 만들어 기능을 분리
#로또 번호 자동 생성, 번호 검증, 당첨 등수 계산 로직을 해당 파일에 분리

def generate_lotto_numbers():
    """
    1~45 사이에서 중복 없는 로또 번호 6개를 생성한다.
    """
    numbers = random.sample(range(1, 46), 6)
    return sorted(numbers)


def validate_lotto_numbers(numbers):
    """
    로또 번호가 6개인지, 중복이 없는지, 1~45 범위인지 검증한다.
    """
    if len(numbers) != 6:
        return False

    if len(set(numbers)) != 6:
        return False

    for number in numbers:
        if number < 1 or number > 45:
            return False

    return True


def calculate_rank(ticket_numbers, winning_numbers, bonus_number):
    """
    구매 번호와 당첨 번호를 비교하여 등수를 계산한다.
    """
    matched_count = len(set(ticket_numbers) & set(winning_numbers))
    bonus_matched = bonus_number in ticket_numbers

    if matched_count == 6:
        rank = "1등"
    elif matched_count == 5 and bonus_matched:
        rank = "2등"
    elif matched_count == 5:
        rank = "3등"
    elif matched_count == 4:
        rank = "4등"
    elif matched_count == 3:
        rank = "5등"
    else:
        rank = "낙첨"

    return matched_count, bonus_matched, rank