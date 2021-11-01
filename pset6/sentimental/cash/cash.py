from math import floor
from cs50 import get_float


dollar = get_float("Change owed: ")
while dollar <= 0:
    dollar = get_float("Change owed: ")

# setting cents and coins
cents = round(dollar * 100)
coins = 0

# calculating 25 cents
if cents >= 25:
    coins += floor(cents / 25)
    cents %= 25

# calculating 10 cents
if cents >= 10:
    coins += floor(cents / 10)
    cents %= 10


# calculating 5 cents
if cents >= 5:
    coins += floor(cents / 5)
    cents %= 5

# calculating 1 cents
if cents >= 1:
    coins += floor(cents / 1)
    cents %= 1

print(coins)
