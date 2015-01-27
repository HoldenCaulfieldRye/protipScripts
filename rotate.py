#!/usr/bin/env python
import sys, os, shutil
import subprocess
import math
from PIL import Image

def interpret(argv):
  rand, noBlack = False, False
  angles, imgPaths = [], []
  with open(argv[1], 'r') as f:
    imgPaths = f.readlines()
    imgPaths = [line.strip() for line in imgPaths]
  if argv[2].startswith('--rand'):
    rand = True
    str_angle = argv[2].split('=')[-1]
    angles.append(int(str_angle))
  else:
    angles = [int(ang) for ang in argv[2].split(',')]  
  if '--noBlack' in sys.argv:
    noBlack = True
  return imgPaths, angles, noBlack

def rotate(candPaths, angles, noBlack):
  rezPaths = []
  for imgPath in candPaths:
    print "rotating %s..." % (imgPath)
    img = Image.open(imgPath)
    for angle in angles:
      rotImg = rotate_image(img, angle)
      
def rotate_image(img, imgName, angle, bothClock, noBlack):
  rotatedImg = img.rotate(angle)
  rotatedImg.save(dirRez + '/' + imgName.replace('.jpg','_'+str(angle)+'.jpg'), 'JPEG')
  if noBlack:
    w, h = img.size
    wr, hr = rotatedRectWithMaxArea(w, h, math.radians(angle))
    # print "weight %i height %i, then weight %i height %i" % (w, h, wr, hr)
    # sys.exit()
    dh_w, dh_h = int((w-wr)/2), int((h-hr)/2)
    rotatedImg.crop((dh_w, dh_h, w - dh_w, h - dh_h)).save(dirRez + '/' + imgName.replace('.jpg','_'+str(angle)+'nb.jpg'), 'JPEG')
  # if bothClock:
  #   # this aint going to work, img will just go back to normal?
  #   arotatedImg = img.rotate(-angle)
  #   arotatedImg.save(dirRez + '/' + imgName.replace('.jpg','_a'+str(angle)+'.jpg'), 'JPEG')

def rotatedRectWithMaxArea(w, h, angle):
  """ bit.ly/1ELj9ZB
  Given a rectangle of size wxh that has been rotated by 'angle' (in
  radians), computes the width and height of the largest possible
  axis-aligned rectangle (maximal area) within the rotated rectangle.
  """  
  if w <= 0 or h <= 0:
    return 0,0
  width_is_longer = w >= h
  side_long, side_short = (w,h) if width_is_longer else (h,w)
  # since the solutions for angle, -angle and 180-angle are all the same,
  # if suffices to look at the first quadrant and the absolute values of sin,cos:
  sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
  if side_short <= 2.*sin_a*cos_a*side_long:
    # half constrained case: two crop corners touch the longer side,
    #   the other two corners are on the mid-line parallel to the longer line
    x = 0.5*side_short
    wr,hr = (x/sin_a,x/cos_a) if width_is_longer else (x/cos_a,x/sin_a)
  else:
    # fully constrained case: crop touches all 4 sides
    cos_2a = cos_a*cos_a - sin_a*sin_a
    wr,hr = (w*cos_a - h*sin_a)/cos_2a, (h*cos_a - w*sin_a)/cos_2a
  return wr,hr

def roll(image, delta):
  "Roll an image sideways"
  xsize, ysize = image.size
  delta = delta % xsize
  if delta == 0: return image
  part1 = image.crop((0, 0, delta, ysize))
  part2 = image.crop((delta, 0, xsize, ysize))
  image.paste(part2, (0, 0, xsize-delta, ysize))
  image.paste(part1, (xsize-delta, 0, xsize, ysize))
  return image


def get_stats():
  pass

def get_help():
  print '''usage e.g.
  ./rotation.py imgPaths.txt  --rand=maxA [--noBlack]
  ./rotation.py imgPaths.txt  3,-7,15     [--noBlack]
  (option1: uniform random rotations with max angle)
  (option2: specific angles, in degrees clockwise)'''


if __name__ == '__main__':
  print sys.argv
  if len(sys.argv) < 3:
    get_help()
    sys.exit()

  candPaths, angles, noBlack = interpret(sys.argv)
  print "candPaths, angles, noBlack:", candPaths[:3], angles, noBlack
  sys.exit()
  rezPaths = rotate(candPaths, angles, noBlack)

  for path in rezPaths:
    print path
