#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height < 1 || height > 8);



    for (int i = 0; i < height; i++)
    {
        // adding the first leading space
        for (int j = height - i; j > 1 ; j--)
        {
            printf(" ");
        }

        // adding reverced peramid
        for (int j = 0; j <= i; j++)
        {
            printf("#");
        }

        // going to the new line
        printf("\n");
    }
}