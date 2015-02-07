#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>

int main(int argc, char *argv[])
{
	int fd;
	char c;
	
	printf("This");
	
	while(read(0, &c, 1) == 1)
	{
		if(c == 'o')
		{
			char *name;
			
			name = (char *) calloc(128, sizeof(char));
			
			while(read(0, &c, 1) == 1)
			{
				strcat(name, &c);
			}
			
		}
		else if(c == 'q')
		{
			close(fd);
			exit(0);
		}
		else
		{
			printf("Please enter o or q");
		}
	}
}
