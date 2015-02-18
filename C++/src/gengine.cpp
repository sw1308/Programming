/*
 *TO COMPILE WITH GCC USE:
 * g++ src/gengine.cpp -o bin/gengine -lGL -lGLEW -lGLU -lglut -lm
 */

#include <stdio.h>
#include <GL/glew.h>
#include <GL/glut.h>

#include "math_3d.h"

#define TRUE 1
#define FALSE 0
#define INC 0.01f

GLuint VBO;

void draw()
{
	glClear(GL_COLOR_BUFFER_BIT);
	
	glColor3f(1.0f, 1.0f, 1.0f);
	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glDrawArrays(GL_TRIANGLES, 0, 3);
	glDisableVertexAttribArray(0);
	
	glutSwapBuffers();
}

static void InitGlutCallbacks()
{
	glutDisplayFunc(draw);
}

static void CreateVertexBuffer()
{
	Vector3f Vertices[3];
    Vertices[0] = Vector3f(-1.0f, -1.0f, 0.0f);
    Vertices[1] = Vector3f(1.0f, -1.0f, 0.0f);
    Vertices[2] = Vector3f(0.0f, 1.0f, 0.0f);

 	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(Vertices), Vertices, GL_STATIC_DRAW);
}

void CreateShader()
{
	GLuint ShaderProgram = glCreateProgram();
	GLuint ShaderObjV = glCreateShader(GL_VERTEX_SHADER);
	GLuint ShaderObjF = glCreateShader(GL_FRAGMENT_SHADER);
}

int main(int argc, char** argv)
{	
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
	glutInitWindowSize(1024, 720);
	glutInitWindowPosition(50,50);
	glutCreateWindow("OpenGL Tutorial");
	
	InitGlutCallbacks();
	
	GLenum res = glewInit();
	if(res != GLEW_OK)
	{
		fprintf(stderr, "Error: '%s'\n", glewGetErrorString(res));
		return 1;
	}
	
	CreateVertexBuffer();
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glutMainLoop();
}
