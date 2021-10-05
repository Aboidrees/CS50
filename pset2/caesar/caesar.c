#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdio.h>

// upper and lower letters container
//+ the start in the ascii chart
struct Letter
{
    string collection;
    int start;
};



int main(int argc, char **argv)
{


    // validate the input
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    string av = argv[1];

    for (int i = 0; i < strlen(av); i++)
    {
        if (!isdigit(av[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

    }

    // inputs: text + key
    int key = atoi(argv[1]);
    string plaintext = get_string("plaintext: ");


    struct Letter upper;
    upper.collection = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    upper.start = 65;

    struct Letter lower;
    lower.collection = "abcdefghijklmnopqrstuvwxyz";
    lower.start = 97;

    struct Letter letter;

    int letter_index;


    // loop and convert the letters
    for (int i = 0; i < strlen(plaintext); i++)
    {
        // switch between upper and lower
        letter = isupper(plaintext[i]) ? upper : lower;

        // generate letter index
        letter_index = ((int)plaintext[i] - letter.start + key) % 26;

        // replace the letter
        plaintext[i] = isalpha(plaintext[i]) ? (char) letter.collection[letter_index] : plaintext[i];


    }

    printf("ciphertext: %s\n", plaintext);

    return 0;
}