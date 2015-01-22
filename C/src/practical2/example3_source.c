#include<stdio.h>
#include<stdlib.h>

int main()
{
	int pid;
	
	printf("Before the fork...\n");
	pid = fork();
	if (pid == 0)
		printf("Child\n");
	else	printf("Parent (child is %d)\n", pid);
	
	/* Note both child and parent will execute following
	   exit statement to indicate success */	
	exit(EXIT_SUCCESS) ;
}
