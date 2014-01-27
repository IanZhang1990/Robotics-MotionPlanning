import time, datetime;
from multiprocessing import Process, Manager, Value

class test:
    def __init__(self, val):
        self.Val = val;

if __name__ == "__main__":
    
    begin = datetime.datetime.now()
    end = datetime.datetime.now();
    timeCost = end-begin;
    print "Cool: {0}".format(timeCost)