#include <cs50.h>
#include <stdio.h>



int main(void)
{
    int n;
    int m;
    int y = 0;

    // TODO: Prompt for start size
    do
    {
        n = get_int("Start size: ");
    }
    while (n < 9);

    // TODO: Prompt for end size
    do
    {
        m = get_int("End size: ");
    }
    while (m < n);
    // TODO: Calculate number of years until we reach threshold

    while (n < m)
    {
        n = (n + (n / 3) - (n / 4));

        y++;
    }

    // TODO: Print number of years
    printf("Years: %i", y);

}


