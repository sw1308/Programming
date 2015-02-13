#include <sys/types.h>
#include <unistd.h>
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
		if(c == 'q')
		{
			exit(0);
		}
		
		if(c == 'o')
		{
			int stringLength;
			write(1, "o was pressed\n", strlen("o was pressed\n"));
			stringLength = SEEK_END - SEEK_CUR;
			
			char *args;
			
			args = (char *) calloc(stringLength, sizeof(char));
			
			read(0, args, stringLength);
			
			write(1, args, stringLength);			
		}
	}
}
