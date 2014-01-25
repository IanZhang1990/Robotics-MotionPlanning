import threading

class myTest:
	def __init__(self):
		self.count = 0;
		pass

	def foo(self):
		try:
			print "staring multithreading"
			for i in range( 1, 5):
				threading.Thread( target=self.mult, args = ([i]) ).start();
		except Exception, msg:
			print msg;

	def mult(self, i):
		self.count += 1;
		print self.count;
		print "value: " + str(i) + '\n'



test = myTest();
test.foo();