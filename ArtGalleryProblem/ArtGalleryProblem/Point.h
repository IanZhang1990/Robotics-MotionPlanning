//////////////////////////////////////////////////////////////////////////
////				class for points in 2D space
//////////////////////////////////////////////////////////////////////////


#include <glm/glm.hpp>

class Point2D
{
public:
	
	Point2D( int x=0, int y=0 )
	{
		this->mPos = glm::vec2(x, y);
	}

	int getX()
	{
		return this->mPos[0];
	}

	int getY()
	{
		return mPos[1];
	}
	
	glm::vec2 mPos;
};