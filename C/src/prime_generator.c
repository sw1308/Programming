// Compile with
// gcc -o bin/prime_generator -v -O3 src/prime_generator.c -lm
// from the Programming/C/ path

#include <stdio.h>
#include <math.h>

#define FILEPATH "dat/primes.txt"

int main()
{
	// Initialise the variables to be used in computation, unsigned long long
	// int's were chosen as they can represent the largest numbers without
	// needing to write new classes
	unsigned long long int i = 0;
	unsigned long long int found = 0;
	unsigned long long int maxVal = 0;
	unsigned long long int* max = &maxVal;

	// Create a file pointer and open it for appending and reading
	FILE *fp;
	fp = fopen(FILEPATH, "a+");

	// This allows the user to define the highest numbered prime to search for
	// before terminating the program
	printf("\nPlease enter the max number of primes to find: ");
	scanf("%llu", max);

	// Scan to the end of the file in order to assess the largest previously
	// found prime number, saves on computation time for extremely large limits
	while(fscanf(fp, "%llu", &i) != EOF) {found++;}
	rewind(fp);
	i++;

	// This is the main while loop of the program, where all of the functional
	// computations take place
	while(found < maxVal)
	{
		// Ignore 1, it's not a prime
		if(i==1)
		{
			i++;
			continue;
		}
		// If the program is running for the first time it will need a starting
		// point to serve as a reference point for the rest of the computations
		else if(i==2)
		{
			fprintf(fp, "%llu\n", i); // Add the "found" prime number to the file
 			found++;
			rewind(fp);
		}
		else
		{
			unsigned long long int line;

			// Scan through the file and for each prime number found that is less
			// than the current number being tested, find out if it is a factor
			// or not.
			while(fscanf(fp, "%llu", &line) != EOF)
			{
				if(line>sqrt(i))
				{
					fprintf(fp, "%llu\n", i);
					found++;
					rewind(fp);
					break;
				}
				else if(i%line==0)
				{
					rewind(fp);
					break;
				}
			}
		}

		i++;

		//Reduces output to increase speed
		if(i%1000000==0)
		{
			printf("Reached milestone: %llu\n", i);
			printf("Found: %llu\n", found);
		}
	}

	fclose(fp);
}
