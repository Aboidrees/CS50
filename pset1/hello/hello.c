#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // input the name
    string name = get_string("What is your name?\n");

    //printing the greeting
    printf("hello, %s\n", name);
}