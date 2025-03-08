import argparse
import csv
import numpy

def classify(instance, mu, sigma, pc):
  pci = [[0, 0], [0, 0]]
  for ci in range(2):
    for a in range(2):
      f1 = (1/(2*numpy.pi*sigma[ci][a])**(1/2))

      f2 = float(instance[a+1]) - mu[ci][a]
      f2 = -(f2**2)/(2*sigma[ci][a])
      f2 = numpy.exp(f2)

      pci[ci][a] = f1 * f2
  
  if pc[0]*pci[0][0]*pci[0][1] >= pc[1]*pci[1][0]*pci[1][1]:
    return 0
  else:
    return 1

# make the string classes A and B to int 0 and 1
def cast(c):
  if c == 'A':
    return 0
  elif c == 'B':
    return 1
  else:
    print("ERROR in cast()")

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data', type=argparse.FileType('r'))
  args = parser.parse_args()
  
  data = []
  # form csv to an array          
  reader = csv.reader(args.data)
  for row in reader:
    data.append(row)

  splitData = [[], []]

  for item in data:
    splitData[cast(item[0])].append(item)

  nc = [len(splitData[0]), len(splitData[1])]
  pc = [nc[0]/(nc[0] + nc[1]),
        nc[1]/(nc[0] + nc[1])]

  mu = [[0, 0], [0, 0]] 
  for i in data:
    mu[cast(i[0])][0] += float(i[1])
    mu[cast(i[0])][1] += float(i[2])
  
  for ci in range(len(mu)):
    mu[ci][0] *= 1/nc[ci]
    mu[ci][1] *= 1/nc[ci]

  sigma = [[0, 0], [0, 0]] 
  for i in data:
    sigma[cast(i[0])][0] += ( float(i[1]) - mu[cast(i[0])][0] )**2 
    sigma[cast(i[0])][1] += ( float(i[2]) - mu[cast(i[0])][1] )**2 
  
  for ci in range(len(mu)):
    sigma[ci][0] *= 1/(nc[ci] - 1)
    sigma[ci][1] *= 1/(nc[ci] - 1)
  
  print("{},{},{},{},{}".format(mu[0][0], sigma[0][0], mu[0][1], sigma[0][1], pc[0]))
  print("{},{},{},{},{}".format(mu[1][0], sigma[1][0], mu[1][1], sigma[1][1], pc[1]))

  total = 0
  for i in data:
    c = classify(i, mu, sigma, pc)
    if c != cast(i[0]):
      total += 1

  print(total)
if __name__=="__main__":
  main()