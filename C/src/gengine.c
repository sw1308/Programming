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

GLfloat Positions[] = 
	{0.0f, 0.5f,
	-0.5f, -0.5f,
	0.5f, -0.5f}; //Array of vertices
GLfloat Colours[] = 
	{1.0f, 0.0f, 0.0f,
	0.0f, 1.0f, 0.0f,
	0.0f, 0.0f, 1.0f}; //Array of colours
	
int keyStates[256]; //Key buffer
GLuint vao, vbo[2];

void rotate2DCW(GLfloat *vertices, GLfloat theta)
{
	
}

//Initial draw function
void draw()
{
	glClear(GL_COLOR_BUFFER_BIT);
	
	glDrawArrays(GL_TRIANGLES, 0, 3);
	
	glLoadIdentity();
	glutSwapBuffers();
	glutPostRedisplay();
}

void redraw()
{
	glClear(GL_COLOR_BUFFER_BIT); //Clear the screen
	
	glDrawArrays(GL_TRIANGLES, 0, 3);
	
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
	if (keyStates['a'] == TRUE)
	{
		glutTimerFunc(100, redraw, 0); //Set up next call to redraw
		keyStates['a'] = FALSE;
	}
}

//Initialise callback functions
static void InitGlutCallbacks()
{
	glutDisplayFunc(draw);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	glutTimerFunc(100, redraw, 0);
	glutTimerFunc(10, keyOperations, 0);
}

char * filetobuff(const char *file)
{
	FILE *fptr;
    long length;
    char *buf;
 
    fptr = fopen(file, "rb"); /* Open file for reading */
    
    if (!fptr) /* Return NULL on failure */
    {
    	return NULL;
    }
    
    fseek(fptr, 0, SEEK_END); /* Seek to the end of the file */
    length = ftell(fptr); /* Find out how many bytes into the file we are */
    buf = (char*)malloc(length+1); /* Allocate a buffer for the entire length of the file and a null terminator */
    fseek(fptr, 0, SEEK_SET); /* Go back to the beginning of the file */
    fread(buf, length, 1, fptr); /* Read the contents of the file in to the buffer */
    fclose(fptr); /* Close the file */
    buf[length] = 0; /* Null terminator */
 
    return buf; /* Return the buffer */
}

GLuint CreateShader(GLenum eShaderType, const char* strShaderFile)
{
	GLuint shader = glCreateShader(eShaderType);
	
	GLchar *shaderSource = filetobuff(strShaderFile);
	
	glShaderSource(shader, 1, (const char **) &shaderSource, 0);
	
	glCompileShader(shader);
	
	GLint status;
	glGetShaderiv(shader, GL_COMPILE_STATUS, &status);
	
	if(status == GL_FALSE)
	{
		GLint infoLogLength;
		glGetShaderiv(shader, GL_INFO_LOG_LENGTH, &infoLogLength);
		
		GLchar strInfoLog[infoLogLength + 1];
		glGetShaderInfoLog(shader, infoLogLength, NULL, strInfoLog);
		
		const char *strShaderType = NULL;
		switch(eShaderType)
		{
			case GL_VERTEX_SHADER: strShaderType = "vertex"; break;
			case GL_GEOMETRY_SHADER: strShaderType = "geometry"; break;
			case GL_FRAGMENT_SHADER: strShaderType = "fragment"; break;
		}
		
		fprintf(stderr, "Compile failure in %s shader:\n%s\n", strShaderType, strInfoLog);
		free(strInfoLog);
		return;
	}
	
	return shader;
}

void CreateProgram(const GLuint shaderList[])
{
	int i;
	GLuint shaderProgram = glCreateProgram();
	
	for(i=0; i<sizeof(shaderList)/sizeof(shaderList[0]); i++)
	{
		glAttachShader(shaderProgram, shaderList[i]);
	}
	
	glBindAttribLocation(shaderProgram, 0, "position");
	glBindAttribLocation(shaderProgram, 1, "colour");
	
	glLinkProgram(shaderProgram);
	
	GLuint status;
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &status);
	
	if(status = GL_FALSE)
	{
		GLint infoLogLength;
		glGetProgramiv(shaderProgram, GL_INFO_LOG_LENGTH, &infoLogLength);
		
		GLchar strInfoLog[infoLogLength + 1];
		glGetProgramInfoLog(shaderProgram, infoLogLength, NULL, strInfoLog);
		fprintf(stderr, "Linker failure: %s\n", strInfoLog);
		free(strInfoLog);
		return;
	}
	
	glUseProgram(shaderProgram);
}

void InitializeProgram()
{
	GLuint shaderList[2];
	
	shaderList[0] = CreateShader(GL_FRAGMENT_SHADER, "dat/gengine.frag");
	shaderList[1] = CreateShader(GL_VERTEX_SHADER, "dat/gengine.vert");
	
	CreateProgram(shaderList);
}

void CreateBuffers()
{
	glGenVertexArrays(1, &vao);
	glBindVertexArray(vao);
	glGenBuffers(2, vbo);
	
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, 6*sizeof(GLfloat), Positions, GL_STREAM_DRAW);
	glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(0);
	
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, 9*sizeof(GLfloat), Colours, GL_STATIC_DRAW);
	glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, 0);
	glEnableVertexAttribArray(1);
}

//Main function
int main(int argc, char** argv)
{	
	glutInit(&argc, argv);
	glutInitWindowSize(400, 400);
	glutInitWindowPosition(50, 50);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);
	glutCreateWindow("OpenGL Tutorial");
	//glutFullScreen();
	
	InitGlutCallbacks();
	
	GLenum res = glewInit();
	if(res != GLEW_OK)
	{
		fprintf(stderr, "Error: '%s'\n", glewGetErrorString(res));
		return 1;
	}
	
	InitializeProgram();
	
	CreateBuffers();
	
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glutMainLoop();
}
