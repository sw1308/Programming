/*
 *TO COMPILE WITH GCC USE:
 * gcc src/gengine.c -o bin/gengine -lGL -lGLEW -lGLU -lglut -lm
 */
#include <GL/glew.h> //Standard header for appropriate OpenGL headers
#define GLFW_DLL
#include <GLFW/glfw3.h> //Allows cross platform usability
#include <GL/glut.h> //Useful OpenGL functions
#include <math.h>
#include <stdio.h>

//Simple TRUE and FALSE definitions
#define TRUE 1
#define FALSE 0

GLuint VBO; //Vertex Buffer Object
GLuint VCO; //Vertex Colour Object
int keyStates[256]; //Key buffer

//2D rotation
GLfloat * 2Drotatecw(GLfloat *position, GLfloat rad)
{
	int i;
	
	for(i=0; i<(sizeof(position)/sizeof(GLfloat)); i+=2)
	{
		position[i] = (position[i] * cos(rad)) + (position[i+1] * sin(rad));
		position[i+1] = (position[i+1] * cos(rad)) - (position[i] * sin(rad));
	}
	
	return position;
}

GLfloat * 2Drotateccw(GLfloat *position, GLfloat rad)
{
	int i;
	
	for(i=0; i<(sizeof(position)/sizeof(GLfloat)); i+=2)
	{
		position[i] = (position[i] * cos(rad)) - (position[i+1] * sin(rad));
		position[i+1] = (position[i+1] * cos(rad)) + (position[i] * sin(rad));
	}
	
	return position;
}

//2D translation
2Dtranslate(GLfloat *position, GLfloat x, GLfloat y)
{
	
}

//2D scale
2Dscale(GLfloat *position, GLfloat scale)
{
	
}

//2D shear
shear(GLfloat *position, GLfloat scale)
{
	
}

//Initial draw function
void draw()
{
	glutSwapBuffers();
	glClear(GL_COLOR_BUFFER_BIT);
	
	glEnableClientState(GL_VERTEX_ARRAY);
	glEnableClientState(GL_COLOR_ARRAY);
	glDrawArrays(GL_TRIANGLES, 0, 3);
	
	glLoadIdentity();
	glutSwapBuffers();
	glutPostRedisplay();
}

void redraw() {
	glutTimerFunc(16, redraw, 0); //Set up next call to redraw
	glClear(GL_COLOR_BUFFER_BIT); //Clear the screen
		
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

//Initialise callback functions
static void InitGlutCallbacks()
{
	glutDisplayFunc(draw);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	glutTimerFunc(16, redraw, 0);
	glutTimerFunc(10, keyOperations, 0);
}

//Create objects
static void CreateVertexBuffer()
{
	const GLfloat Positions[] = 
	{0.0f, 0.5f,
	-0.5f, -0.5f,
	0.5f, -0.5f};
	const GLfloat Colours[] = 
	{1.0f, 0.0f, 0.0f,
	0.0f, 1.0f, 0.0f,
	0.0f, 0.0f, 1.0f};

 	glGenBuffers(1, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, 9 * sizeof(GLfloat), Positions, GL_STATIC_DRAW);
	glFinish();
	glVertexPointer(2, GL_FLOAT, 0, (char *) NULL);
	
	glGenBuffers(1, &VCO);
	glBindBuffer(GL_ARRAY_BUFFER, VCO);
	glBufferData(GL_ARRAY_BUFFER, 9 * sizeof(GLfloat), Colours, GL_STATIC_DRAW);
	glFinish();
	glColorPointer(3, GL_FLOAT, 0, (char *) NULL);
}

//Main function
int main(int argc, char** argv)
{
	glutInit(&argc, argv);
	glutInitWindowSize(400, 400);
	glutInitWindowPosition(50, 50);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
	glutCreateWindow("OpenGL Tutorial");
	glutFullScreen();
	
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
