package GravitationalBody is
	radius : Float;
	mass : Float;
	lastUpdated : Integer;
	physicsLess : Boolean;

	type position is
	record
		x : Float;
		y : Float;
	end record;

	type velocity is
	record
		x : Float;
		y : Float;
	end record;

	currentVelocity : velocity;
	currentPosition : position;

	function getVelocity() return velocity;
	function getPosition() return position;
	procedure exertForce (xForce : in Float; yForce : in Float);

	function getVelocity() return velocity is
	begin --getVelocity
		return currentVelocity;
	end;

	function getPosition() return position is
	begin --getPosition
		return currentPosition;
	end;
begin
	
end;