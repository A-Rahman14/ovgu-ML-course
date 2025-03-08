import numpy
import argparse
import csv


def get_gradient(w, x, y, fx, eta):
    gradient = x * (y - fx)
    gradient = numpy.sum(gradient, axis=0)
    gradient = numpy.array([float("{0:.4f}".format(val)) for val in gradient])
    temp = numpy.array(eta * gradient).reshape(w.shape)
    w = w + temp
    return gradient, w


def get_sse(y, fx):
    return numpy.sum(numpy.square(fx - y))


def get_predicted_value(x, w):
    return numpy.dot(x, w)


def main():
    args = parser.parse_args()
    file, eta, threshold = args.data, float(args.eta), float(args.threshold)
    with open(file) as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        x = []
        y = []
        for row in reader:
            x.append([1.0] + row[:-1])
            y.append([row[-1]])

    x = numpy.array(x).astype(float)
    y = numpy.array(y).astype(float)
    w = numpy.zeros(x.shape[1]).astype(float)
    w = w.reshape(x.shape[1], 1)
    fx = get_predicted_value(x, w)
    sse_old = get_sse(y, fx)
    print(*[0], *["{0:}".format(val) for val in w.T[0]], *["{0:}".format(sse_old)])
    gradient, w = get_gradient(w, x, y, fx, eta)
    iteration = 1
    while True:
        fx = get_predicted_value(x, w)
        sse_new = get_sse(y, fx)
        if abs(sse_new - sse_old) > threshold:
            print(
                *[iteration], *["{0:}".format(val) for val in w.T[0]], *["{0:}".format(sse_new)])
            gradient, w = get_gradient(w, x, y, fx, eta)
            iteration += 1
            sse_old = sse_new
        else:
            break
    print(*[iteration], *["{0:}".format(val) for val in w.T[0]], *["{0:}".format(sse_new)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", help="data file")
    parser.add_argument("-e", "--eta", help="eta")
    parser.add_argument("-t", "--threshold", help="threshold")
    main()

