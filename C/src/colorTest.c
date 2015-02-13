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

int colorCase, rComplete, bComplete, gComplete;
int keyStates[256];
float r, g, b;
float v[3];

void draw()
{
	glutSwapBuffers();
	glClear(GL_COLOR_BUFFER_BIT);
	glLoadIdentity();
	glFlush();
	glutPostRedisplay();
}

void generateV()
{
	v[0] = (float) rand()/(float)RAND_MAX;
	v[1] = (float) rand()/(float)RAND_MAX;
	v[2] = (float) rand()/(float)RAND_MAX;
	v[0] = roundf(v[0] * 100) / 100;
	v[1] = roundf(v[1] * 100) / 100;
	v[2] = roundf(v[2] * 100) / 100;
}

/*void redraw()*/
/*{*/
/*	glutTimerFunc(16, redraw, 0);*/
/*	*/
/*	switch(colorCase)*/
/*	{*/
/*		case 0:*/
/*			if(r > g)*/
/*			{*/
/*				g += 0.01f;*/
/*			}*/
/*			else if (r > 0.0f)*/
/*			{*/
/*				r -= 0.01f;*/
/*			}*/
/*			else*/
/*			{*/
/*				colorCase = 1;*/
/*			}*/
/*			break;*/
/*		case 1:*/
/*			if(g > b)*/
/*			{*/
/*				b += 0.01f;*/
/*			}*/
/*			else if (g > 0.0f)*/
/*			{*/
/*				g -= 0.01f;*/
/*			}*/
/*			else*/
/*			{*/
/*				colorCase = 2;*/
/*			}*/
/*			break;*/
/*		case 2:*/
/*			if (b > r)*/
/*			{*/
/*				r += 0.01f;*/
/*			}*/
/*			else if (b > 0.0f)*/
/*			{*/
/*				b -= 0.01f;*/
/*			}*/
/*			else*/
/*			{*/
/*				colorCase = 0;*/
/*			}*/
/*			break;*/
/*		default:*/
/*			r = 1.0f;*/
/*			g = 0.0f;*/
/*			b = 0.0f;*/
/*			colorCase = 0;*/
/*	}*/
/*	*/
/*	glClearColor(r, g, b, 1.0f);*/
/*	*/
/*	glClear(GL_COLOR_BUFFER_BIT);*/
/*	*/
/*	glFlush();*/
/*	glutPostRedisplay();*/
/*}*/

void redraw()
{
	glutTimerFunc(16, redraw, 0);
	
	if(r > v[0])
	{
		r -= INC;
	}
	else if(r < v[0])
	{
		r += INC;
	}
	else
	{
		rComplete = TRUE;
	}
	
	if(g > v[1])
	{
		g -= INC;
	}
	else if(g < v[1])
	{
		g += INC;
	}
	else
	{
		gComplete = TRUE;
	}
	
	if(b > v[2])
	{
		b -= INC;
	}
	else if(b < v[2])
	{
		b += INC;
	}
	else
	{
		bComplete = TRUE;
	}
	
	r = roundf(r * 100) / 100;
	g = roundf(g * 100) / 100;
	b = roundf(b * 100) / 100;
	
	printf("r: %f g: %f b: %f v: %f, %f, %f\n", r, g, b, v[0], v[1], v[2]);
	
	if(rComplete == TRUE && gComplete == TRUE && bComplete == TRUE)
	{
		generateV();
		rComplete = FALSE;
		gComplete = FALSE;
		bComplete = FALSE;
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
	srand(time(NULL));
	r = 1.0f;
	g = 0.0f;
	b = 0.0f;
	colorCase = 0;
	rComplete = FALSE;
	gComplete = FALSE;
	bComplete = FALSE;
	generateV();
}

int main(int argc, char** argv)
{
	init();
	glutInit(&argc, argv);
	srand(time(NULL));
	glutInitWindowSize(640, 480);
	glutInitWindowPosition(50,50);
	glutCreateWindow("OpenGL");
	glutFullScreen();
	glutDisplayFunc(draw);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	glutTimerFunc(16, redraw, 0);
	glutTimerFunc(10, keyOperations, 0);
	glClearColor(r, g, b, 1.0f);
	
	glutMainLoop();
	
	return 0;
}
