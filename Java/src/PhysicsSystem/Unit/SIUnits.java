package PhysicsSystem.Unit;

import PhysicsSystem.Unit.Unit;
import PhysicsSystem.Type.UnitType;

public class SIUnits {
	public static final Unit Metre = new Unit("m", UnitType.LENGTH);
	public static final Unit Kilogram = new Unit("kg", UnitType.MASS);
	public static final Unit Second = new Unit("s", UnitType.TIME);
	public static final Unit Ampere = new Unit("A", UnitType.CURRENT);
	public static final Unit Kelvin = new Unit("K", UnitType.TEMPERATURE);
	public static final Unit Mole = new Unit("mol", UnitType.CHEMICALAMOUNT);
	public static final Unit Candela = new Unit("cd", UnitType.LUMINOSITY);
}