#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <assert.h>

#define THREADNUM 50

int knockCount;
int idCount;

pthread_mutex_t gateLock;
pthread_mutex_t threadLock[THREADNUM];
pthread_mutex_t idLock;

pthread_t gateThread;
pthread_t waitingThreads[THREADNUM];

void knockKnock()
{
	pthread_mutex_lock(&gateLock);
	knockCount++;
	pthread_mutex_unlock(&gateLock);
}

int getID()
{
	pthread_mutex_lock(&idLock);
	idCount++;
	pthread_mutex_unlock(&idLock);
	return idCount;
}

void *threadFunc()
{
	int i = getID();

	knockKnock();

	printf("Thread %d waiting on gate.\n", i);
	pthread_mutex_lock(&threadLock[i]);

	printf("Thread %d finished.\n", i);

	pthread_mutex_unlock(&threadLock[i]);

	pthread_exit(NULL);
}

void *gateWait()
{
	int i;
	for(i=0; i<THREADNUM; i++)
	{
		pthread_mutex_lock(&threadLock[i]);
	}

	while(knockCount < THREADNUM);

	printf("%s\n", "Unlocked the gate.");

	for(i=0; i<THREADNUM; i++)
	{
		pthread_mutex_unlock(&threadLock[i]);
	}

	pthread_exit(NULL);
}

void waitOnThreads()
{
	pthread_join(gateThread, NULL);

	int i;
	for(i=0; i<THREADNUM; i++)
	{
		pthread_join(waitingThreads[i], NULL);
	}

	return;
}

int tearDown()
{
	assert(pthread_mutex_destroy(&gateLock) == 0);
	assert(pthread_mutex_destroy(&idLock) == 0);

	int i;
	for(i=0; i<THREADNUM; i++)
	{
		assert(pthread_mutex_destroy(&threadLock[i]) == 0);
	}

	return 0;
}

int main(int argc, char const *argv[])
{
	int i;
	pthread_mutex_init(&gateLock, NULL);
	pthread_mutex_init(&idLock, NULL);

	knockCount = 0;
	idCount = -1;

	for(i=0; i<THREADNUM; i++)
	{
		pthread_mutex_init(&threadLock[i], NULL);
	}

	pthread_create(&gateThread, NULL, gateWait, NULL);

	for(i=0; i<THREADNUM; i++)
	{
		pthread_create(&waitingThreads[i], NULL, threadFunc, NULL);
	}

	waitOnThreads();

	return tearDown();
}
