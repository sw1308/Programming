#include <threadedPrimes.h>

/*
This thread will control the flow of data and maintain concurrency within
it's critical sections. The functions of this thread are defined as follows.

Populate main array from primes file.

If length of the main array is less than some arbitrary limit then start an
initializerThread to fill in the rest of the initial main array and ensure it is
in order.

Create a set of generationThreads and start them all.

Create a sortThread and start it (it will start blocked).

Hand out test case to a requesting thread and increment the current test case
counter, this function is a critical section and will only be able to be run for
one thread at a time.

Upon reaching the goal number of generations or upon exiting, a STOP message
will be broadcast and the controllerThread will block until all ACK messages
have been received from generationThread set. Then send a SORT message and
terminate upon receiving a RESUME message.
*/
int nextNum;
pthread_mutex_t nextNumLock;
pthread_mutex_t genPrimesLock;

int getNext()
{
	int temp;
	// Lock nextNum
	pthread_mutex_lock(&nextNumLock);
	
	nextNum++;
	temp = nextNum;

	// Unlock nextNum
	pthread_mutex_unlock(&nextNumLock);
	return temp;
}

void addPrime(int newPrime)
{
	// Lock genPrimes
	pthread_mutex_lock(&genPrimesLock);

	generatedPrimes = (int*) realloc(generatedPrimes, sizeof(generatedPrimes[0]) * (generatedPrimesSize+1));
	generatedPrimes[generatedPrimesSize] = newPrime;
	generatedPrimesSize++;

	// Unlock genPrimes
	pthread_mutex_unlock(&genPrimesLock);
}

void *controlMain(void* args)
{
	pthread_t* genThreads = args;

	int i=0;

	pthread_mutex_init(&nextNumLock, NULL);
	pthread_mutex_init(&genPrimesLock, NULL);

	// sortedPrimes[1] = 3;

	for(i=0; i<numThreads; i++)
	{
		pthread_join(genThreads[i],NULL);
	}

	terminate = true;

	printf("Found primes: %d\n", generatedPrimesSize);

	pthread_mutex_destroy(&nextNumLock);
	pthread_mutex_destroy(&genPrimesLock);

	printf("All generation threads have completed, exiting.\n");

	pthread_exit(NULL);
}