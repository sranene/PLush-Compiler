#include <stdlib.h>
#include <stdbool.h>

void print_int(int value) {
    printf("%d\n", value);
}

void print_string(const char* value) {
    printf("%s\n", value);
}

void print_arrayint(int* array) {
    for (int i = 0; i < 10; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");
}

void print_float(float value) {
    printf("%f\n", value);
}

void print_arrayint2(int** array, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
}

void print_char(char value) {
    printf("%c\n", value);
}

void print_boolean(bool value) {
    if (value) {
        printf("True\n");
    } else {
        printf("False\n");
    }
}

////////////////////////////////////////////////////////////

int* createEmptyArray() {
    int* arr = (int*)malloc(10 * sizeof(int));
    for (int i = 0; i < 10; ++i) {
        arr[i] = 0;
    }
    return arr;
}

int** createArray2v1() {
    int** arr = (int**)malloc(3 * sizeof(int*));
    
    arr[0] = (int*)malloc(4 * sizeof(int));
    arr[1] = (int*)malloc(4 * sizeof(int));
    arr[2] = (int*)malloc(4 * sizeof(int));
    
    int values1[] = {1, 2, 3, 4};
    int values2[] = {5, 6, 7, 8};
    int values3[] = {123, 456, 789, 1};
    
    for (int i = 0; i < 4; ++i) {
        arr[0][i] = values1[i];
        arr[1][i] = values2[i];
        arr[2][i] = values3[i];
    }
    
    return arr;
}

int** createArray2v2() {
    int** arr = (int**)malloc(3 * sizeof(int*));
    
    arr[0] = (int*)malloc(4 * sizeof(int));
    arr[1] = (int*)malloc(4 * sizeof(int));
    arr[2] = (int*)malloc(4 * sizeof(int));
    
    int values1[] = {2, 2, 4, 4};
    int values2[] = {5, 6, 7, 8};
    int values3[] = {123, 456, 7890000, 1};
    
    for (int i = 0; i < 4; ++i) {
        arr[0][i] = values1[i];
        arr[1][i] = values2[i];
        arr[2][i] = values3[i];
    }
    
    return arr;
}