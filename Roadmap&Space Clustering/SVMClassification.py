import sys
import os
from subprocess import *

from libsvm.python.svmutil import *
from libsvm.python.svm import *


is_win32 = (sys.platform == 'win32')
if not is_win32:
	svmscale_exe = "libsvm/svm-scale"
	svmtrain_exe = "libsvm/svm-train"
	svmpredict_exe = "libsvm/svm-predict"
	grid_py = "libsvm/tools/grid.py"
	gnuplot_exe = "/usr/local/bin/gnuplot"
else:
	quit()

assert os.path.exists(svmscale_exe),"svm-scale executable not found"
assert os.path.exists(svmtrain_exe),"svm-train executable not found"
assert os.path.exists(svmpredict_exe),"svm-predict executable not found"
assert os.path.exists(gnuplot_exe),"gnuplot executable not found"
assert os.path.exists(grid_py),"grid.py not found"



class SVMClassifier:
	def __init__(self):
		self.SVMModel = None
		pass

	def train(self, filename):
		assert os.path.exists(filename),"training file not found"
		self.TrainFilePath  = filename
		self.ScaledFile 	= self.TrainFilePath + ".scale"
		self.ModelFile 		= self.TrainFilePath + ".model"
		self.RangeFile 		= self.TrainFilePath + ".range"

		cmd = '{0} -s "{1}" "{2}" > "{3}"'.format(svmscale_exe, self.RangeFile, self.TrainFilePath, self.ScaledFile)
		print('Scaling training data...')
		Popen(cmd, shell = True, stdout = PIPE).communicate()

		cmd = '{0} -svmtrain "{1}" -gnuplot "{2}" "{3}"'.format(grid_py, svmtrain_exe, gnuplot_exe, self.ScaledFile)
		print('Cross validation...')
		f = Popen(cmd, shell = True, stdout = PIPE).stdout

		line = ''
		while True:
			last_line = line
			line = f.readline()
			if not line: break
		c,g,rate = map(float,last_line.split())

		print('Best c={0}, g={1} CV rate={2}'.format(c,g,rate))

		cmd = '{0} -c {1} -g {2} "{3}" "{4}"'.format(svmtrain_exe,c,g,self.ScaledFile,self.ModelFile)
		print('Training...')
		Popen(cmd, shell = True, stdout = PIPE).communicate()
		print('Output model: {0}'.format(self.ModelFile))
		
		# Read range file and record data range
		self.readRangeFile();

		# Load model into memory
		self.SVMModel = svm_load_model( self.ModelFile )

	def readRangeFile(self):
		###############################################
		# Get range information from range file
		###############################################
		range_file = open( self.RangeFile, 'r' )
		range_file.readline()
		ranges = range_file.readline().split(' ')
		self.Range = ( int(ranges[0]), int(ranges[1]))
		#----------------------------------------------
		range_1 = range_file.readline()
		ranges = range_1.split(' ')
		self.MinX1 = int(ranges[1])
		self.MaxX1 = int(ranges[2])
		#----------------------------------------------
		range_2 = range_file.readline()
		ranges = range_2.split(' ')
		self.MinY1 = int(ranges[1])
		self.MaxY1 = int(ranges[2])
		#----------------------------------------------
		range_3 = range_file.readline()
		ranges = range_2.split(' ')
		self.MinX2 = int(ranges[1])
		self.MaxX2 = int(ranges[2])
		range_4 = range_file.readline()
		ranges = range_4.split(' ')
		self.MinY2 = int(ranges[1])
		self.MaxY2 = int(ranges[2])
		range_file.close();
	
	def loadSVMModel( self, filepath ):
		# Load model into memory
		self.SVMModel = svm_load_model( filepath )


	def predict(self, one_data ):
		if self.SVMModel == None:
			print("No SVM Model loaded")
			return

		if( len( one_data ) != 4 ):
			print( "Illegal data" )
			return;

		val1 = float(self.Range[0]) + float( self.Range[1] - self.Range[0] ) * float( one_data[0] - self.MinX1 ) / ( self.MaxX1 - self.MinX1 )
		val2 = float(self.Range[0]) + float( self.Range[1] - self.Range[0] ) * float( one_data[1] - self.MinY1 ) / ( self.MaxY1 - self.MinY1 ) 
		val3 = float(self.Range[0]) + float( self.Range[1] - self.Range[0] ) * float( one_data[2] - self.MinX2 ) / ( self.MaxX2 - self.MinX2 )
		val4 = float(self.Range[0]) + float( self.Range[1] - self.Range[0] ) * float( one_data[3] - self.MinY2 ) / ( self.MaxY2 - self.MinY2 ) 

		#x, maxid = gen_svm_nodearray( [val1,val2,val3,val4] )
		#x = [svm_node(1, one_data[0]), svm_node(2, one_data[1])]
		#y = libsvm.svm_predict( self.SVMModel, x )
		xi = [[val1,val2,val3,val4]]
		label, acc, val = svm_predict( [0], xi, self.SVMModel )
		return label, acc, val
