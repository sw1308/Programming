#include <stdio.h>
#include <math.h>

#define FILEPATH "primes.txt"

int main()
{
	unsigned long long int i = 0;
	unsigned long long int found = 0;
	unsigned long long int maxVal = 0;
	unsigned long long int* max = &maxVal;
	
	FILE *fp;
	fp = fopen(FILEPATH, "a+");
	
	printf("\nPlease enter the max number of primes to find: ");
	scanf("%llu", max);
	
	while(fscanf(fp, "%llu", &i) != EOF) {found++;}
	rewind(fp);
	i++;
	
	
	while(found < maxVal)
	{
		if(i==1)
		{
			i++;
			continue;
		}
		else if(i==2)
		{
			fprintf(fp, "%llu\n", i);
			found++;
			rewind(fp);
		}
		else
		{
			unsigned long long int line;
		
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
