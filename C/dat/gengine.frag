#version 300 es

smooth in lowp vec4 vertColour;

out lowp vec4 OutputColour;

void main()
{
	OutputColour = vertColour;
}
