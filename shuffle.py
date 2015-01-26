#!/usr/bin/env python
import sys
import numpy as np
from numpy import random

def shuffle(source):
  with open(source, 'r') as f1:
    content = f1.readlines()
    content = [line.strip() for line in content]
    npLines = np.array(content)
    random.shuffle(npLines)
    listLines = list(npLines)
  return listLines

def shuffle_and_overwrite(source_and_dest):
  listLines = shuffle(source_and_dest)
  f = open(source_and_dest, 'w')
  f.write('\n'.join(listLines))
  f.close()

def get_help():
  print '''usage: e.g.
  ./shuffle.py file
  (shuffled contents will be output to stdout)

  ./shuffle.py -i file
  (file will be overwritten by its shuffle)'''
  sys.exit()

if __name__ == '__main__':
  if sys.argv[1] == '-i':
    if len(sys.argv) == 3:
      shuffle_and_overwrite(sys.argv[2])
    else:
      get_help()

  elif len(sys.argv) != 2:
    get_help()

  else:
    listLines = shuffle(sys.argv[1])
    for line in listLines:
      print line
  
