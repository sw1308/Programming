#include <stdio.h>

double ack(double m, double n)
{
	if (m == 0.0l) return n + 1.0l;
	else if (n == 0.0l) return ack(m - 1.0l, 1.0l);
	else return ack(m - 1.0l, ack(m, n - 1.0l));
}

int main(int argc, char const *argv[])
{
	for(double i=0.0l; i<6.0l; i++)
	{
		for(double j=0.0l; j<6.0l; j++)
		{
			printf("Ackerman(%lf, %lf): %lf\n", i, j, ack(i, j));
		}
	}
	return 0;
}