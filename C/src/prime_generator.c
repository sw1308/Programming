#include <stdio.h>
#include <math.h>

#define FILEPATH "primes.txt"

int main()
{
	int i = 0;
	int isPrime;
	
	FILE *fp;
	fp = fopen(FILEPATH, "a+");
	
	while(fscanf(fp, "%d", &i) != EOF);
	rewind(fp);
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
			fprintf(fp, "%d\n", i);
			rewind(fp);
		}
		else if((i % 2) == 0)
		{
			i++;
			continue;
		}
		else
		{
			int line;
		
			while(fscanf(fp, "%d", &line) != EOF)
			{
				if(line>sqrt(i))
				{
					fprintf(fp, "%d\n", i);
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
		
		if(i%1000000==0)
		{
			printf("Reached milestone: %d\n", i);
		}
	}
	
	fclose(fp);
}
