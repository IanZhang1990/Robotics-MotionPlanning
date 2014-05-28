
import math

def g(phi1, phi2):
	if( math.fabs(phi1-phi2) < math.pi ):
		return math.fabs(phi1-phi2);
	else:
		return math.pi - math.fabs(phi1-phi2);

def cost(x, y, phi):
	startAngl = phi; #math.pi/4;
	length = math.sqrt(x**2+y**2);
	pathAngl = math.atan2(y,x);

	if( pathAngl <= -math.pi+ startAngl ):
		return length + g(phi, 0);
	elif( pathAngl < 0 and pathAngl >= (-math.pi + startAngl) ):
		if( pathAngl <= startAngl - math.pi/2 ):
			theta = math.pi - math.fabs(pathAngl) - startAngl;
			d = length * math.sin( theta ); 
			return d/2*math.pi + math.fabs( length*math.cos(theta) - d ) + g(phi, 0);
		else:
			theta = math.pi - startAngl;
			d = math.fabs(y) / math.sin( theta );
			return d/2*math.pi + d + math.fabs( x - math.fabs(y)/math.tan(theta) ) + g(phi, 0);
		
	elif( pathAngl == 0 ):
		return length + g(phi, 0);
	elif( pathAngl > 0 and pathAngl <= startAngl ):
		return length + g(phi, 0);
	elif( pathAngl > startAngl ):
		if( pathAngl <= startAngl + math.pi/2 ):
			theta = pathAngl - startAngl;
			d = length * math.sin( theta );
			return d/2*math.pi + math.fabs( length*math.cos(theta) - d ) + g(phi, 0);
		else:
			theta = math.pi/2 - startAngl;
			d = y / math.sin(theta);
			return d/2*math.pi + d + math.fabs( math.fabs(x) - y/math.tan(theta) ) + g(phi, 0);
		

def main():
	data = [];

	for i in range( -60, 60 ):
		for j in range( -60,60 ):
			x = float(i) / 30.0;
			y = float(j) / 30.0;
			c = cost( x, y, math.pi/3 );
			data.append( (x,y,c) );
	
	f = open('costValue.txt', 'w');
	f.write("# X\tY\tCost\n");
	for element in data:
		f.write( '{0}\t{1}\t{2}\n'.format( element[0],element[1],element[2] ) );
	f.close();
	pass;

if __name__ == "__main__":
	main();