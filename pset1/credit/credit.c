#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <string.h>



int count_digits(long card)
{
    int count = 0;

    do
    {
        card /= 10;
        ++count;
    }
    while (card != 0);
    return count;
}

bool sum_even_digits(long card, int digits_number)
{

    int extracted_digit;
    int even_sum = 0;
    int odd_sum = 0;

    // loop over digits
    for (int i = 1; i <= digits_number; i++)
    {
        // extract lest digit and the save the remaining
        extracted_digit = (int)(card % 10);
        card = (long)(card / 10);

        // agregate even digits
        if (i % 2 == 0)
        {
            extracted_digit *= 2;
            even_sum += ((int)extracted_digit / 10 + (int)extracted_digit % 10);
        }
        // summing odd digits
        else
        {
            odd_sum += extracted_digit;
        }
    }

    // check the first digit
    return ((even_sum + odd_sum) % 10 == 0);
}

string get_card_type(long card, int digits_number)
{
    // get left digit
    int most_digit = (int)(card / (long)pow(10, digits_number - 1));

    // check left digit if its visa or else
    if (most_digit == 4)
    {
        return "VISA";
    }
    else if (most_digit == 5 || most_digit == 3)
    {
        // get second left digit for other than visa
        int second_most = (int)(card / (long)pow(10, digits_number - 2)) % 10;

        // master card check
        if (second_most > 0 && second_most < 6)
        {
            return "MASTERCARD";
        }
        // american express  check
        else if (second_most == 4 || second_most == 7)
        {
            return "AMEX";
        }

        // invalid condition
        else
        {
            return "INVALID";
        }
    }

    // general invalid
    return "INVALID";
}

int main(void)
{
    unsigned long card;
    int count;

    // enter card number
    do
    {
        card = get_long("Number: ");
        count = count_digits(card);
        if (count > 0 && count < 13)
        {
            printf("INVALID\n");
            return 0;
        }

        // printf("%i\n", count);

    }
    while (count != 13 && count != 15 && count != 16);


    // running Luhn’s Algorithm
    if (sum_even_digits(card, count))
    {
        printf("%s\n", get_card_type(card, count));
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}