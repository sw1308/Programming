#include "GLTutorial.h"

#define NUM_OBJECTS 1
#define WINDOW_WIDTH 1366
#define WINDOW_HEIGHT 768

GLuint IBO;
GLuint VBO;
GLuint gWorldLocation;
pipeline transformationPipeline;

static void RenderScene()
{
	glClear(GL_COLOR_BUFFER_BIT);

	glEnableVertexAttribArray(0);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0);

	glDrawElements(GL_TRIANGLES, 12, GL_UNSIGNED_INT, 0);

	glutSwapBuffers();
	glDisableVertexAttribArray(0);
}

static void calculateMovements()
{
	static persProjInfo proj;
	static float scale = 0.0f;

	scale += 0.01f;
	
	if(scale > 2 * M_PI)
	{
		scale = 0.0f;
	}

	proj.FOV = 30.0f;
	proj.width = WINDOW_WIDTH;
	proj.height = WINDOW_HEIGHT;
	proj.zNear = 1.0f;
	proj.zFar = 1000.0f;

	transformationPipeline.scale(0.5f);
	transformationPipeline.worldPos(0.0f, 0.0f, 5.0f);
	transformationPipeline.rotate(0.0f, toDegree(scale), toDegree(scale));

	transformationPipeline.setPerspectiveProj(proj);

	glUniformMatrix4fv(gWorldLocation, 1, GL_TRUE, (const GLfloat*) transformationPipeline.getWPTrans());

	glutPostRedisplay();
}

static void initGlutCallBacks()
{
	glutDisplayFunc(RenderScene);
	glutIdleFunc(calculateMovements);
}

static void setUpScene()
{
	vector3f vertices[4];

	vertices[0] = vector3f(-1.0f, -1.0f, -1.0f);
	vertices[1] = vector3f(0.0f, -1.0f, 1.0f);
	vertices[2] = vector3f(1.0f, -1.0f, -1.0f);
	vertices[3] = vector3f(0.0f, 1.0f, 0.0f);

	uint indices[] = {
		0, 3, 1,
		1, 3, 2,
		2, 3, 0,
		0, 1, 2
	};

	glGenBuffers(NUM_OBJECTS, &VBO);
	glBindBuffer(GL_ARRAY_BUFFER, VBO);
	glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);

	glGenBuffers(NUM_OBJECTS, &IBO);
	glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, IBO);
	glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, GL_STATIC_DRAW);
}

static void addShader(GLuint shaderProgram, const char* pShaderText, GLenum shaderType)
{
	GLuint shaderObj = glCreateShader(shaderType);

	if(shaderObj == 0)
	{
		fprintf(stderr, "Error creating shader type: %d\n", shaderType);
		exit(0);
	}

	const GLchar* p[1];
	p[0] = pShaderText;
	GLint lengths[1];
	lengths[0] = strlen(pShaderText);
	glShaderSource(shaderObj, 1, p, lengths);
	glCompileShader(shaderObj);
	GLint success;
	glGetShaderiv(shaderObj, GL_COMPILE_STATUS, &success);

	if(!success)
	{
		GLchar infoLog[1024];
		glGetShaderInfoLog(shaderObj, 1024, NULL, infoLog);
		fprintf(stderr, "Error compiling shader type %d: %s", shaderType, infoLog);
		exit(1);
	}

	glAttachShader(shaderProgram, shaderObj);
}

static void compileShaders()
{
	const char* pVsFileName = dataFile("shader.vert");
	const char* pFsFilename = dataFile("shader.frag");

	GLuint shaderProgram = glCreateProgram();

	if(shaderProgram == 0)
	{
		fprintf(stderr, "Error creating shader program\n");
		exit(1);
	}

	string vs, fs;

	readFile(pVsFileName, vs);
	readFile(pFsFilename, fs);

	if(vs == "" || fs == "")
	{
		fprintf(stderr, "Shader not read in correctly\n");
		exit(1);
	}

	addShader(shaderProgram, vs.c_str(), GL_VERTEX_SHADER);
	addShader(shaderProgram, fs.c_str(), GL_FRAGMENT_SHADER);

	GLint success = 0;
	GLchar errorLog[1024] = {0};

	glLinkProgram(shaderProgram);
	glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);

	if(!success)
	{
		glGetProgramInfoLog(shaderProgram, sizeof(errorLog), NULL, errorLog);
		fprintf(stderr, "Error linking shader program: '%s'\n", errorLog);
		exit(1);
	}

	glValidateProgram(shaderProgram);
	glGetProgramiv(shaderProgram, GL_VALIDATE_STATUS, &success);

	if(!success)
	{
		glGetProgramInfoLog(shaderProgram, sizeof(errorLog), NULL, errorLog);
		fprintf(stderr, "Invalid shader program: '%s'\n", errorLog);
		exit(1);
	}

	glUseProgram(shaderProgram);

	gWorldLocation = glGetUniformLocation(shaderProgram, "gWorld");
	assert(gWorldLocation != 0xFFFFFFFF);
}

int main(int argc, char *argv[])
{
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA);

	glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
	glutInitWindowPosition(100, 100);
	glutCreateWindow("OpenGL Testing");

	initGlutCallBacks();

	GLenum res = glewInit();
	if(res != GLEW_OK)
	{
		fprintf(stderr, "Error: %s\n", glewGetErrorString(res));
		return 1;
	}

	printf("GL version: %s\n", glGetString(GL_VERSION));

	setUpScene();

	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);

	compileShaders();

	glutMainLoop();

	return 0;
}