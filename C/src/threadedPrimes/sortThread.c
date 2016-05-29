#include <threadedPrimes.h>

/*
This thread will sort the generated array upon receiving a SORT message from all
generator threads, then broadcast a RESUME message after sorting the generatedPrimes
array and appending it to the sortedPrimes list.
*/

char knockCount;
char idCount;

pthread_mutex_t gateLock;
pthread_mutex_t idLock;
pthread_mutex_t* threadLock;

pthread_t gateThread;

void trySort()
{
	pthread_mutex_lock(&gateLock);
	knockCount++;
	printf("Knocked %d time(s)\n", knockCount);
	pthread_mutex_unlock(&gateLock);
}

void waitForSort(char id)
{
	printf("thread %d is waiting on a sort\n", id);
	pthread_mutex_lock(&threadLock[id]);
	pthread_mutex_unlock(&threadLock[id]);
	printf("thread %d is resuming\n", id);
}

void gateWait()
{
	int i;
	for(i=0; i<numThreads; i++)
	{
		pthread_mutex_lock(&threadLock[i]);
	}

	while(knockCount < numThreads);

	pthread_mutex_lock(&gateLock);
	knockCount = 0;
	pthread_mutex_unlock(&gateLock);

	quicksort(generatedPrimes, generatedPrimesSize);

	for(i=0; i<numThreads; i++)
	{
		pthread_mutex_unlock(&threadLock[i]);
	}
}

int tearDown()
{
	assert(pthread_mutex_destroy(&gateLock) == 0);
	assert(pthread_mutex_destroy(&idLock) == 0);

	int i;
	for(i=0; i<numThreads; i++)
	{
		assert(pthread_mutex_destroy(&threadLock[i]) == 0);
	}

	return 0;
}

void insertionsort(int* array, int start, int end)
{
	;
}

void quicksort(int* array, int size)
{
	int i, j, p, t;
	if (size < 2) return;

	p = array[size / 2];
	
	for (i = 0, j = size - 1;; i++, j--)
	{
		while (array[i] < p)
			i++;
		while (p < array[j])
			j--;
		if (i >= j)
			break;
		t = array[i];
		array[i] = array[j];
		array[j] = t;
	}

	quicksort(array, i);
	quicksort(array + i, size - i);
}

void *sortMain()
{
	int i;
	
	idCount = -1;
	threadLock = malloc( sizeof(pthread_mutex_t) * numThreads);

	pthread_mutex_init(&gateLock, NULL);
	pthread_mutex_init(&idLock, NULL);

	for(i=0; i<numThreads; i++)
	{
		pthread_mutex_init(&threadLock[i], NULL);
	}

	while(!terminate)
	{
		gateWait();
	}

	tearDown();
	return;
}
