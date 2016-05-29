#include <assert.h>

void *sortMain();
void quicksort(int* array, int size);
void insertionsort(int* array, int start, int end);
int tearDown();
void gateWait();
int getID();
void waitForSort(char id);
void trySort();