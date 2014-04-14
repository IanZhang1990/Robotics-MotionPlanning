import math;

def euclideanDist( config1, config2 ):
    length = len(config1);
    if( len(config1) != len(config2) ):
        raise Exception(" Your data should be in the same dimension ");

    dist = 0;
    for i in range(0, length):
        dist += (config1[i] - config2[i]) ** 2;
    return math.sqrt( dist );

def euclideanDistSqr( config1, config2 ):
    length = len(config1);
    if( len(config1) != len(config2) ):
        raise Exception(" Your data should be in the same dimension ");

    dist = 0;
    for i in range(0, length):
        dist += (config1[i] - config2[i]) ** 2;
    return ( dist );

def ChebyshevDist( config1, config2 ):
    length = len(config1);
    if( len(config1) != len(config2) ):
        raise Exception(" Your data should be in the same dimension ");

    dist = [0] * length;
    for i in range(0, length):
        dist[i] = (config1[i] - config2[i]);
    return max(dist);

def add( config1, config2 ):
    length = len(config1);
    if( len(config1) != len(config2) ):
        raise Exception(" Your data should be in the same dimension ");

    result = [0] * length;
    for i in range(0, length):
        result[i] = config1[i] + config2[i];

    return result;

def devide( config, value ):
    """Devide a vector by a number"""
    if( value == 0 ):
        raise Exception( "Can't devide by 0" );
    length = len(config);

    result = [0]*length;
    for i in range(0, length):
        result[i] = config[i] / value;

    return result;

def sphereLineCollision( center, radius, end1, end2 ):
    dist = point2LineDist( center, end1, end2 );
    if( dist > radius ):
        return False;
    else:
        return True;
 
def point2LineDist( point, end1, end2):
    """Distance from one point to a segment of line ( end1 --> end2 )"""
    # Ref: http://blog.csdn.net/freezhanacmore/article/details/9568873
    ab = ( end2[0] - end1[0], end2[1] - end1[1]);
    ac = ( point[0]- end1[0], point[1]-end1[1] );
    bc = ( point[0]- end2[0], point[1]-end2[1] )
        
    if( ab[0]*ac[0]+ab[1]*ac[1] < 0 ):
        return math.sqrt( ac[0]**2 + ac[1]**2 );
    elif( ab[0]*bc[0]+ab[1]*bc[1] > 0 ):
        return math.sqrt( bc[0]**2 + bc[1]**2 );
    else:
        return math.fabs( ab[0]*ac[1]-ab[1]*ac[0] ) / math.sqrt( ab[0]**2 + ab[1]**2 );