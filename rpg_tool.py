import random

def roll_dice(characteristic, dice):
    return random.randint(1, dice) + characteristic[1]

def roll_dice_without_characteristic(dice):
    return random.randint(1, dice)

def get_characterictic_bonus(characteristic):
    return (characteristic - 10) // 2