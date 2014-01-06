import sys
import os
from subprocess import *

from SVMClassification import *


g_SVMModelFile = "path.txt.model"
g_rangeFile = "path.txt.range"
g_testDataList = []

def loadTestData( filepath ):
	storeList = []
	testFile = open( filepath, 'r' )
	#########################################
	### The test file should have the format:
	###  1,2,3,4
	###  50,50,100,100
	###--------------------------------------
	while True:
		readLine = testFile.readline();
		if not readLine:
			# EOF reached
			break;

		strData = readLine.split(',');
		storeList = storeList + [(int(strData[0]),int(strData[1]),int(strData[2]),int(strData[3]))]
		pass

	return storeList;

if __name__ == "__main__":
	classifier = SVMClassifier();
	classifier.readRangeFile( g_rangeFile );
	classifier.loadSVMModel( g_SVMModelFile );

	g_testDataList = loadTestData( "2DtestData.txt" );

	for data in g_testDataList:
		label, acc, val = classifier.predict( data )
		ifFeasible = "";
		if label==1:
			ifFeasible = "Feasible"
		else:
			ifFeasible = "Infeasible"

		print( "Testing: {0}".format( data ) );
		print( "Result: {0} path, accuracy:{1}\t value: {2}".format( ifFeasible, acc, val ) );