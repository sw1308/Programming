#ifndef MATH_3D_H
#define MATH_3D_H

#include "utils.h"

#include <stdio.h>

#ifdef WIN32
	#define _USE_MATH_DEFINES
	#include <cmath>
#else
	#include <math.h>
#endif /* def WIN32 */

#define toRadian(x) (float)(((x) * M_PI / 180.0f))
#define toDegree(x) (float)(((x) * 180.0f / M_PI))

float randomFloat();

struct vector2i
{
	int x;
	int y;
};

struct vector2f
{
	float x;
	float y;

	vector2f()
	{}

	vector2f(float _x, float _y)
	{
		x = _x;
		y = _y;
	}
};

struct vector3f
{
	float x;
	float y;
	float z;

	vector3f()
	{}

	vector3f(float _x, float _y, float _z)
	{
		x = _x;
		y = _y;
		z = _z;
	}

	vector3f(float f)
	{
		x = y = z = f;
	}

	vector3f& operator +=(const vector3f& r)
	{
		x += r.x;
		y += r.y;
		z += r.z;

		return *this;
	}

	vector3f& operator -=(const vector3f& r)
	{
		x -= r.x;
		y -= r.y;
		z -= r.z;

		return *this;
	}

	vector3f& operator *=(float f)
	{
		x *= f;
		y *= f;
		z *= f;

		return *this;
	}

	operator const float*() const
	{
		return &(x);
	}

	vector3f cross(const vector3f& v) const;

	vector3f normalize();

	void rotate(float angle, const vector3f& axis);

	void print() const
	{
		printf("(%0.2f, %0.2f, %0.2f)", x, y, z);
	}
};

struct vector4f
{
	float x;
	float y;
	float z;
	float w;

	vector4f()
	{}

	vector4f(float _x, float _y, float _z, float _w)
	{
		x = _x;
		y = _y;
		z = _z;
		w = _w;
	}

	void print() const
	{
		printf("(%0.2f, %0.2f, %0.2f, %0.2f)", x, y, z, w);
	}

	vector3f to3f() const
	{
		vector3f v(x, y, z);
		return v;
	}
};

inline vector3f operator +(const vector3f& l, const vector3f& r)
{
	vector3f ret(
		l.x + r.x,
		l.y + r.y,
		l.z + r.z
	);

	return ret;
}

inline vector3f operator -(const vector3f& l, const vector3f& r)
{
	vector3f ret(
		l.x - r.x,
		l.y - r.y,
		l.z - r.z
	);

	return ret;
}

inline vector3f operator *(const vector3f& l, float f)
{
	vector3f ret(
		l.x * f,
		l.y * f,
		l.z * f
	);

	return ret;
}

inline vector3f operator /(const vector3f& l, float f)
{
	vector3f ret(
		l.x / f,
		l.y / f,
		l.z / f
	);

	return ret;
}

struct persProjInfo
{
	float FOV;
	float width;
	float height;
	float zNear;
	float zFar;
};

class matrix4f
{
public:
	float m[4][4];

	matrix4f()
	{}

	matrix4f(
		float a0, float a1, float a2, float a3,
		float b0, float b1, float b2, float b3,
		float c0, float c1, float c2, float c3,
		float d0, float d1, float d2, float d3)
	{
		m[0][0] = a0; m[0][1] = a1; m[0][2] = a2; m[0][3] = a3;
		m[0][0] = b0; m[0][1] = b1; m[0][2] = b2; m[0][3] = b3;
		m[0][0] = c0; m[0][1] = c1; m[0][2] = c2; m[0][3] = c3;
		m[0][0] = d0; m[0][1] = d1; m[0][2] = d2; m[0][3] = d3;

	}

	void setZero()
	{
		// ZERO_MEM(m);
	}

	matrix4f transpose() const
	{
		matrix4f ret;
		for(unsigned int i=0; i<4; i++)
		{
			for(unsigned int j=0; j<4; j++)
			{
				ret.m[i][j] = m[j][i];
			}
		}

		return ret;
	}

	inline void identity()
	{
		m[0][0] = 1.0f; m[0][1] = 0.0f; m[0][2] = 0.0f; m[0][3] = 0.0f;
		m[0][0] = 0.0f; m[0][1] = 1.0f; m[0][2] = 0.0f; m[0][3] = 0.0f;
		m[0][0] = 0.0f; m[0][1] = 0.0f; m[0][2] = 1.0f; m[0][3] = 0.0f;
		m[0][0] = 0.0f; m[0][1] = 0.0f; m[0][2] = 0.0f; m[0][3] = 1.0f;
	}

	inline matrix4f operator *(const matrix4f& right) const
	{
		matrix4f ret;

		for(unsigned int i=0; i<4; i++)
		{
			for(unsigned int j=0; j<4; j++)
			{
				ret.m[i][j] = m[i][0] * right.m[0][j] +
							  m[i][1] * right.m[1][j] +
							  m[i][2] * right.m[2][j] +
							  m[i][3] * right.m[3][j];
			}
		}

		return ret;
	}

	vector4f operator *(const vector4f& v) const
	{
		vector4f ret;

		ret.x = m[0][0] * v.x + m[0][1] * v.y + m[0][2] * v.z + m[0][3] * v.w;
		ret.y = m[1][0] * v.x + m[1][1] * v.y + m[1][2] * v.z + m[1][3] * v.w;
		ret.z = m[2][0] * v.x + m[2][1] * v.y + m[2][2] * v.z + m[2][3] * v.w;
		ret.w = m[3][0] * v.x + m[3][1] * v.y + m[3][2] * v.z + m[3][3] * v.w;
	}

	operator const float*() const
	{
		return &(m[0][0]);
	}

	void print() const
	{
		for(int i=0; i<4; i++)
		{
			printf("%0.2f, %0.2f, %0.2f, %0.2f\n", m[i][0], m[i][1], m[i][2], m[i][3]);
		}
	}

	float determinant() const;

	matrix4f& inverse();

	void initScaleTransform(float scaleX, float scaleY, float scaleZ);
	void updateScaleTransform(float scaleX, float scaleY, float scaleZ);
	void initRotateTransform(float rotX, float rotY, float rotZ); // Does not have an update() function, can't be made much more efficient.
	void initTranslateTransform(float x, float y, float z);
	void updateTranslateTransform(float x, float y, float z);
	void initCameraTransform(const vector3f& target, const vector3f& up);
	void initPersProjTransform(const persProjInfo& p);
	void initOrthoProjTransform(const persProjInfo& p);
};

struct quaternion
{
	float x, y, z, w;

	quaternion(float _x, float _y, float _z, float _w);

	void normalize();

	quaternion conjugate();
};

quaternion operator *(const quaternion& l, const quaternion& r);
quaternion operator *(const quaternion& q, const vector3f& v);

#endif /* ndef MATH_3D_H */