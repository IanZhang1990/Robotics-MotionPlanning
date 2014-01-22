#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <list>
#include <vector>

// CGAL Lib
#include <CGAL/Polygon_2.h>
#include <CGAL/Boolean_set_operations_2.h>

#include "RobotArm.h"
#include "FileWriter.h"

using std::cout;
using std::endl;



//std::srand(std::time(0));

RobotArm robot(MyPoint(400.0,300.0),100, 100, 100);

int obstSize = 8;
Point points[8][4] = { { Point(400+40,250+10), Point(400,250+10), Point(400,250), Point(400+40,250)},
		{ Point(460+40,250+10), Point(460,250+10), Point(460,250), Point(460+40,250)},
		{ Point(400+40,370+30), Point(400,370+30), Point(400,370), Point(400+40,370)},
		{ Point(270+40,290+10), Point(270,290+10), Point(270,290), Point(270+40,290)},
		{ Point(470+40,300+50), Point(470,300+50), Point(470,300), Point(470+40,300)},
		{ Point(350+40,100+50), Point(350,100+50), Point(350,100), Point(350+40,100)},
		{ Point(350+40,190+10), Point(350,190+10), Point(350,190), Point(350+40,190)},
		{ Point(320+100,210+20), Point(320,210+20), Point(320,210), Point(320+100,210)}
};

Polygon2d polys[8];


double fRand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

std::vector<double> randomConfig()
{
	double theta = fRand( 0.0, PI * 2 );
	double alpha = fRand( 0.0, PI * 2 );
	double phi   = fRand( 0.0, PI * 2 );
	std::vector<double> ret;
	ret.push_back(theta);
	ret.push_back(alpha);
	ret.push_back(phi);
	return ret;
}

void sample( int number )
{
	std::vector< std::vector<double> > collisionCofigs;
	std::vector< std::vector<double> > freeConfigs;

	std::srand( std::time(0) );

	for( int i=0; i < number; i++ )
	{
		if( i % 100 == 0 )
			printf( "Sample NO. %d \n", i );

		std::vector<double> randConfig = randomConfig();
		robot.updateAngles( randConfig[0],randConfig[1],randConfig[2] );
		//printf( "Get sample: %f\t%f\t%f\n", randConfig[0],randConfig[1],randConfig[2] );
		bool ifCollide = false;
		for( int i = 0; i < obstSize; i++  )
		{
			if(robot.collideWith( polys[i] ))
			{
				std::vector<double> record;
				record.push_back(randConfig[0]);
				record.push_back(randConfig[1]);
				record.push_back(randConfig[2]);
				record.push_back(i);
				collisionCofigs.push_back( record );
				ifCollide = true;
			}
		}
		if( ifCollide == false )
		{
			std::vector<double> record;
			record.push_back(randConfig[0]);
			record.push_back(randConfig[1]);
			record.push_back(randConfig[2]);
			freeConfigs.push_back( record );
		}
		randConfig.clear();
	}

	std::cout << "Get obstacle config: " << collisionCofigs.size() << std::endl;
	std::cout << "Get free config: " << freeConfigs.size() << std::endl;


	// Write to file
	std::cout << "Write to file...\n";
	FileWriter fileWriter;
	for( unsigned int i = 0; i < collisionCofigs.size(); i++ )
	{
		std::vector<double> record = collisionCofigs[i];
		fileWriter.addData( record[0],record[1],record[2],i );
	}
	for( unsigned int i = 0; i < freeConfigs.size(); i++ )
	{
		fileWriter.addData( freeConfigs[i][0],freeConfigs[i][1],freeConfigs[i][2] );
	}
	fileWriter.flush();

}


int main ()
{
	for( int i =0; i < obstSize; i++ )
	{
		polys[i] = Polygon2d( points[i], points[i]+4 );
	}


	std::cout << "Begin to sample...\n";
	sample( 5000 );
	std::cout << "DONE!!!\n";

	return 0;
}


