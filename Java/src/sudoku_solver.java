import java.util.ArrayList;

class sudoku_solver {
	public static void main(String[] args) {
		Puzzle currentPuzzle = new Puzzle(9);
		currentPuzzle.setCell(0,0,5);
		currentPuzzle.setCell(1,0,1);
		currentPuzzle.setCell(4,0,2);
		currentPuzzle.setCell(6,0,9);
		currentPuzzle.setCell(1,1,7);
		currentPuzzle.setCell(3,1,5);
		currentPuzzle.setCell(5,1,9);
		currentPuzzle.setCell(6,1,8);
		currentPuzzle.setCell(5,2,8);
		currentPuzzle.setCell(8,2,2);
		currentPuzzle.setCell(1,3,3);
		currentPuzzle.setCell(6,3,6);
		currentPuzzle.setCell(8,3,8);
		currentPuzzle.setCell(1,4,9);
		currentPuzzle.setCell(3,4,7);
		currentPuzzle.setCell(5,4,1);
		currentPuzzle.setCell(7,4,4);
		currentPuzzle.setCell(0,5,2);
		currentPuzzle.setCell(2,5,4);
		currentPuzzle.setCell(7,5,3);
		currentPuzzle.setCell(0,6,6);
		currentPuzzle.setCell(3,6,9);
		currentPuzzle.setCell(2,7,1);
		currentPuzzle.setCell(3,7,3);
		currentPuzzle.setCell(5,7,2);
		currentPuzzle.setCell(7,7,6);
		currentPuzzle.setCell(2,8,9);
		currentPuzzle.setCell(4,8,4);
		currentPuzzle.setCell(7,8,8);
		currentPuzzle.setCell(8,8,1);
		
		System.out.println("Valid input puzzle? " + currentPuzzle.isValid());
		
		PuzzleTree problem = new PuzzleTree(currentPuzzle);
		
		while(!currentPuzzle.isSolved()) {
			currentPuzzle = problem.branch();
			
		}
	}
}

class Puzzle {
	private int[][][] possibilities;
	private int[] count;
	private int[][] density;
	private int size;
	private boolean solved;
	
	public Puzzle(int size) {
		this.size = size;
		possibilities = new int[size][size][size];
		density = new int[size][size];
		count = new int[size];
		
		for(int x=0; x<size; x++) {
			for(int y=0; y<9; y++) {
				for(int z=0; z<size; z++) {
					possibilities[x][y][z] = 1;
				}
				density[x][y] = 4;
			}
			count[x] = 9;
		}
		
		solved = false;
	}
	
	public Puzzle(Puzzle parent) {
		this.size = parent.getSize();
		possibilities = parent.getTable();
		count = parent.getCount();
		solved = parent.isSolved();
	}
	
	public int getSize() {
		return this.size;
	}
	
	public boolean isSolved() {
		return this.solved;
	}
	
	public int[][][] getTable() {
		return possibilities;
	}
	
	public int[] getCount() {
		return count;
	}
	
	public int getCount(int request) {
		return count[request-1];
	}
	
	public void setCell(int x, int y, int n) {
		for(int i=0; i<size; i++) {
			possibilities[x][y][i] = 0;
			possibilities[i][y][n-1] = 0;
			possibilities[x][i][n-1] = 0;
		}
		
		int lowerX, lowerY, upperX, upperY;

		if(x<3) {
			lowerX = 0;
			upperX = 3;
		} else if(x<6) {
			lowerX = 3;
			upperX = 6;
		} else {
			lowerX = 6;
			upperX = 9;
		}
		
		if(y<3) {
			lowerY = 0;
			upperY = 3;
		} else if(x<6) {
			lowerY = 3;
			upperY = 6;
		} else {
			lowerY = 6;
			upperY = 9;
		}
		
		for(int i=lowerX; i<upperX; i++) {
			for(int j=lowerY; j<upperY; j++) {
				possibilities[i][j][n-1] = 0;
			}
		}
		
		possibilities[x][y][n-1] = 1;
		density[x][y]--;
		count[n-1]--;
		
		for(int i=0; i<size; i++) {
			if(count[i] > 0) {
				return;
			}
		}
		
		solved = true;
	}
	
	public String toString() {
		String returnString = " ||-------------------------------------||\n";
		boolean singular = false;
		int cell = 0;
		
		for(int y=0; y<size; y++) {
			for(int x=0; x<size; x++) {
				for(int z=0; z<size; z++) {
					if(possibilities[x][y][z] == 1) {
						if(singular) {
							singular = false;
							break;
						}
						singular = true;
						cell = z+1;	
					}
				}
				
				String sep = " | ";
				
				if(x%Math.sqrt(size) == 0) {
					sep = " || ";
				}
				
				if(singular) {
					returnString = returnString + sep + cell;
				} else {
					returnString = returnString + sep +" ";
				}
				
				singular = false;
			}
			if((y+1)%Math.sqrt(size) == 0) {
				returnString = returnString + " ||\n ||-------------------------------------||\n";
			} else {
				returnString = returnString + " ||\n";
			}
		}
		
		return returnString;
	}
	
	public boolean isValid() {
		for(int x=0; x<size; x++) {
			for(int y=0; y<size; y++) {
				if(density[x][y] == 0) {
					return false;
				}
			}
		}
		
		return true;
	}
}

class PuzzleTree {
	private Puzzle rootPuzzle;
	private ArrayList<PuzzleTree> leafPuzzles;
	private int currentPuzzle;
	
	public PuzzleTree(int size) {
		rootPuzzle = new Puzzle(size);
		currentPuzzle = -1;
	}
	
	public PuzzleTree(Puzzle parent) {
		rootPuzzle = new Puzzle(parent);
		currentPuzzle = -1;
	}
	
	public Puzzle getRoot() {
		return rootPuzzle;
	}
	
	public Puzzle branch() {
		leafPuzzles.add(new PuzzleTree(rootPuzzle));
		currentPuzzle++;
		return leafPuzzles.get(currentPuzzle).getRoot();
	}
	
	public Puzzle revert() {
		return rootPuzzle;
	}
}
