#ifndef UTIL_H
#define UTIL_H

#ifndef WIN32
#include <unistd.h>
#endif

#include <cstring>
#include <string>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>

#include "types.h"

using namespace std;

#ifndef WIN32
#include <unistd.h>
#define getCurrentDir getcwd
#else
#include <direct.h>
#define getCurrentDir _getcwd
#endif /* ndef WIN32 */

bool readFile(const char* filename, string& output);

void utilError(const char* pFileName, uint line, const char* pError);
void fileError(const char* pFileName, uint line, const char* pFileError);

#define UTIL_ERROR(error) utilError(__FILE__, __LINE__, error);
#define FILE_ERROR(pFileError) fileError(__FILE__, __LINE__, pFileError);

#define ZERO_MEM(a) memset(a, 0, sizeof(a));
#define ARRAY_SIZE_IN_ELEMENTS(a) (sizeof(a)/sizeof(a)[0]);

#ifdef WIN32

#define SNPRINTF _snprintf_s
#define RANDOM rand
#define SRANDOM srand((unsigned)time(NULL))
float fmax(float a, float b);

#else

#define SNPRINTF snprintf
#define RANDOM random
#define SRANDOM srandom(getpid())

#endif /* def WIN32 */

#define INVALID_UNIFORM_LOCATION 0xffffffff
#define INVALID_OGL_VALUE 0xffffffff

#define SAFE_DELETE(p) if (p) {delete p; p=NULL;}

#define GL_EXIT_IF_ERROR															\
{																					\
	GLenum error = glGetError();													\
	if(error != GL_NO_ERROR)														\
	{																				\
		fprintf(stderr, "OpenGL error in %s:%d 0x%x\n", __FILE__, __LINE__, error);	\
		exit(0);																	\
	}																				\
}

#define GL_CHECK_ERROR() (glGetError() == GL_NO_ERROR)

long long getCurrentTimeMillis();

#endif /* ndef UTIL_H */