#include <stdio.h>
#include <math.h>

#define FILEPATH "primes.txt"

int main()
{
	int i = 1;
	int isPrime;
	
	FILE *fa;
	fa = fopen(FILEPATH, "a");
	
	while(1)
	{
		if(checkPrime(i) == 1)
		{
			fprintf(fa, "%d\n", i);
			printf("Found prime: %d\n", i);
		}
		
		i++;
	}
	
	fclose(fa);
}

int checkPrime(int i)
{
	if(i==2)
	{
		return 1;
	}
	else if((i % 2) == 0)
	{
		return 0;
	}
	else
	{
		int line;
		
		FILE *fw;
		fw = fopen(FILEPATH, "r");
		
		while(fscanf(fw, "%d", &line) && (line<sqrt(i)))
		{
			if(i%line==0)
			{
				return 0;
			}
		}
		
		fclose(fw);
		
		return 1;
	}
}
