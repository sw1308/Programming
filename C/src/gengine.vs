#version 300

layout (location = 0) in vec4 position;
layout (location = 1) in vec4 colour;

smooth out vec4 OutputColour;

void main()
{
	gl_Position = position;
	OutputColour = colour;
}
