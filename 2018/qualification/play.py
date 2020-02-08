import sys
import math
from time import gmtime, strftime
sys.dont_write_bytecode = True

def main():
  print(sys.argv)
  if len(sys.argv)>1:
    fw = open(" ".join([sys.argv[1].split('.')[0], strftime("%H:%M:%S", gmtime()), ".txt"]),'w')
    with open(sys.argv[1], 'r') as fr:
        R, C, F, N, B, T = list(map(int, fr.readline().split()))
        for i in range(N):
            line = list(map(int, fr.readline().split()))
            print(line)
            fw.write(" ".join([str(elem) for elem in line])+'\n')
        fr.close()
        fw.close()
    




if __name__ == '__main__':
    main()