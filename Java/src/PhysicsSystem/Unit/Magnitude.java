package PhysicsSystem.Unit;

/*
	Generic class intended to represent prefixes like kilo, mega, giga, etc.
*/

public class Magnitude {
	private String name;
	private double magnitude;
	private String prefix;

	public Magnitude(String name, String prefix, double magnitude) {
		this.name = name;
		this.prefix = prefix;
		this.magnitude = magnitude;
	}

	public String getName() {return this.name;}
	public String getPrefix() {return this.prefix;}
	public double getMagnitude() {return this.magnitude;}
}
