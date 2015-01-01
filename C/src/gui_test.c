#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#define TRUE 1
#define FALSE 0

int fireState;
int keyStates[256];


typedef struct Player
{
	int x;
	int y;
	int fire_rate;
	int size;
} PLAYER;

typedef struct Projectile
{
	int x_pos;
	int y_pos;
	struct Projectile *next;
} BULLET;

PLAYER player1;
BULLET *root;

void keyOperations();

void initGL()
{
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
}

void display()
{
	keyOperations();
	glMatrixMode(GL_MODELVIEW);
	glFlush();
}

void redraw(int i)
{
	glutTimerFunc(16, redraw, 0);
	glClear(GL_COLOR_BUFFER_BIT);
	glLoadIdentity();

	glBegin(GL_QUADS);
		glColor3f(1.0f, 1.0f, 1.0f);
		glVertex2f(player1.x, (player1.y - player1.size));
		glColor3f(1.0f, 1.0f, 1.0f);
		glVertex2f((player1.x + player1.size), (player1.y - player1.size));
		glColor3f(1.0f, 1.0f, 1.0f);
		glVertex2f((player1.x + player1.size), player1.y);
		glColor3f(1.0f, 1.0f, 1.0f);
		glVertex2f(player1.x, player1.y);
	glEnd();
	
	BULLET *node;
	node = root;
	
	if(node != 0)
	{
		while(node -> next != 0)
		{
			node = node -> next;
			node -> x_pos += 10;

			glBegin(GL_QUADS);
				glColor3f(1.0f, 1.0f, 1.0f);
				glVertex2f(node -> x_pos, (node -> y_pos - 5));
				glColor3f(1.0f, 1.0f, 1.0f);
				glVertex2f((node -> x_pos + 5), (node -> y_pos - 5));
				glColor3f(1.0f, 1.0f, 1.0f);
				glVertex2f((node -> x_pos + 5), node -> y_pos);
				glColor3f(1.0f, 1.0f, 1.0f);
				glVertex2f(node -> x_pos, node -> y_pos);
			glEnd();
		}
	}
	
	glFlush();
	glutPostRedisplay();
}

void reshape(GLsizei width, GLsizei height)
{
	glClear(GL_COLOR_BUFFER_BIT);

	if (height == 0) height = 1;
	
	GLfloat aspect = (GLfloat)width / (GLfloat)height;
	glViewport(0, 0, width, height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	
	gluOrtho2D(-width, width, -height, height);
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
	if(keyStates['w'] == TRUE)
	{
		player1.y += 5;
	}
	if(keyStates['a'] == TRUE)
	{
		player1.x -= 5;
	}
	if(keyStates['s'] == TRUE)
	{
		player1.y -= 5;
	}
	if(keyStates['d'] == TRUE)
	{
		player1.x += 5;
	}
	if(keyStates['e'] == TRUE)
	{
		player1.size += 5;
	}
	if(keyStates['q'] == TRUE)
	{
		player1.size -= 5;
	}
	if(keyStates[' '] == TRUE)
	{
		if(fireState == player1.fire_rate || fireState == 0)
		{
			fireState = 0;
			BULLET *node;
			node = root;
		
			if(node != 0)
			{
				while(node -> next != 0)
				{
					node = node -> next;
				}
			}
		
			node -> next = malloc(sizeof(BULLET));
			node = node -> next;
		
			if(node == 0)
			{
				return;
			}
		
			node -> next = 0;
			node -> x_pos = player1.x + (player1.size);
			node -> y_pos = player1.y - (player1.size/2);
		}
		
		fireState ++;
	}
}

void initialise()
{
	fireState = 0;
	
	player1.x = 0;
	player1.y = 0;
	player1.fire_rate = 10;
	player1.size = 50;

	root = (BULLET *) malloc(sizeof(BULLET));
	root -> next = 0;
	root -> x_pos = 0;
	root -> y_pos = 0;
}

int main(int argc, char** argv)
{
	initialise();
	
	srand(time(NULL));
	glutInit(&argc, argv);
	glutInitWindowSize(640, 480);
	glutInitWindowPosition(50, 50);
	glutCreateWindow("Model Transform"); 
	glutDisplayFunc(display);
	glutReshapeFunc(reshape);
	glutTimerFunc(16, redraw, 0);
	glutKeyboardFunc(keyPressed);
	glutKeyboardUpFunc(keyUp);
	initGL();
	glClear(GL_COLOR_BUFFER_BIT);
	glutMainLoop();
	return 0;
}
