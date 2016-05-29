package PhysicsSystem.Unit;

import PhysicsSystem.Unit.Magnitude;
import PhysicsSystem.Type.UnitType;
import PhysicsSystem.Interface.UnitInterface;

/*
	This class forms the basis of all units that can be used in the system.
	It is not designed to be changed once instantiated (except for the scale).
*/

public class Unit implements UnitInterface {
	// Name used to easily identify the Unit type in a human readable format.
	private String unitName;

	// Enum of the generic type that indicates compatible Units you can convert between.
	private UnitType unitType;

	// Ratio between one Unit and the SI Unit of the same type.
	private double conversionRatio;

	// Factor to use when being asked to display at a certain magnitude.
	private Magnitude scaleFactor;

	public Unit(String name, UnitType unitType) {this(name, unitType, 1.0d);}

	public Unit(String name, UnitType unitType, double conversionRatio) {
		this.unitName = name;
		this.unitType = unitType;
		this.conversionRatio = conversionRatio;
	}

	public String getUnitName() {return this.unitName;}
	public UnitType getUnitType() {return this.unitType;}
	public double getConversionRatio() {return this.conversionRatio * this.scaleFactor.getMagnitude();}

	public String getPrintedName() {return this.scaleFactor.getPrefix() + this.unitName;}
}