#include <ctype.h>
#include <string.h>
#include <stdlib.h>
#include <cs50.h>
#include <stdio.h>


int main(int argc, char **argv)
{



    // inputs: text + key
    string key = argv[1];


    // validate the input
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    if (strlen(key) != 26)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }


    for (int i = 0; i < strlen(key); i++)
    {
        int count = 0;
        for (int j = 0; j < strlen(key); j++)
        {
            if (key[i] == key[j] && i != j)
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }

        }

        if (!isalpha(key[i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }

    }

    string plaintext = get_string("plaintext: ");


    int letter_index;


    // loop and convert the letters
    for (int i = 0; i < strlen(plaintext); i++)
    {

        // generate letter index
        letter_index = ((int)plaintext[i] - (isupper(plaintext[i]) ? 65 : 97));

        // replace the letter
        plaintext[i] = isupper(plaintext[i]) ? toupper((char) key[letter_index]) : plaintext[i];
        plaintext[i] = islower(plaintext[i]) ? tolower((char) key[letter_index]) : plaintext[i];
    }

    // printf("KEY: %s\n", upper.collection);
    // printf("key: %s\n", lower.collection);
    printf("ciphertext: %s\n", plaintext);

    return 0;
}


