import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

class Node(object):
    def __init__(self, id):
        super().__init__()
        self.id = id
    

def main():
    d = dict()
    nod = Node(1)
    if nod not in d:
        d[nod] = 1
    else:
        d[nod]+= 2
    print(d[nod])

if __name__ == '__main__':
    main()