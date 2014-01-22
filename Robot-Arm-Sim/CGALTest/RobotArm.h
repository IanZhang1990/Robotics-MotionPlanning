#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Boolean_set_operations_2.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/Polygon_2_algorithms.h>
#include <math.h>
#include <iostream>
#include <GL/glut.h>  // for the OpenGL GLUT library

typedef CGAL::Exact_predicates_exact_constructions_kernel K;
typedef K::Point_2 Point;
typedef K::Circle_2 Circle;
typedef CGAL::Polygon_2<K> Polygon2d;
typedef CGAL::Polygon_with_holes_2<K> Polygon_with_holes_2;

using std::cout;
using std::endl;

#define PI 3.14159265354

struct MyPoint
{
	double x;
	double y;
	MyPoint(double _x=0, double _y=0)
	{
		x = _x;
		y = _y;
	}
};

class RobotArm
{
public:
	RobotArm(MyPoint startPos, int l1, int l2, int l3)
	{
		this->mStartPosition = startPos;

		this->mLength1 = l1;
		this->mLength2 = l2;
		this->mLength3 = l3;

		this->mAngle1 = 0;
		this->mAngle2 = 0;
		this->mAngle3 = 0;

		this->mWidth = 12;

		this->updateAngles( 0, 0, 0 );
	}

	void render()
	{
		glColor3f(1.0f, 0.0f, 0.0f);
		glBegin(GL_QUADS);
			for( int i=0; i < 4; i++ )
			{
				glVertex2f( (float)(this->mPointsOfSkt1[i].x), (float)(this->mPointsOfSkt1[i].y) );
			}
		glEnd();

		glColor3f(0.0f, 1.0f, 0.0f);
		glBegin(GL_QUADS);
			for( int i=0; i < 4; i++ )
			{
				glVertex2f( (float)(this->mPointsOfSkt2[i].x), (float)(this->mPointsOfSkt2[i].y) );
			}
		glEnd();

		glColor3f(1.0f, 1.0f, 0.0f);
		glBegin(GL_QUADS);
			for( int i=0; i < 4; i++ )
			{
				glVertex2f( (float)(this->mPointsOfSkt3[i].x), (float)(this->mPointsOfSkt3[i].y) );
			}
		glEnd();
	}

	bool collideWith( Polygon2d polygon )
	{
		Point points1[] = {Point(mPointsOfSkt1[0].x, mPointsOfSkt1[0].y), Point(mPointsOfSkt1[1].x, mPointsOfSkt1[1].y),
				Point(mPointsOfSkt1[2].x, mPointsOfSkt1[2].y), Point(mPointsOfSkt1[3].x, mPointsOfSkt1[3].y)};
		Point points2[] = {Point(mPointsOfSkt2[0].x, mPointsOfSkt2[0].y), Point(mPointsOfSkt2[1].x, mPointsOfSkt2[1].y),
						Point(mPointsOfSkt2[2].x, mPointsOfSkt2[2].y), Point(mPointsOfSkt2[3].x, mPointsOfSkt2[3].y)};
		Point points3[] = {Point(mPointsOfSkt3[0].x, mPointsOfSkt3[0].y), Point(mPointsOfSkt3[1].x, mPointsOfSkt3[1].y),
						Point(mPointsOfSkt3[2].x, mPointsOfSkt3[2].y), Point(mPointsOfSkt3[3].x, mPointsOfSkt3[3].y)};

		Polygon2d a = Polygon2d(points1, points1+4);
		Polygon2d b = Polygon2d(points2, points2+4);
		Polygon2d c = Polygon2d(points3, points3+4);


		return CGAL::do_intersect( a, polygon ) || CGAL::do_intersect( b, polygon ) || CGAL::do_intersect( c, polygon );

	}

	void updateAngles( double angle1, double angle2, double angle3 )
	{
		this->mAngle1 = angle1;
		this->mAngle2 = this->mAngle1 + angle2;
		this->mAngle3 = this->mAngle2 + angle3;

		CalculatePointsOfSkt1();
		CalculatePointsOfSkt2();
		CalculatePointsOfSkt3();
	}

	void CalculatePointsOfSkt1()
	{
		MyPoint A1 = MyPoint((double)(this->mStartPosition.x),(double)(this->mStartPosition.y) );
		MyPoint B1 = MyPoint( (double)(A1.x+(double)(this->mLength1)*cos(this->mAngle1)), (double)(A1.y+(double)(this->mLength1)*sin(this->mAngle1)) );

		MyPoint A1_1 = MyPoint( A1.x - this->mWidth/2.0*cos(PI/2.0-this->mAngle1),
							A1.y + this->mWidth/2.0*sin(PI/2.0-this->mAngle1));
		MyPoint A1_2 = MyPoint( A1.x + this->mWidth/2.0*cos(PI/2.0-this->mAngle1),
						   	A1.y - this->mWidth/2.0*sin(PI/2.0-this->mAngle1));
		MyPoint B1_1 = MyPoint( B1.x - this->mWidth/2.0*cos(PI/2.0-this->mAngle1),
							B1.y + this->mWidth/2.0*sin(PI/2.0-this->mAngle1));
		MyPoint B1_2 = MyPoint( B1.x + this->mWidth/2.0*cos(PI/2.0-this->mAngle1),
							B1.y - this->mWidth/2.0*sin(PI/2.0-this->mAngle1));

		this->mPointsOfSkt1[0] = B1_1;
		this->mPointsOfSkt1[1] = A1_1;
		this->mPointsOfSkt1[2] = A1_2;
		this->mPointsOfSkt1[3] = B1_2;
	}

	void CalculatePointsOfSkt2()
	{

		MyPoint A2 = MyPoint(this->mStartPosition.x + this->mLength1*cos(mAngle1),
						 this->mStartPosition.y + this->mLength1*sin(mAngle1) );
		MyPoint B2 = MyPoint( A2.x+this->mLength2*cos(this->mAngle2), A2.y+this->mLength2*sin(this->mAngle2) );
		MyPoint A2_1 = MyPoint( A2.x - this->mWidth/2*cos(PI/2.0-this->mAngle2),
							A2.y + this->mWidth/2*sin(PI/2.0-this->mAngle2));
		MyPoint A2_2 = MyPoint( A2.x + this->mWidth/2*cos(PI/2.0-this->mAngle2),
						   	A2.y - this->mWidth/2*sin(PI/2.0-this->mAngle2));
		MyPoint B2_1 = MyPoint( B2.x - this->mWidth/2*cos(PI/2.0-this->mAngle2),
							B2.y + this->mWidth/2*sin(PI/2.0-this->mAngle2));
		MyPoint B2_2 = MyPoint( B2.x + this->mWidth/2*cos(PI/2.0-this->mAngle2),
							B2.y - this->mWidth/2*sin(PI/2.0-this->mAngle2));

		this->mPointsOfSkt2[0] = B2_1;
		this->mPointsOfSkt2[1] = A2_1;
		this->mPointsOfSkt2[2] = A2_2;
		this->mPointsOfSkt2[3] = B2_2;
	}

	void CalculatePointsOfSkt3()
	{
		MyPoint A3 = MyPoint(this->mStartPosition.x + this->mLength1*cos(mAngle1) + this->mLength2*cos(mAngle2),
						 this->mStartPosition.y + this->mLength1*sin(mAngle1) + this->mLength2*sin(mAngle2));
		MyPoint B3 = MyPoint( A3.x+this->mLength3*cos(this->mAngle3), A3.y+this->mLength3*sin(this->mAngle3) );
		MyPoint A3_1 = MyPoint( A3.x - this->mWidth/2*cos(PI/2.0-this->mAngle3),
							A3.y + this->mWidth/2*sin(PI/2.0-this->mAngle3));
		MyPoint A3_2 = MyPoint( A3.x + this->mWidth/2*cos(PI/2.0-this->mAngle3),
						   	A3.y - this->mWidth/2*sin(PI/2.0-this->mAngle3));
		MyPoint B3_1 = MyPoint( B3.x - this->mWidth/2*cos(PI/2.0-this->mAngle3),
							B3.y + this->mWidth/2*sin(PI/2.0-this->mAngle3));
		MyPoint B3_2 = MyPoint( B3.x + this->mWidth/2*cos(PI/2.0-this->mAngle3),
							B3.y - this->mWidth/2*sin(PI/2.0-this->mAngle3));

		this->mPointsOfSkt3[0] = B3_1;
		this->mPointsOfSkt3[1] = A3_1;
		this->mPointsOfSkt3[2] = A3_2;
		this->mPointsOfSkt3[3] = B3_2;
	}


private:
	MyPoint mStartPosition;
	double mWidth;

	double mLength1;
	double mLength2;
	double mLength3;

	// Angles to level
	double mAngle1;
	double mAngle2;
	double mAngle3;

	MyPoint mPointsOfSkt1[4];
	MyPoint mPointsOfSkt2[4];
	MyPoint mPointsOfSkt3[4];
};
