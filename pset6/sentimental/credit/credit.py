from math import floor
from cs50 import get_string


card = get_string("Number: ").strip()
count = len(card)

# presist enter card number
while not card.isnumeric() or (count not in [13, 15, 16]):
    if count > 1 and count < 13:
        print("INVALID")
        exit()

    card = get_string("Number: ").strip()
    count = len(card)

card_checksum = 0


# running Luhn’s Algorithm
# even digits
for i in range(count-2, -1, -2):
    even_digit = int(card[i]) * 2
    card_checksum += floor(even_digit / 10) + even_digit % 10

# odd digits
for i in range(count-1, -1, -2):
    card_checksum += int(card[i])

if card_checksum % 10 != 0:
    print("INVALID")
    exit()


# get Card type
if card[0] == "4":
    print("VISA")
    exit()

else:
    if card[0] == "5" or card[0] == "3":
        # check master
        if int(card[1]) > 0 and int(card[1]) < 6:
            print("MASTERCARD")
            exit()

        # check AMEX
        elif card[1] == "4" or card[1] == "7":
            print("AMEX")
            exit()

        # Invalid
        else:
            print("INVALID")
            exit()
