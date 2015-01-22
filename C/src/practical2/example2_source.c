#include<stdio.h>
#include<stdlib.h>

int main()
{
	printf("Before the fork...\n");
	fork();
	printf("After the fork... \n");
	
	/* Both child and parent will execute following
	  exit statement to indicate success */	
	exit(EXIT_SUCCESS) ;
}
