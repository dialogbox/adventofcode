import numpy as np

def improve(algo, input, background):
  image = np.array([[1 if c == '#' else 0 for c in l] for l in input])

  height, width = image.shape
  # expend
  nimage = np.empty(shape=(height+6, width+6))
  nimage[:] = background
  nimage[3:height+3, 3:width+3] = image

  height, width = nimage.shape

  conv = np.array([["".join(np.char.mod('%d',(nimage[y-1:y+2, x-1:x+2].reshape(1,9)[0]))) for x in range(1,width-1) ] for y in range(1,height-1)])

  image = np.array([[algo[int(i,2)] for i in l] for l in conv])

  return image[1:-1, 1:-1]

def print_image(image):
  print("--------------------")
  print("\n".join(["".join(l) for l in image]))

def next_background(b0, b511):
  if b0 == '.':
    while True:
      yield 0
  elif b0 == '#' and b511 == '.':
    while True:
      yield 0
      yield 1
  else:
    yield 0
    while True:
      yield 1

def parse_input(path):
  f = open(path, 'r')
  algo = f.readline().strip()
  f.readline()
  image = np.array([[c for c in l.strip()] for l in f])

  return algo, image

def improve_n(algo, image, n):
  backgroud_iter = next_background(algo[0], algo[-1])

#  print_image(image)
  for i in range(n):
    image = improve(algo, image, next(backgroud_iter))

#  print_image(image)

  print(len(image[image == '#']))

def part1(path):
  algo, image = parse_input(path)

  improve_n(algo, image, 2)

def part2(path):
  algo, image = parse_input(path)

  improve_n(algo, image, 50)