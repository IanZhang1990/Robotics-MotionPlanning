
#include "Grid.h"
#include "IRenderable.h"
#include <vector>

#pragma once
class Plane: public IRenderable
{
public:
	Plane(void);
	~Plane(void);

	virtual void render();

public:
	std::vector<std::vector<Grid*>> mGrids;
};

