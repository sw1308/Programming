#include <threadedPrimes.h>

/*
This thread will generate prime numbers concurrently, the steps taken are
described below.

Retrieve next number to test from controller thread (blocks)

Test number against all numbers in main array until it reaches one that is less
than square root of test case.

If the end of the main array is reached before becoming larger than or equal to
the square root of test case then send a SORT message to sortThread and block
until receiving RESUME message.

Send ACK message and terminate if STOP message is received else repeat.
*/

int isPrime(int testCase)
{
	return true;
}

void *genMain(void* ID)
{
	int i;
	int newNum;
	char id = *(char*)ID;

	for(i=0; i<10000; i++)
	// while(1)
	{
		newNum = getNext();

		if(isPrime(newNum))
		{
			addPrime(newNum);
		}

		if(newNum % 1000 == 0)
		{
			trySort();
			waitForSort(id);
		}
	}

	pthread_exit(NULL);
}
