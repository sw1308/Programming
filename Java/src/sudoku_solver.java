public class Puzzle {
	private int[][][] possibilities;
	private int[] count;
	
	public Puzzle() {
		possibilities = new int[9][9][9];
		count = new int[9];
	}
	
	public Puzzle(Puzzle parent) {
		possibilities = parent.getTable();
		count = parent.getCount();
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
	
	public setCell(int x, int y, int n) {
		for(int i=0; i<9; i++;) {
			possibilities[x][y][i] = 0;
			possibilities[i][y][n-1] = 0;
			possibilities[x][y][n-1] = 0;
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
		count[n-1]--;
	}
}

public class PuzzleTree {
	private Puzzle rootPuzzle;
	private ArrayList<PuzzleTree> leafPuzzles;
	private int currentPuzzle;
	
	public PuzzleTree() {
		rootPuzzle = new Puzzle()
		currentPuzzle = -1;
	}
	
	public PuzzleTree(Puzzle parent) {
		rootPuzzle = new Puzzle(parent);
		currentPuzzle = -1;
	}
	
	public Puzzle branch() {
		leafPuzzles.add(new Puzzle(rootPuzzle));
		currentPuzzle++;
		return leafPuzzle.get(currentPuzzle);
	}
	
	public Puzzle revert() {
		return rootPuzzle;
	}
}
