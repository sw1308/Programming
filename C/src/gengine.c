#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

void init(int width, int height, char *windowTitle)
{
	
}

int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	srand(time(NULL));
	glutInitWindowSize(width, height);
	glutInitWindowPosition(50,50)
	glutCreateWindow(windowTitle);
}
