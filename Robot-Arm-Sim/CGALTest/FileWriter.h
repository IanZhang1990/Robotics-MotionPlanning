#ifndef __FILEWRITER__
#define __FILEWRITER__

// basic file operations
#include <iostream>
#include <fstream>
using namespace std;

class FileWriter
{
public:
	FileWriter()
	{
		this->mFileStreamCollide.open( "Collision.txt", std::ios_base::out );
		this->mFileStreamFree.open( "Free.txt", std::ios_base::out );
	}

	void addData( float a, float b, float c )
	{
		std::stringstream s;
		s << setprecision(6) << a << "\t\t" << b << "\t\t" << c << '\n';
		string str = s.str();
		this->mFileStreamFree << str;
	}

	void addData( float a, float b, float c, float d )
	{
		std::stringstream s;
		s << setprecision(6) << a << "\t\t" << b << "\t\t" << c << "\t\t" << d << '\n';
		string str = s.str();
		this->mFileStreamCollide << str;
	}

	void flush()
	{
		this->mFileStreamCollide.flush();
		this->mFileStreamCollide.close();
		this->mFileStreamFree.flush();
		this->mFileStreamFree.close();
	}

private:
	ofstream mFileStreamCollide;
	ofstream mFileStreamFree;
};

#endif
