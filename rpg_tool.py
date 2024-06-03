import random

def roll_dice(characteristic, dice):
    return random.randint(1, dice) + characteristic[1]

def rool_dice_without_characteristic(dice):
    return random.randint(1, dice)