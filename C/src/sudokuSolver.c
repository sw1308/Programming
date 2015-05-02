#include<stdio.h>
#include<stdlib.h>

char complete = 0;

typedef struct TABLE
{
	unsigned int cells[16][16];
	unsigned char count[16];
} TABLE;

TABLE currentTable;

void init(int table[16][16]) {
	currentTable = table;
}

char turnOff(int cell, int x)
{
	count[x]--;
	return cell & !(1 << x-1);
}

void setCell(TABLE* t, char coords, char val)
{
	int i;
	
	for(i=0;i<16;i++)
	{
		t[coords>>4][count&16] = turnOff(t[coords>>4][count&16],i);
	}
	
	for(i=0;i<16;i++)
	{
		if(!(i==(coords>>4)))
		{
			t[i][coords&16] = turnOff(t[i][coords&16], val);
		}
		
		if(!(i==(coords&16)))
		{
			t[coords>>4][i] = turnOff(t[coords>>4][i], val);
		}
	}
	
	//TODO account for supercell
}

int main()
{
	init();
	
	char i;
	char j;
	
	while(complete < 1)
	{
		for(i=1;i<17;i++)
		{
			for(j=0;j<16;j++)
			{
				char check = check4SingleRow(i,j);
				
				if(check>0)
				{
					setCell(currentTable, (check << 4)+j, i);
				}
			}
		}
	}
	
	printf("Puzzle solved");
}