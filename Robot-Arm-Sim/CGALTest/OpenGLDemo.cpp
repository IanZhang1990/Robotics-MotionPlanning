//  CGAL 2D Polygon Example from CGAL 3.4 Distribution
//  with OpenGL GUI OpenGL

#include <stdlib.h>
#include <math.h>
#include <stdio.h>
#include <GL/glut.h>  // for the OpenGL GLUT library
/*
#include <math.h>

// CGAL header files

//#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Boolean_set_operations_2.h>

#include <list>

#include "RobotArm.h"

using std::cout;
using std::endl;

RobotArm robotArm(MyPoint(400.0,300.0),100, 100, 100);

MyPoint points1[] = { MyPoint(400+40,250+10), MyPoint(400,250+10), MyPoint(400,250), MyPoint(400+40,250)};
MyPoint points2[] = { MyPoint(460+40,250+10), MyPoint(460,250+10), MyPoint(460,250), MyPoint(460+40,250)};
MyPoint points3[] = { MyPoint(400+40,370+30), MyPoint(400,370+30), MyPoint(400,370), MyPoint(400+40,370)};
MyPoint points4[] = { MyPoint(270+40,290+10), MyPoint(270,290+10), MyPoint(270,290), MyPoint(270+40,290)};
MyPoint points5[] = { MyPoint(470+40,300+50), MyPoint(470,300+50), MyPoint(470,300), MyPoint(470+40,300)};
MyPoint points6[] = { MyPoint(350+40,100+50), MyPoint(350,100+50), MyPoint(350,100), MyPoint(350+40,100)};
MyPoint points7[] = { MyPoint(350+40,190+10), MyPoint(350,190+10), MyPoint(350,190), MyPoint(350+40,190)};
MyPoint points8[] = { MyPoint(320+100,210+20), MyPoint(320,210+20), MyPoint(320,210), MyPoint(320+100,210)};


Point points1_1[] = { Point(points1[0].x,points1[0].y), Point(points1[1].x,points1[1].y),Point(points1[2].x,points1[2].y),Point(points1[3].x,points1[3].y)};




Polygon2d poly1 = Polygon2d(points1_1, points1_1+4);



float angle1 = 0.0f;

void myDisplay()
{
  // Display polygon and 2 test points using OpenGL

  glClear(GL_COLOR_BUFFER_BIT);

  glColor3f(1.0f, 0.0f, 0.0f);
  glBegin(GL_QUADS);
  for( int i=0; i < 4; i++ )
	  glVertex2f( points1[i].x,points1[i].y );
  glEnd();
  glBegin(GL_QUADS);
  for( int i=0; i < 4; i++ )
	  glVertex2f( points2[i].x,points2[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
  	  glVertex2f( points3[i].x,points3[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
   	  glVertex2f( points4[i].x,points4[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
  	  glVertex2f( points5[i].x,points5[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
  	  glVertex2f( points6[i].x,points6[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
   	  glVertex2f( points7[i].x,points7[i].y );
  glEnd();
  glBegin(GL_QUADS);
    for( int i=0; i < 4; i++ )
  	  glVertex2f( points8[i].x,points8[i].y );
  glEnd();
  robotArm.updateAngles( angle1, angle1, angle1 );
  robotArm.render();


  //if( robotArm.collideWith( poly1 ) )
	//  cout << "Collide!" << endl;

  angle1 += 0.0002;
  glFlush();
}


int main(int argc, char **argv)
{
	// Set up simple 2D OpenGL environment.
   glutInit(&argc, argv);
   glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB | GLUT_DEPTH);
   glutInitWindowSize(800, 600);
   glutInitWindowPosition(50,50);
   glutCreateWindow("91.504 Simple CGAL Test");
   glutDisplayFunc(myDisplay);
   glutIdleFunc(myDisplay);
   glClearColor(0.0, 0.0, 1.0, 0.0);
   glColor3f(1.0f, 0.0f, 0.0f);
   glPointSize(2.0);
   glLineWidth(4.0);
   glMatrixMode(GL_PROJECTION);
   glLoadIdentity();
   gluOrtho2D(0.0, 800.0, 0.0, 600.0);

   glutMainLoop();
	return 0;
}
*/
