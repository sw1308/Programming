#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>

#include <controllerThread.h>
#include <initThread.h>
#include <generationThread.h>
#include <sortThread.h>
#define true 1
#define false 0

extern int numThreads;
extern int terminate;
extern int resume;
extern int* sortedPrimes;
extern int sortedPrimesSize;
extern int* generatedPrimes;
extern int generatedPrimesSize;

void initThreads();