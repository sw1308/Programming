#include "pipeline.h"

const matrix4f& pipeline::getProjTrans()
{
	m_projTransformation.initPersProjTransform(m_persProjInfo);
	return m_projTransformation;
}

const matrix4f& pipeline::getWorldTrans()
{
	matrix4f scaleTrans, rotateTrans, translationTrans;

	scaleTrans.initScaleTransform(m_scale.x, m_scale.y, m_scale.z);
	rotateTrans.initRotateTransform(m_rotation.x, m_rotation.y, m_rotation.z);
	translationTrans.initTranslateTransform(m_worldPos.x, m_worldPos.y, m_worldPos.z);

	m_WTransformation = translationTrans * rotateTrans * scaleTrans;

	return m_WTransformation;
}

const matrix4f& pipeline::getWPTrans()
{
	getWorldTrans();
	getProjTrans();

	m_WPTransformation = m_projTransformation * m_WTransformation;
	return m_WPTransformation;
}