/*
 *TO COMPILE WITH GCC USE:
 * gcc src/colorTest.c -o bin/colorTest -lGL -lGLU -lglut
 */
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

#define TRUE 1
#define FALSE 0

int colorCase;
int keyStates[256];
float r, g, b;

void draw()
{
	glutSwapBuffers();
	glClear(GL_COLOR_BUFFER_BIT);
	glLoadIdentity();
	glFlush();
	glutPostRedisplay();
}

void redraw()
{
	glutTimerFunc(16, redraw, 0);
	
	switch(colorCase)
	{
		case 0:
			if(r > g)
			{
				g += 0.01f;
			}
			else if (r > 0.0f)
			{
				r -= 0.01f;
			}
			else
			{
				colorCase = 1;
			}
			break;
		case 1:
			if(g > b)
			{
				b += 0.01f;
			}
			else if (g > 0.0f)
			{
				g -= 0.01f;
			}
			else
			{
				colorCase = 2;
			}
			break;
		case 2:
			if (b > r)
			{
				r += 0.01f;
			}
			else if (b > 0.0f)
			{
				b -= 0.01f;
			}
			else
			{
				colorCase = 0;
			}
			break;
		default:
			r = 1.0f;
			g = 0.0f;
			b = 0.0f;
			colorCase = 0;
	}
	
	glClearColor(r, g, b, 1.0f);
	
	glClear(GL_COLOR_BUFFER_BIT);
	
	glFlush();
	glutPostRedisplay();
}

void keyPressed(unsigned char key, int x, int y)
{
	keyStates[key] = TRUE;
}

void keyUp(unsigned char key, int x, int y)
{
	keyStates[key] = FALSE;
}

void keyOperations()
{
	glutTimerFunc(10, keyOperations, 0);
	
	if (keyStates['q'] == TRUE)
	{
		exit(0);
	}
}

void init()
{
	r = 1.0f;
	g = 0.0f;
	b = 0.0f;
	colorCase = 0;
}

int main(int argc, char** argv)
{
	init();
	glutInit(&argc, argv);
	srand(time(NULL));
	glutInitWindowSize(640, 480);
	glutInitWindowPosition(50,50);
	glutCreateWindow("OpenGL");
//	glutFullScreen();
	glutDisplayFunc(draw);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	glutTimerFunc(16, redraw, 0);
	glutTimerFunc(10, keyOperations, 0);
	glClearColor(r, g, b, 1.0f);
	
	glutMainLoop();
	
	return 0;
}
