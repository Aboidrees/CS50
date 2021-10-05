#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>


int main() {
    string s = get_string("Input:  ");


    int length = strlen(s);
    int words = 0;
    int sentences = 0;
    int letters = 0;


    for(int i = 0; i < length; i++ )
    {
        if(s[i] == ' ')
        {
            words++;
        }

        if((s[i] > 65 && s[i] < 91) || (s[i] > 96 && s[i] < 123))
        {
            letters++;
        }

        if(s[i] == '.' || s[i] == '!' || s[i] == '?')
        {
            sentences++;
        }

    }
    if(length > 0){
        words += 1;
    }

    // average number of sentences per 100 words
    float S = sentences * 100 / words; // 4 * 100 / 14

    // average number of sentences per 100 words
    float L = letters * 100 / words;


    float index = (0.0588 * L) - (0.296 * S) - (15.8);


    if( index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if(index > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) round(index));
    }
    // printf("Letters: %i\nWords: %i\nSentences: %i \nL: %f\nS: %f\nGrade : %f\n", letters, words, sentences, L, S, index);


    return 0;
}