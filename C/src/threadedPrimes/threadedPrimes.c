#include <unistd.h>
#include <threadedPrimes.h>

int numThreads;
int nextNum;
char* threadIDs;
int* sortedPrimes;
int sortedPrimesSize;
int* generatedPrimes;
int generatedPrimesSize;

int terminate = false;

char* primeFile = "../dat/primes.txt";
pthread_t controlThread;
pthread_t sortThread;
pthread_t* genThreads;

void initThreads(int threadCount)
{
	int i;

	/* Create sortThread */
	pthread_create(&sortThread, NULL, sortMain, NULL);

	// Populate a set of generationThreads
	genThreads = (pthread_t*) malloc(threadCount * sizeof (pthread_t*));

	for(i=0; i<threadCount; i++)
	{
		pthread_create(&genThreads[i], NULL, genMain, threadIDs+i);
	}

	/* Create controllerThread and hand it a pointer to the set of generationThreads */
	pthread_create(&controlThread, NULL, controlMain, genThreads);

	/* Wait for controlThread to terminate, ensuring that progress has been dumped to file */
	pthread_join(controlThread, NULL);
	pthread_join(sortThread, NULL);
	printf("All threads has terminated, exiting.\n");
}

int main(int argc, char const *argv[])
{
	int procCount = sysconf(_SC_NPROCESSORS_ONLN); // Get number of available CPU threads
	int i;

	// sortedPrimes[0] = 2;

	numThreads = procCount * 2;
	threadIDs = malloc(sizeof(char) * numThreads);
	for(i=0; i<numThreads; i++)
	{
		threadIDs[i] = i;
	}

	initThreads(numThreads);

	free(generatedPrimes);

	return 0;
}
