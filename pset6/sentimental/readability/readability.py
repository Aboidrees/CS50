from cs50 import get_string

# read text
s = get_string("Input: ").strip()

# set vars
length = len(s)
words = 0
sentences = 0
letters = 0

# loop over letters
for i in s:
    # inspect letters
    if i.isalnum():
        letters += 1

    # inspect words
    if i == " ":
        words += 1

    # inspect sentences
    if i == "!" or i == "." or i == "?":
        sentences += 1

# words must be number of spaces + 1
if length > 0:
    words += 1

# average number of sentences per 100 words
S = sentences * 100.0 / words  # 4 * 100 / 14

# average number of sentences per 100 words
L = letters * 100.0 / words


index = (0.0588 * L) - (0.296 * S) - (15.8)

if index < 1:
    print("Before Grade 1")

elif index > 16:
    print("Grade 16+")

else:
    print("Grade " + str(round(index)))


# print(letters)