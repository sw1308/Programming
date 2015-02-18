/*
 *TO COMPILE WITH GCC USE:
 * gcc src/colorTest.c -o bin/colorTest -lGL -lGLU -lglut -lm
 */
#include <math.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

#define TRUE 1
#define FALSE 0
#define INC 0.01f

int rComplete[4], bComplete[4], gComplete[4], factor;
int keyStates[256];
float r[4], g[4], b[4];
float v[4][3];

void draw()
{
	glutSwapBuffers();
	glClear(GL_COLOR_BUFFER_BIT);
	glLoadIdentity();
	glFlush();
	glutPostRedisplay();
}

void generateV(int i)
{
	v[i][0] = (float) rand()/(float)RAND_MAX;
	v[i][1] = (float) rand()/(float)RAND_MAX;
	v[i][2] = (float) rand()/(float)RAND_MAX;
	v[i][0] = roundf(v[i][0] * factor) / factor;
	v[i][1] = roundf(v[i][1] * factor) / factor;
	v[i][2] = roundf(v[i][2] * factor) / factor;
}

void redraw()
{
	glutTimerFunc(16, redraw, 0);
	
	glClear(GL_COLOR_BUFFER_BIT || GL_DEPTH_BUFFER_BIT);
	
	int i;
	
	for(i=0; i<4; i++)
	{
		if(r[i] > v[i][0])
		{
			r[i] -= INC;
		}
		else if(r[i] < v[i][0])
		{
			r[i] += INC;
		}
		else
		{
			rComplete[i] = TRUE;
		}
	
		if(g[i] > v[i][1])
		{
			g[i] -= INC;
		}
		else if(g[i] < v[i][1])
		{
			g[i] += INC;
		}
		else
		{
			gComplete[i] = TRUE;
		}
	
		if(b[i] > v[i][2])
		{
			b[i] -= INC;
		}
		else if(b[i] < v[i][2])
		{
			b[i] += INC;
		}
		else
		{
			bComplete[i] = TRUE;
		}
	
		r[i] = roundf(r[i] * 100) / 100;
		g[i] = roundf(g[i] * 100) / 100;
		b[i] = roundf(b[i] * 100) / 100;
	
		if(rComplete[i] == TRUE && gComplete[i] == TRUE && bComplete[i] == TRUE)
		{
			generateV(i);
			rComplete[i] = FALSE;
			gComplete[i] = FALSE;
			bComplete[i] = FALSE;
		}
	}
	
	glBegin(GL_QUADS);
		glColor3f(r[0], g[0], b[0]);
		glVertex2f(-1.0f, -1.0f);
		glColor3f(r[1], g[1], b[1]);
		glVertex2f(-1.0f, 1.0f);
		glColor3f(r[2], g[2], b[2]);
		glVertex2f(1.0f, 1.0f);
		glColor3f(r[3], g[3], b[3]);
		glVertex2f(1.0f, -1.0f);
	glEnd();
	
	glutSwapBuffers();
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
	srand(time(NULL));
	gluOrtho2D(-1.0f, -1.0f, 1.0f, 1.0f);
	
	factor = 1 / INC;
	
	int i;
	
	for(i=0; i<4; i++)
	{
		r[i] = 1.0f;
		g[i] = 0.0f;
		b[i] = 0.0f;
		rComplete[i] = FALSE;
		gComplete[i] = FALSE;
		bComplete[i] = FALSE;
	}
	
	for(i=0; i<4; i++)
	{
		generateV(i);
	}
}

int main(int argc, char** argv)
{
	init();
	glutInit(&argc, argv);
	srand(time(NULL));
	glutInitWindowSize(640, 480);
	glutInitWindowPosition(50,50);
	glutInitDisplayMode(GLUT_DOUBLE);
	glutCreateWindow("OpenGL");
	glutFullScreen();
	glutDisplayFunc(draw);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	glutTimerFunc(16, redraw, 0);
	glutTimerFunc(10, keyOperations, 0);
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	
	glutMainLoop();
	
	return 0;
}
