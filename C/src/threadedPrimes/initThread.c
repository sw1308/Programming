#include <threadedPrimes.h>

/*
This thread will begin by reading the saved primes from the primeFile, it will
then test to see whether there are enough primes to not starve the system.

If there are then the thread will terminate, if not then the thread will
generate prime numbers in order until it has an array of appropriate size, at
which point it will return the array and terminate.
*/

int* fillSortedList()
{
	printf("Init Thread has been started.\n");
	printf("Prines file is %s\n", primeFile);

	return {0, 1};
}