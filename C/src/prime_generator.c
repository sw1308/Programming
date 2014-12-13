#include <stdio.h>
#include <math.h>

#define FILEPATH "primes.txt"

int main()
{
	unsigned long long int i = 0;
	
	FILE *fp;
	fp = fopen(FILEPATH, "a+");
	
	while(fscanf(fp, "%llu", &i) != EOF);
	i++;
	
	while(1)
	{
		if(i==1)
		{
			i++;
			continue;
		}
		else if(i==2)
		{
			fprintf(fp, "%llu\n", i);
			rewind(fp);
		}
		else if((i % 2) == 0)
		{
			i++;
			continue;
		}
		else
		{
			unsigned long long int line;
		
			while(fscanf(fp, "%llu", &line) != EOF)
			{
				if(line>sqrt(i))
				{
					fprintf(fp, "%llu\n", i);
					rewind(fp);
					break;
				}
				else if(i%line==0)
				{
					break;
				}
			}
		}
		
		i++;
		
		//Reduces output to increase speed
		if(i%1000000==0)
		{
			printf("Reached milestone: %llu\n", i);
		}
	}
	
	fclose(fp);
}
