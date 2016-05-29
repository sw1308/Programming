package Directory is
	function Present (Name : String) return Boolean; -- Returns true if Name is contained in Directory
	generic
		with procedure Visit (Name, Phone_Number, Address : String; Stop : out Boolean);
	procedure Iterate (Name : String);
end Directory;