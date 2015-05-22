/*			SUDOKU SOLVER

This program aims to solve a 16x16 sudoku puzzle quickly and efficiently.

Currently the program can be summarized by taking the following steps:

while (not solved):
	while (change happens):
		fill in possibilities determined by rules of sudoku

	if (failure occurred):
		revert to parent table

	create new branch in problem tree
	switch to new branch
	fill in random cell with one of it's possible values
*/

#include<stdio.h>
#include<stdlib.h>

char complete = 0;
char changed = 1;

typedef struct TABLE
{
	unsigned int cells[16][16];
	unsigned char count[16];
} TABLE;

TABLE currentTable;

void init(int table[16][16]) {
	currentTable = table;
}

void turnOff(int cell, int x)
{
	currentTable.count[x]--; //Decrement count of value in currentTable
	changed++; //Indicate that a change to the table has happened
	return cell & !(1 << x-1);
}

//Set cell at coords to val
void setCell(char coords, char val)
{
	char i;

	for(i=0;i<16;i++)
	{
		switch val
		{
			case i:
				break;
			default:
				turnOff(cell, i);
		}
	}
}

//Code kept for applying ruleset, not currently used
/*void setCell(char coords, char val)
{
	int i;

	//Set only possibility for cell to val
	for(i=0;i<16;i++)
	{
		switch val
		{
			case i:
				break;
			default:
				currentTable.cells[coords>>4][coords&16] = turnOff(currentTable.cells[coords>>4][coords&16],i);
	}

	//Remove all val possibilities in row and column of cell
	for(i=0;i<16;i++)
	{
		switch i
		{
			case (coords>>4):
				break;
			case (coords&16):
				break;
			default:
				currentTable.cells[i][coords&16] = turnOff(currentTable.cells[i][coords&16],val);
				currentTable.cells[coords>>4][i] = turnOff(currentTable.cells[coords>>4][i],val);
		}
	}

	//Remove all val possibilities in supercell of cell
	//TODO
}*/

int main()
{
	init();

	char i;
	char j;

	while(complete < 1)
	{
		while(changeHappens > 1)
		{
			applyRules(table);
		}

		if(failed > 1)
		{
			revertTree();
			fillRandom();
		}
		else
		{
			forkTree();
			fillRandom();
		}
	}

	printf("Puzzle solved");
}
