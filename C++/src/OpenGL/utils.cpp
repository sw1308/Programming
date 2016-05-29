#include <iostream>
#include <fstream>

#ifdef WIN32
#include <Windows.h>
#else
#include <sys/time.h>
#endif /* def WIN32 */

#include "utils.h"

bool readFile(const char* filename, string& output)
{
	ifstream f(filename);

	if(f.is_open())
	{
		string line;

		while(getline(f, line))
		{
			output.append(line);
			output.append("\n");
		}

		f.close();
	}
	else
	{
		printf("could not open file\n");
		return false;
	}

	return true;
}

void utilError(const char* pFileName, uint line, const char* pError)
{
#ifdef WIN32
	char msg[1000];
	SNPRINTF(msg, sizeof(msg), "%s:%d %s", pFileName, line, pError);
	MessageBoxA(NULL, msg, NULL, 0);
#else
	fprintf(stderr, "%s:%d %s\n", pFileName, line, pError);
#endif /* def WIN32 */
}

void fileError(const char* pFileName, uint line, const char* pFileError)
{
#ifdef WIN32
	char msg[1000];
	SNPRINTF(msg, sizeof(msg), "%s:%d unable to open file '%s'", pFileName, line, pFileError);
	MessageBoxA(NULL, msg, NULL, 0);
#else
	fprintf(stderr, "%s:%d unable to open file '%s'\n", pFileName, line, pFileError);
#endif /* def WIN32 */
}

long long getCurrentTimeMillis()
{
#ifdef WIN32
	return GetTickCount();
#else
	timeval t;
	gettimeofday(&t, NULL);

	long long ret = t.tv_sec * 1000 + t.tv_usec / 1000;
	return ret;
#endif
}

#ifdef WIN32
#if _MSC_VER != 1800
float fmax(float a, float b)
{
	if(a>b)
	{
		return a;
	} else {
		return b;
	}
}
#endif /* _MSC_VER != 1800 */
#endif /* def WIN32 */