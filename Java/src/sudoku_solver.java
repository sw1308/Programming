import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;
import java.util.LinkedList;
import java.io.IOException;
import java.io.FileReader;
import java.io.BufferedReader;

class sudoku_solver {
	private static Puzzle currentPuzzle;
	private static PuzzleTree problem;
	private static int size;
	
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.print("Please enter the size (width) of the puzzle: ");
		size = sc.nextInt();
		System.out.print("Please enter the file path for the puzzle text file: ");
		String filePath = sc.next();
		currentPuzzle = new Puzzle(size);
		
		try {
			parsePuzzle(filePath);
		} catch(IOException e) {
			System.out.println("You moron, the file doesn't exist.");
			System.exit(0);
		}
		
		System.out.println("Valid input puzzle? " + currentPuzzle.isValid());
		
		if(!currentPuzzle.isValid()) {
			System.out.println("Input not valid, shutting down.");
			return;
		}
		
		problem = new PuzzleTree(currentPuzzle);
		
		while(!currentPuzzle.isSolved()) {
			boolean changeHappens = true;
			int superCell = (int) Math.sqrt(size);
			while(changeHappens) {
				changeHappens = false;
				
				for(int z=0; z<size; z++) {
					for(int x=0; x<size; x++) {
						int instances = 0;
						int yInstance = 9;
						for(int y=0; y<size; y++) {
							if(currentPuzzle.getTable()[x][y][z] == 1 && currentPuzzle.getDensity()[x][y] > 1) {
								instances++;
								yInstance = y;
							}
						}
						
						if(instances == 1) {
							currentPuzzle.setCell(x, yInstance, z+1);
							changeHappens = true;
						}
						
					}
					
					for(int y=0; y<size; y++) {
						int instances = 0;
						int xInstance = 9;
						for(int x=0; x<size; x++) {
							if(currentPuzzle.getTable()[x][y][z] == 1 && currentPuzzle.getDensity()[x][y] > 1) {
								instances++;
								xInstance = x;
							}
						}
						
						if(instances == 1) {
							currentPuzzle.setCell(xInstance, y, z+1);
							changeHappens = true;
						}
						
					}
					
					for(int j=0; j<superCell; j++) {
						for(int i=0; i<superCell; i++) {
							int instances = 0;
							int xInstance = 9;
							int yInstance = 9;
							for(int x=superCell*j; x<superCell*(j+1); x++) {
								for(int y=superCell*i; y<superCell*(i+1); y++) {
									instances++;
									xInstance = x;
									yInstance = y;
								}
							}
							if(instances == 1) {
								currentPuzzle.setCell(xInstance, yInstance, z+1);
								changeHappens = true;
							}
						}
					}
				}
			}
			
			System.out.println("Reached dead end, applying heuristic...");
			
			Coords move = problem.getNextMove();
			
			problem = problem.branch();
			if(problem == null) {
				System.out.println("Possibilities exhausted, please ensure that you have entered a solvable puzzle.");
				System.exit(0);
			}
			currentPuzzle = problem.getRoot();
			currentPuzzle.setCell(move.x, move.y, move.z);
			
			if(!currentPuzzle.isValid()) {
				System.out.println("Invalid solution, reverting...");
				problem = problem.revert();
				currentPuzzle = problem.getRoot();
			}
		}
		
		System.out.println("Puzzle solved: \n" + currentPuzzle.toString());
	}
	
	private static void parsePuzzle(String fp) throws IOException {
		FileReader fr = new FileReader(fp);
		BufferedReader br = new BufferedReader(fr);
		LinkedList<Integer> stack = new LinkedList<Integer>();
		int rawInt;
		int[][] rawData = new int[size][size];
		
		for(int i=0; i<size; i++) {
			rawInt = Integer.parseInt(br.readLine());
			while(rawInt > 0) {
				stack.push(rawInt%10);
				rawInt = rawInt/10;
			}
			
			for(int j=0; j<size-stack.size(); j++) {
				rawData[i][j] = 0;
			}
			
			for(int j=size-stack.size(); j<size; j++) {
				rawData[i][j] = stack.pop();
			}
		}
		
		for(int j=0; j<size; j++) {
			for(int i=0; i<size; i++) {
				if(rawData[i][j] > 0) {
					currentPuzzle.setCell(i, j, rawData[i][j]);
				}
			}
		}
		
		br.close();
	}
}

class Puzzle {
	private int[][][] possibilities;
	private int[] count;
	private int[][] density;
	private boolean[][] placed;
	private int size;
	private boolean solved;
	
	public Puzzle(int size) {
		this.size = size;
		possibilities = new int[size][size][size];
		density = new int[size][size];
		count = new int[size];
		placed = new boolean[size][size];
		
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
		possibilities = new int[size][size][size];
		density = new int[size][size];
		count = new int[size];
		placed = new boolean[size][size];
		for(int i=0; i<size; i++) {
			for(int j=0; j<size; j++) {
				for(int k=0; k<size; k++) {
					possibilities[i][j][k] = parent.getTable()[i][j][k];
				}
				density[i][j] = parent.getDensity()[i][j];
				placed[i][j] = parent.getPlaced()[i][j];
			}
			count[i] = parent.getCount()[i];
		}
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
	
	public int[][] getDensity() {
		return density;
	}
	
	public boolean[][] getPlaced() {
		return placed;
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
		} else if(y<6) {
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
		
		System.out.println("Placing " + n + " at (" + x + "," + y + ")");
		possibilities[x][y][n-1] = 1;
		placed[x][y] = true;
		calcDensity();
		
		if(isValid()) {
			count[n-1]--;
		}
		
		for(int i=0; i<size; i++) {
			if(count[i] > 0) {
				return;
			}
		}
		
		solved = true;
	}
	
	public void calcDensity() {
		for(int y=0; y<size; y++) {
			for(int x=0; x<size;x++) {
				int counter = 0;
				int n = 0;
				for(int z=0; z<size; z++) {
					if(possibilities[x][y][z] == 1) {
						counter++;
						n = z;
					}
				}
				
				density[x][y] = counter;
				
				if(counter == 1 && !placed[x][y]) {
					setCell(x, y, n+1);
				}
			}
		}
	}
	
	public String toString() {
		String returnString = " ||-------------------------------------||\n";
		boolean singular = false;
		int cell = 0;
		
		for(int x=0; x<size; x++) {
			for(int y=0; y<size; y++) {
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
				
				if(y%Math.sqrt(size) == 0) {
					sep = " || ";
				}
				
				if(singular) {
					returnString = returnString + sep + cell;
				} else {
					returnString = returnString + sep +" ";
				}
				
				singular = false;
			}
			if((x+1)%Math.sqrt(size) == 0) {
				returnString = returnString + " ||\n ||-------------------------------------||\n";
			} else {
				returnString = returnString + " ||\n";
			}
		}
		
		return returnString;
	}
	
	public String toData() {
		String returnString = "";
		
		for(int y=0; y<size; y++) {
			returnString = returnString + "\n";
			for(int x=0; x<size; x++) {
				returnString = returnString + " : ";
				for(int z=0; z<size; z++) {
					returnString = returnString + possibilities[x][y][z];
				}
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
	private PuzzleTree parentTree;
	private ArrayList<PuzzleTree> leafPuzzles;
	private int currentPuzzle;
//	private int maxBranch;
	private LinkedList<Coords> heuristic;
	
	public PuzzleTree(int size) {
		rootPuzzle = new Puzzle(size);
		currentPuzzle = -1;
		leafPuzzles = new ArrayList<PuzzleTree>();
		heuristic = new LinkedList<Coords>();
//		calcMax();
		calcHeuristic();
	}
	
	public PuzzleTree(Puzzle parent) {
		parentTree = null;
		rootPuzzle = new Puzzle(parent);
		currentPuzzle = -1;
		leafPuzzles = new ArrayList<PuzzleTree>();
		heuristic = new LinkedList<Coords>();
//		calcMax();
		calcHeuristic();
	}
	
	public PuzzleTree(Puzzle parent, PuzzleTree parentTree) {
		this.parentTree = parentTree;
		rootPuzzle = new Puzzle(parent);
		currentPuzzle = -1;
		leafPuzzles = new ArrayList<PuzzleTree>();
		heuristic = new LinkedList<Coords>();
//		calcMax();
		calcHeuristic();
	}
	
	public Puzzle getRoot() {
		return rootPuzzle;
	}
	
	public PuzzleTree branch() {
//		calcMax();
		
		if(heuristic.size() == 0) {
			System.out.println("Cannot branch, exceeded current branch limit.");
			return revert();
		}
		
		leafPuzzles.add(new PuzzleTree(rootPuzzle, this));
		currentPuzzle++;
		return leafPuzzles.get(currentPuzzle);
	}
	
	public PuzzleTree revert() {
		if(heuristic.size() == 0) {
			return parentTree.revert();
		}
		return parentTree;
	}
	
/*	public void calcMax() {
		maxBranch = 0;
		for(int x=0; x<rootPuzzle.getSize(); x++) {
			for(int y=0; y<rootPuzzle.getSize(); y++) {
				if(rootPuzzle.getDensity()[x][y] > 1) {
					maxBranch += rootPuzzle.getDensity()[x][y];
				}
			}
		}
	}*/
	
	public Coords getNextMove() {
		return heuristic.pop();
	}
	
	private void calcHeuristic() {
		int size = rootPuzzle.getSize();
		
		for(int y=0; y<size; y++) {
			for(int x=0; x<size; x++) {
				if(rootPuzzle.getDensity()[x][y] > 1) {
					for(int z=0; z<size; z++) {
						if(rootPuzzle.getTable()[x][y][z] == 1) {
							Coords temp = new Coords(x, y, z+1);
							heuristic.push(temp);
						}
					}
				}
			}
		}
	}
}

class Coords {
	public int x, y, z;
	
	public Coords(int x, int y, int z) {
		this.x = x;
		this.y = y;
		this.z = z;
	}
}
