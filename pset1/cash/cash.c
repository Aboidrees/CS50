#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    float dollar;
    do
    {
        dollar = get_float("Change owed: ");
    }
    while (dollar <= 0);

    // setting cents and coins
    int cents = round(dollar * 100);
    int coins = 0;

    // calculating 25 cents
    if (cents >= 25)
    {
        coins += (int) cents / 25;
        cents %= 25;
    }

    // calculating 10 cents
    if (cents >= 10)
    {
        coins += (int) cents / 10;
        cents %= 10;
    }

    // calculating 5 cents
    if (cents >= 5)
    {
        coins += (int) cents / 5;
        cents %= 5;
    }

    // calculating 1 cents
    if (cents >= 1)
    {
        coins += (int) cents / 1;
        cents %= 1;
    }

    printf("25c coins=%i| remaining=%i\n", coins, cents);
}
