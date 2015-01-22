#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include <sys/wait.h>


char *argv[] = { "/bin/ls"} ;

int main()
{
	int pid; int stat_loc;
	
	printf("Before the fork...\n");
	pid = fork();
	if (pid == 0)
		/* Note: execl requires 0 terminated strings for
		   program path and arguments (in this case "." for
		   current directory);
		   a NULL indicates end of (variable number) of arguments
		*/ 
		execve("/bin/ls\0", argv,  NULL);
	else	
	{	wait(&stat_loc) ;
		printf("Parent (child is %d)\n", pid);
	}
	
	/* Note parent will execute following
	   exit statement to indicate success */	
	exit(EXIT_SUCCESS) ;
}
