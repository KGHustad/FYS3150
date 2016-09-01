#include <iostream>

using namespace std;

int main(int argc, char *argv[])
{
    int number1 = 5;
    int number2 = number1;
    int *adress1 = &number1;     //adress variables must always start with a star
    int *adress2 = &number2;
    cout << "number1 adress: " << (long)&adress1 << endl;    //we print the pointer(memory adress) of number1
    cout << "number2 adress: " << (long)&adress2 << endl;   //we print with "cout" (console out)

    cout << "the size of number1 is: " << sizeof(number1) << endl;  //"sizeof()" checks the size of a variable or object type
    cout << "the size of a double is " << sizeof(double) << endl;

    //de-referencing operator - we can access a variable through it's adress, with a *-operator:
    cout << "number1 should be: " << *adress1 << endl;
    //we can even change the number with the de-referncing operator:
    *adress1 = 10;
    cout << "number1 is now: " << number1 << endl;


    int *array = new int[10]; //dynamic memory allocation - use this
    *array = 1337; //*array gives us a pointer to the FIRST(array[0]) element in the array. We then set it to 1337.
    cout << *array << endl;
    cout << array[0] << endl;
    array[0] = 10;
    cout << array[0] << endl;

    int array2[10]; //static memeory allocation - don't use

    return 0;
}
