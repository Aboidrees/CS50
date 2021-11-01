from cs50 import get_int

height = get_int("Height: ")

# check input
while height < 1 or height > 8:
    height = get_int("Height: ")


for i in range(height):
    # adding the first leading space
    print((" " * (height - i-1)) + ("#" * (i+1)))
