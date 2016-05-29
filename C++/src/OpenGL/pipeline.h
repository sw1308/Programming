#ifndef PIPELINE_H
#define PIPELINE_H

#include "math_3d.h"

struct orientation
{
	vector3f scale;
	vector3f rotation;
	vector3f pos;

	orientation()
	{
		scale = vector3f(1.0f, 1.0f, 1.0f);
		rotation = vector3f(0.0f, 0.0f, 0.0f);
		pos = vector3f(0.0f, 0.0f, 0.0f);
	}
};

class pipeline
{
public:
	pipeline()
	{
		m_scale = vector3f(1.0f, 1.0f, 1.0f);
		m_rotation = vector3f(0.0f, 0.0f, 0.0f);
		m_worldPos = vector3f(0.0f, 0.0f, 0.0f);
	}

	void scale(float s)
	{
		scale(s, s, s);
	}

	void scale(vector3f& vScale)
	{
		scale(vScale.x, vScale.y, vScale.z);
	}

	void scale(float scaleX, float scaleY, float scaleZ)
	{
		m_scale.x = scaleX;
		m_scale.y = scaleY;
		m_scale.z = scaleZ;
	}

	void worldPos(float x, float y, float z)
	{
		m_worldPos.x = x;
		m_worldPos.y = y;
		m_worldPos.z = z;
	}

	void worldPos(const vector3f& pos)
	{
		m_worldPos = pos;
	}

	void rotate(float rotX, float rotY, float rotZ)
	{
		m_rotation.x = rotX;
		m_rotation.y = rotY;
		m_rotation.z = rotZ;
	}

	void rotate(const vector3f& r)
	{
		rotate(r.x, r.y, r.z);
	}

	void setPerspectiveProj(const persProjInfo& p)
	{
		m_persProjInfo = p;
	}

	void setCamera(const vector3f& pos, const vector3f& target, const vector3f up)
	{
		m_camera.pos = pos;
		m_camera.target = target;
		m_camera.up = up;
	}

	void reOrient(const orientation& o)
	{
		m_scale = o.scale;
		m_worldPos = o.pos;
		m_rotation = o.rotation;
	}

	const matrix4f& getProjTrans();
	const matrix4f& getWorldTrans();
	const matrix4f& getWPTrans();

private:
	vector3f m_scale;
	vector3f m_worldPos;
	vector3f m_rotation;

	persProjInfo m_persProjInfo;

	struct
	{
		vector3f pos;
		vector3f target;
		vector3f up;
	} m_camera;

	matrix4f m_WTransformation;
	matrix4f m_WPTransformation;
	matrix4f m_projTransformation;
};

#endif /* PIPELINE_H */