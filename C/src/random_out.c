#include <time.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
	srand(time(NULL));

	printf("%1.5f", ((float)rand()/(float)RAND_MAX));
}
