
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
