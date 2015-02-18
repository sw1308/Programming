/*
 *TO COMPILE WITH GCC USE:
 * gcc src/gengine.c -o bin/gengine -lGL -lGLEW -lGLU -lglut -lm
 */
#include <math.h>
#include "math_3d.h"
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>

#define TRUE 1
#define FALSE 0
#define INC 0.01f

GLuint VBO;

void draw()
{
	glClear(GL_COLOR_BUFFER_BIT);
	
	Vector3f Vertices[1];
	Vertices[0] = Vector3f(0.0f, 0.0f, 0.0f);
	
	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(Vertices), Vertices, GL_STATIC_DRAW);
	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glDrawArrays(GL_POINTS, 0, 1);
	glDisableVertexAttribArray(0);
	
	glutSwapBuffers();
}

int main(int argc, char* argv[])
{
	GLenum res = glewInit();
	if(res != GLEW_OK)
	{
		fprintf(stderr, "Error: '%s'\n", glewGetErrorString(res));
		return 1;
	}
	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowSize(1024, 720);
	glutInitWindowPosition(50,50);
	glutCreateWindow("OpenGL Tutorial");
	glutDisplayFunc(draw);
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
	glutMainLoop();
}
