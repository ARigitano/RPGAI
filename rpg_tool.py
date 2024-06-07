import random

def roll_dice(dice, bonus_characteristic):
    roll_result = random.randint(1, dice)
    total_result = roll_result + bonus_characteristic
    result_string = f"Rolled a {roll_result} + {bonus_characteristic} = {total_result}"
    return total_result, result_string


def get_characteristic_bonus(characteristic):
    return (characteristic - 10) // 2