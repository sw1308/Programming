#include <stdio.h>
#include <string>
#include <string.h>
#include <GL/glew.h>
#include <GL/freeglut.h>

#include "utils.h"
#include "math_3d.h"
#include "pipeline.h"

#ifndef WIN32
#define dataFile(filename) ("../../dat/GLTutorial/"filename)
#else
#define dataFile(filename) ("..\\..\\dat\\GLTutorial\\"filename)
#endif /* ndef WIN32 */