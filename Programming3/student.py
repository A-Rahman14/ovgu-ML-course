import argparse
import csv
import math


def neuralNetwork(file, eta, times):
    w_bias_h1 = 0.20000
    w_a_h1 = -0.30000
    w_b_h1 = 0.40000
    w_bias_h2 = -0.50000
    w_a_h2 = -0.10000
    w_b_h2 = -0.40000
    w_bias_h3 = 0.30000
    w_a_h3 = 0.20000
    w_b_h3 = 0.10000
    w_bias_o = -0.10000
    w_h1_o = 0.10000
    w_h2_o = 0.30000
    w_h3_o = -0.40000

    i = 0
    while i < times:
        for instance in file:
            a, b, t = instance[0], instance[1], instance[2]

            h1_net = net(a, w_a_h1, b, w_b_h1, w_bias_h1)
            h1 = activation(h1_net)
            h2_net = net(a, w_a_h2, b, w_b_h2, w_bias_h2)
            h2 = activation(h2_net)
            h3_net = net(a, w_a_h3, b, w_b_h3, w_bias_h3)
            h3 = activation(h3_net)

            o_net = h1 * w_h1_o + h2 * w_h2_o + h3 * w_h3_o + w_bias_o
            o = activation(o_net)

            delta_o = o * (1 - o) * (t - o)
            delta_h1 = h1 * (1 - h1) * w_h1_o * delta_o
            delta_h2 = h2 * (1 - h2) * w_h2_o * delta_o
            delta_h3 = h3 * (1 - h3) * w_h3_o * delta_o

            w_bias_h1 += eta * delta_h1
            w_a_h1 += eta * delta_h1 * a
            w_b_h1 += eta * delta_h1 * b
            w_bias_h2 += eta * delta_h2
            w_a_h2 += eta * delta_h2 * a
            w_b_h2 += eta * delta_h2 * b
            w_bias_h3 += eta * delta_h3
            w_a_h3 += eta * delta_h3 * a
            w_b_h3 += eta * delta_h3 * b
            w_bias_o += eta * delta_o
            w_h1_o += eta * delta_o * h1
            w_h2_o += eta * delta_o * h2
            w_h3_o += eta * delta_o * h3

            print(a, ", ", b, ", ", h1, ", ", h2, ", ", h3, ", ", o, ", ", t, ", ",
                  delta_h1, ", ", delta_h2, ", ", delta_h3, ", ", delta_o, ", ",
                  w_bias_h1, ", ", w_a_h1, ", ", w_b_h1, ", ",
                  w_bias_h2, ", ", w_a_h2, ", ", w_b_h2, ", ",
                  w_bias_h3, ", ", w_a_h3, ", ", w_b_h3, ", ",
                  w_bias_o, ", ", w_h1_o, ", ", w_h2_o, ", ", w_h3_o)
        i += 1



def activation(_net):
    return 1 / (1 + math.exp(-1 * _net))


def net(a, w_a, b, w_b, w_bias):
    return (a * w_a) + (b * w_b) + w_bias


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data")
    parser.add_argument("--eta", type=float)
    parser.add_argument("--iterations", type=int)
    file = open(parser.parse_args().data)
    csvreader = list(csv.reader(file))

    print ("a,b,h1,h2,h3,o,t,delta_h1,delta_h2,delta_h3,delta_o,w_bias_h1,w_a_h1,w_b_h1,w_bias_h2,w_a_h2,w_b_h2,w_bias_h3,w_a_h3,w_b_h3,w_bias_o,w_h1_o,w_h2_o,w_h3_o")
    print ("-,-,-,-,-,-,-,-,-,-,-, 0.20000, -0.30000, 0.40000, -0.50000, -0.10000, -0.40000, 0.30000, 0.20000, 0.10000, -0.10000, 0.10000, 0.30000, -0.40000")

    for i in csvreader:
        i[0] = float(i[0])
        i[1] = float(i[1])
        i[2] = float(i[2])

    neuralNetwork(csvreader, parser.parse_args().eta, parser.parse_args().iterations)

    file.close()
