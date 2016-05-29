#version 330

layout (location=0) in vec3 position;

out vec4 colour;

uniform mat4 gWorld;

void main()
{
	colour = clamp((vec4(position, 1.0)), 0.3, 1.0);
	gl_Position = gWorld * vec4(position, 1.0);
}
