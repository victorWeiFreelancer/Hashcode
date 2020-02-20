import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

def coef(r, n):
    return 12*(1 - 1/( (1+r/12)**(12*n)))/r

def main():
    L = 370000
    p = L/coef(0.016, 25)
    print(p)



if __name__ == '__main__':
    main()