#include <math.h>

void add(int row, int col, GLfloat ** matrix1, GLfloat ** matrix2)
{
	int i, j;
	
	for(i=0; i<row; i++)
	{
		for(j=0; j<col; j++)
		{
			matrix1[i][j] = matrix1[i][j] + matrix2[i][j];
		}
	}
}

void transpose(int m, int n, GLfloat ** matrix, GLfloat ** returnMatrix)
{
	int i, j;
	
	for(i=0; i<m; i++)
	{
		for(j=0; j<n; j++)
		{
			returnMatrix[j][i] = matrix[i][j];
		}
	}
}

void multByFactor(int row, int col, GLfloat ** matrix, GLfloat factor)
{
	int i, j;
	
	for(i=0; i<row; i++)
	{
		for(j=0; j<col; j++)
		{
			matrix[row][col] = matrix[row][col] * factor;
		}
	}
}

void multByVector(int n, int p, GLfloat vector[n], GLfloat matrix[n][p], GLfloat returnMatrix[p])
{
	int j;
	int k;
	
	for(j=0; j<p; j++)
	{
		GLfloat result = 0.0f;
	
		for(k=0; k<n; k++)
		{
			result += vector[k] * matrix[k][j];
		}
	
		returnMatrix[j] = result;
	}
}

void multByMatrix(int m, int n, int p, GLfloat matrix1[m][n], GLfloat matrix2[n][p], GLfloat returnMatrix[m][p])
{
	int i;
	int j = 0;
	int k;
	
	for(i=0; i<m; i++)
	{
		GLfloat result = 0.0f;
		
		for(k=0; k<n; k++)
		{
			result += matrix1[i][k] * matrix2[k][j];
		}
		
		returnMatrix[i][j] = result;
		
		j++;
	}
}
