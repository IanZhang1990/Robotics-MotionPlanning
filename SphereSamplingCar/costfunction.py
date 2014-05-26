
import math

def cost(x,y):
	startAngl = math.pi/4;
	goalAngl = 0;
	length = math.sqrt(x**2 + y**2);
	pathAngl = math.atan2(y,x);

	if( math.fabs(pathAngl) - startAngl == 0 ):
		return length + math.pi/4;
	elif( pathAngl < 0 and math.fabs(pathAngl) - startAngl > 0 ):
		theta = math.fabs(pathAngl) - startAngl;
		if theta > math.pi/2:
			theta = math.pi/2 - theta;
		d = length * math.sin( theta );
		return d/2*math.pi + math.fabs( length*math.cos(theta) - d ) + math.pi/4;
	elif( math.fabs(pathAngl) - startAngl < 0 ):
		return length + math.pi/4;
	elif( pathAngl == 0 ):
		return length + math.pi/4;
	elif( pathAngl > 0 and math.fabs(pathAngl) - startAngl > 0 ):
		theta = math.fabs(pathAngl) - startAngl;
		if theta > math.pi/2:
			theta = math.pi/2 - theta;
		d = length * math.sin( theta );
		return d/2*math.pi + math.fabs( length*math.cos(theta) - d ) + math.pi/4;

def main():
	data = [];

	for i in range( 0, 40 ):
		for j in range( 0,40 ):
			x = float(i) / 20.0;
			y = float(j) / 20.0;
			c = cost( x, y );
			data.append( (x,y,c) );

	f = open('costValue.txt', 'w');
	f.write("# X\tY\tCost\n");
	for element in data:
		f.write( '{0}\t{1}\t{2}\n'.format( element[0],element[1],element[2] ) );
	f.close();
	pass;

if __name__ == "__main__":
	main();