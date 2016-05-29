#include <stdlib.h>

#include "math_3d.h"

vector3f vector3f::cross(const vector3f& v) const
{
	const float _x = y * v.z - z * v.y;
	const float _y = z * v.x - x * v.z;
	const float _z = x * v.y - y * v.x;

	return vector3f(_x, _y, _z);
}

vector3f vector3f::normalize()
{
	const float length = sqrtf((x * x) + (y * y) + (z * z));

	x /= length;
	y /= length;
	z /= length;

	return *this;
}

void vector3f::rotate(float angle, const vector3f& axis)
{
	const float sinHalfAngle = sinf(toRadian(angle/2));
	const float cosHalfAngle = cosf(toRadian(angle/2));

	const float rx = axis.x * sinHalfAngle;
	const float ry = axis.y * sinHalfAngle;
	const float rz = axis.z * sinHalfAngle;
	const float rw = cosHalfAngle;

	quaternion rotationQ(rx, ry, rz, rw);
	quaternion conjugateQ = rotationQ.conjugate();

	quaternion w = rotationQ * (*this) * conjugateQ;

	x = w.x;
	y = w.y;
	z = w.z;
}

void matrix4f::initScaleTransform(float scaleX, float scaleY, float scaleZ)
{
	m[0][0] = scaleX; m[0][1] = 0.0f; m[0][2] = 0.0f; m[0][3] = 0.0f;
	m[1][0] = 0.0f; m[1][1] = scaleY; m[1][2] = 0.0f; m[1][3] = 0.0f;
	m[2][0] = 0.0f; m[2][1] = 0.0f; m[2][2] = scaleZ; m[2][3] = 0.0f;
	m[3][0] = 0.0f; m[3][1] = 0.0f; m[3][2] = 0.0f; m[3][3] = 1.0f;
}

void matrix4f::updateScaleTransform(float scaleX, float scaleY, float scaleZ)
{
	m[0][0] = scaleX;
	m[1][1] = scaleY;
	m[2][2] = scaleZ;
}

void matrix4f::initRotateTransform(float rotX, float rotY, float rotZ)
{
	matrix4f rx, ry, rz;

	const float x = toRadian(rotX);
	const float y = toRadian(rotY);
	const float z = toRadian(rotZ);

	rx.m[0][0] = 1.0f;	rx.m[0][1] = 0.0f;		rx.m[0][2] = 0.0f; 		rx.m[0][3] = 0.0f;
	rx.m[1][0] = 0.0f;	rx.m[1][1] = cosf(x);	rx.m[1][2] = -sinf(x);	rx.m[1][3] = 0.0f;
	rx.m[2][0] = 0.0f;	rx.m[2][1] = sinf(x);	rx.m[2][2] = cosf(x);	rx.m[2][3] = 0.0f;
	rx.m[3][0] = 0.0f;	rx.m[3][1] = 0.0f;		rx.m[3][2] = 0.0f;		rx.m[3][3] = 1.0f;

	ry.m[0][0] = cosf(y);	ry.m[0][1] = 0.0f; ry.m[0][2] = -sinf(y);	ry.m[0][3] = 0.0f;
	ry.m[1][0] = 0.0f;		ry.m[1][1] = 1.0f; ry.m[1][2] = 0.0f;		ry.m[1][3] = 0.0f;
	ry.m[2][0] = sinf(y);	ry.m[2][1] = 0.0f; ry.m[2][2] = cosf(y);	ry.m[2][3] = 0.0f;
	ry.m[3][0] = 0.0f;		ry.m[3][1] = 0.0f; ry.m[3][2] = 0.0f;		ry.m[3][3] = 1.0f;

	rz.m[0][0] = cosf(z);	rz.m[0][1] = -sinf(z);	rz.m[0][2] = 0.0f;	rz.m[0][3] = 0.0f;
	rz.m[1][0] = sinf(z);	rz.m[1][1] = cosf(z);	rz.m[1][2] = 0.0f;	rz.m[1][3] = 0.0f;
	rz.m[2][0] = 0.0f;		rz.m[2][1] = 0.0f;		rz.m[2][2] = 1.0f;	rz.m[2][3] = 0.0f;
	rz.m[3][0] = 0.0f;		rz.m[3][1] = 0.0f;		rz.m[3][2] = 0.0f;	rz.m[3][3] = 1.0f;

	*this = rz * ry * rx;
}

void matrix4f::initTranslateTransform(float x, float y, float z)
{
	m[0][0] = 1.0f; m[0][1] = 0.0f; m[0][2] = 0.0f; m[0][3] = x;
	m[1][0] = 0.0f; m[1][1] = 1.0f; m[1][2] = 0.0f; m[1][3] = y;
	m[2][0] = 0.0f; m[2][1] = 0.0f; m[2][2] = 1.0f; m[2][3] = z;
	m[3][0] = 0.0f; m[3][1] = 0.0f; m[3][2] = 0.0f; m[3][3] = 1.0f;
}

void matrix4f::updateTranslateTransform(float x, float y, float z)
{
	m[0][3] = x;
	m[1][3] = y;
	m[2][3] = z;
}

void matrix4f::initCameraTransform(const vector3f& target, const vector3f& up)
{
	vector3f n = target;
	n.normalize();

	vector3f u = up;
	u.normalize();

	u = u.cross(n);
	vector3f v = n.cross(u);

	m[0][0] = u.x; m[0][1] = u.y; m[0][2] = u.z; m[0][3] = 0.0f;
	m[1][0] = v.x; m[1][1] = v.y; m[1][2] = v.z; m[1][3] = 0.0f;
	m[2][0] = n.x; m[2][1] = n.y; m[2][2] = n.z; m[2][3] = 0.0f;
	m[3][0] = 0.0f; m[3][1] = 0.0f; m[3][2] = 0.0f; m[3][3] = 1.0f;
}

void matrix4f::initPersProjTransform(const persProjInfo& p)
{
	const float ar = p.width / p.height;
	const float zRange = p.zNear - p.zFar;
	const float tanHalfFOV = tanf(toRadian(p.FOV / 2.0f));

	m[0][0] = 1.0f/(tanHalfFOV * ar);	m[0][1] = 0.0f; 				m[0][2] = 0.0f;							m[0][3] = 0.0f;
	m[1][0] = 0.0f; 					m[1][1] = 1.0f/(tanHalfFOV);	m[1][2] = 0.0f;							m[1][3] = 0.0f;
	m[2][0] = 0.0f; 					m[2][1] = 0.0f; 				m[2][2] = (-p.zNear - p.zFar)/zRange;	m[2][3] = 2.0f*p.zFar*p.zNear/zRange;
	m[3][0] = 0.0f; 					m[3][1] = 0.0f; 				m[3][2] = 1.0f; 						m[3][3] = 1.0f;
}

void matrix4f::initOrthoProjTransform(const persProjInfo& p)
{
	const float zRange = p.zNear - p.zFar;

	m[0][0] = 2.0f/p.width;	m[0][1] = 0.0f;				m[0][2] = 0.0f; 		m[0][3] = 0.0f;
	m[1][0] = 0.0f; 		m[1][1] = 2.0f/p.height;	m[1][2] = 0.0f; 		m[1][3] = 0.0f;
	m[2][0] = 0.0f; 		m[2][1] = 0.0f; 			m[2][2] = 2.0f/zRange;	m[2][3] = (-p.zFar - p.zNear)/zRange;
	m[3][0] = 0.0f; 		m[3][1] = 0.0f; 			m[3][2] = 0.0f; 		m[3][3] = 1.0f;
}

float matrix4f::determinant() const
{
	return m[0][0]*m[1][1]*m[2][2]*m[3][3] - m[0][0]*m[1][1]*m[2][3]*m[3][2] + m[0][0]*m[1][2]*m[2][3]*m[3][1] - m[0][0]*m[1][2]*m[2][1]*m[3][3] 
		+ m[0][0]*m[1][3]*m[2][1]*m[3][2] - m[0][0]*m[1][3]*m[2][2]*m[3][1] - m[0][1]*m[1][2]*m[2][3]*m[3][0] + m[0][1]*m[1][2]*m[2][0]*m[3][3] 
		- m[0][1]*m[1][3]*m[2][0]*m[3][2] + m[0][1]*m[1][3]*m[2][2]*m[3][0] - m[0][1]*m[1][0]*m[2][2]*m[3][3] + m[0][1]*m[1][0]*m[2][3]*m[3][2] 
		+ m[0][2]*m[1][3]*m[2][0]*m[3][1] - m[0][2]*m[1][3]*m[2][1]*m[3][0] + m[0][2]*m[1][0]*m[2][1]*m[3][3] - m[0][2]*m[1][0]*m[2][3]*m[3][1] 
		+ m[0][2]*m[1][1]*m[2][3]*m[3][0] - m[0][2]*m[1][1]*m[2][0]*m[3][3] - m[0][3]*m[1][0]*m[2][1]*m[3][2] + m[0][3]*m[1][0]*m[2][2]*m[3][1]
		- m[0][3]*m[1][1]*m[2][2]*m[3][0] + m[0][3]*m[1][1]*m[2][0]*m[3][2] - m[0][3]*m[1][2]*m[2][0]*m[3][1] + m[0][3]*m[1][2]*m[2][1]*m[3][0];
}

matrix4f& matrix4f::inverse()
{
	// Compute the reciprocal determinant
	float det = determinant();
	if(det == 0.0f)
	{
		// Matrix cannot be invertible,
		// throw an assertion error.

		assert(0);
		return *this;
	}

	float invdet = 1.0f / det;

	matrix4f res;
	res.m[0][0] = invdet  * (m[1][1] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) + m[1][2] * (m[2][3] * m[3][1] - m[2][1] * m[3][3]) + m[1][3] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]));
	res.m[0][1] = -invdet * (m[0][1] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) + m[0][2] * (m[2][3] * m[3][1] - m[2][1] * m[3][3]) + m[0][3] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]));
	res.m[0][2] = invdet  * (m[0][1] * (m[1][2] * m[3][3] - m[1][3] * m[3][2]) + m[0][2] * (m[1][3] * m[3][1] - m[1][1] * m[3][3]) + m[0][3] * (m[1][1] * m[3][2] - m[1][2] * m[3][1]));
	res.m[0][3] = -invdet * (m[0][1] * (m[1][2] * m[2][3] - m[1][3] * m[2][2]) + m[0][2] * (m[1][3] * m[2][1] - m[1][1] * m[2][3]) + m[0][3] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]));
	res.m[1][0] = -invdet * (m[1][0] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) + m[1][2] * (m[2][3] * m[3][0] - m[2][0] * m[3][3]) + m[1][3] * (m[2][0] * m[3][2] - m[2][2] * m[3][0]));
	res.m[1][1] = invdet  * (m[0][0] * (m[2][2] * m[3][3] - m[2][3] * m[3][2]) + m[0][2] * (m[2][3] * m[3][0] - m[2][0] * m[3][3]) + m[0][3] * (m[2][0] * m[3][2] - m[2][2] * m[3][0]));
	res.m[1][2] = -invdet * (m[0][0] * (m[1][2] * m[3][3] - m[1][3] * m[3][2]) + m[0][2] * (m[1][3] * m[3][0] - m[1][0] * m[3][3]) + m[0][3] * (m[1][0] * m[3][2] - m[1][2] * m[3][0]));
	res.m[1][3] = invdet  * (m[0][0] * (m[1][2] * m[2][3] - m[1][3] * m[2][2]) + m[0][2] * (m[1][3] * m[2][0] - m[1][0] * m[2][3]) + m[0][3] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]));
	res.m[2][0] = invdet  * (m[1][0] * (m[2][1] * m[3][3] - m[2][3] * m[3][1]) + m[1][1] * (m[2][3] * m[3][0] - m[2][0] * m[3][3]) + m[1][3] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]));
	res.m[2][1] = -invdet * (m[0][0] * (m[2][1] * m[3][3] - m[2][3] * m[3][1]) + m[0][1] * (m[2][3] * m[3][0] - m[2][0] * m[3][3]) + m[0][3] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]));
	res.m[2][2] = invdet  * (m[0][0] * (m[1][1] * m[3][3] - m[1][3] * m[3][1]) + m[0][1] * (m[1][3] * m[3][0] - m[1][0] * m[3][3]) + m[0][3] * (m[1][0] * m[3][1] - m[1][1] * m[3][0]));
	res.m[2][3] = -invdet * (m[0][0] * (m[1][1] * m[2][3] - m[1][3] * m[2][1]) + m[0][1] * (m[1][3] * m[2][0] - m[1][0] * m[2][3]) + m[0][3] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]));
	res.m[3][0] = -invdet * (m[1][0] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]) + m[1][1] * (m[2][2] * m[3][0] - m[2][0] * m[3][2]) + m[1][2] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]));
	res.m[3][1] = invdet  * (m[0][0] * (m[2][1] * m[3][2] - m[2][2] * m[3][1]) + m[0][1] * (m[2][2] * m[3][0] - m[2][0] * m[3][2]) + m[0][2] * (m[2][0] * m[3][1] - m[2][1] * m[3][0]));
	res.m[3][2] = -invdet * (m[0][0] * (m[1][1] * m[3][2] - m[1][2] * m[3][1]) + m[0][1] * (m[1][2] * m[3][0] - m[1][0] * m[3][2]) + m[0][2] * (m[1][0] * m[3][1] - m[1][1] * m[3][0]));
	res.m[3][3] = invdet  * (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) + m[0][1] * (m[1][2] * m[2][0] - m[1][0] * m[2][2]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]));

	*this = res;

	return *this;
}

quaternion::quaternion(float _x, float _y, float _z, float _w)
{
	x = _x;
	y = _y;
	z = _z;
	w = _w;
}

void quaternion::normalize()
{
	float length = sqrtf((x * x) + (y * y) + (z * z));

	x /= length;
	y /= length;
	z /= length;
	w /= length;
}

quaternion quaternion::conjugate()
{
	quaternion ret(-x, -y, -z, w);

	return ret;
}

quaternion operator*(const quaternion& l, const quaternion& r)
{
	const float w = (l.w * r.w) - (l.x * r.x) - (l.y * r.y) - (l.z * r.z);
	const float x = (l.x * r.w) - (l.w * r.x) - (l.y * r.z) - (l.z * r.y);
	const float y = (l.y * r.w) - (l.w * r.y) - (l.z * r.x) - (l.x * r.z);
	const float z = (l.z * r.w) - (l.w * r.z) - (l.x * r.y) - (l.y * r.x);

	quaternion ret(x, y, z, w);

	return ret;
}

quaternion operator*(const quaternion& q, const vector3f& v)
{
	const float w = -(q.x * v.x) - (q.y * v.y) - (q.z * v.z);
	const float x = (q.w * v.x) - (q.y * v.z) - (q.z * v.y);
	const float y = (q.w * v.y) - (q.z * v.x) - (q.x * v.z);
	const float z = (q.w * v.z) - (q.x * v.y) - (q.y * v.x);

	quaternion ret(x, y, z, w);

	return ret;
}

float randomFloat()
{
	float max = RAND_MAX;
	return ((float)RANDOM())/max;
}