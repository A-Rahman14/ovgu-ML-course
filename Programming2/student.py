import numpy
import argparse
import csv

data = []
atts_ = []
root = []


def build_tree(attributes, depth, att_in_node):
    data_print = [depth, att_in_node, entropy(attributes), "no_leaf"]

    if (entropy(attributes) < 0.0000001) or depth >= len(atts_) - 1:
        data_print[-1] = atts_[-1][which_class(attributes)]
        print(data_print[0], ",", data_print[1], ",", data_print[2], ",", data_print[3])
    else:
        print(data_print[0], ",", data_print[1], ",", data_print[2], ",", data_print[3])
        ai = choose_next_att(attributes)
        splits = []
        for att_val in atts_[ai]:
            temp = attributes.copy()
            temp[ai] = att_val
            splits.append(temp)
        for split_ind in range(len(splits)):
            build_tree(splits[len(splits) - 1 - split_ind], depth + 1,
                       "att{}={}".format(ai, splits[len(splits) - 1 - split_ind][ai]), )


def entropy(attributes, with_total_number=False):
    class_number = len(atts_[-1])
    class_instances_count = []
    for x in range(class_number):
        class_instances_count.append(0)
    for instance in data:
        suites_attributes = True
        for att_val_ind in range(len(instance) - 1):
            if attributes[att_val_ind] == "\n":
                continue
            elif attributes[att_val_ind] != instance[att_val_ind]:
                suites_attributes = False
        if suites_attributes:
            class_instances_count[atts_[-1].index(instance[-1])] += 1
    total = 0
    for number in class_instances_count:
        total += number
    entropy_value = 0
    for number in class_instances_count:
        if number != 0:
            entropy_value += (number / total * (numpy.log(number / total) / numpy.log(class_number)))
    entropy_value *= -1
    if with_total_number:
        return [entropy_value, total]
    else:
        return entropy_value


def which_class(attributes):
    distribution = []
    for x in range(len(atts_[-1])):
        distribution.append(0)

    for instance in data:
        suites_attributes = True
        for att_val_ind in range(len(instance) - 1):
            if attributes[att_val_ind] == "\n":
                continue
            elif attributes[att_val_ind] != instance[att_val_ind]:
                suites_attributes = False
        if suites_attributes:
            distribution[atts_[-1].index(instance[-1])] += 1

    return numpy.argmax(distribution)


def choose_next_att(attributes):
    highest_gain = [gain(attributes, 0), 0]
    for x in range(1, len(atts_) - 1):
        current_gain = gain(attributes, x)
        if current_gain > highest_gain[0]:
            highest_gain = [current_gain, x]

    return highest_gain[1]


def gain(attributes, next_att_ind):
    entropy_s = entropy(attributes, True)
    entropies_of_attribute = []
    for att_val in atts_[next_att_ind]:
        new_node = attributes.copy()
        new_node[next_att_ind] = att_val
        entropies_of_attribute.append(entropy(new_node, True))
    gain_ = entropy_s[0]
    for entropy_si in entropies_of_attribute:
        gain_ -= (entropy_si[1] / entropy_s[1]) * entropy_si[0]
    return gain_


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=argparse.FileType("r"))
    args = parser.parse_args()
    reader = csv.reader(args.data)
    for row in reader:
        data.append(row)
    highest_length = 0
    for item in data:
        if len(item) > highest_length:
            highest_length = len(item)
    for item in data:
        if len(item) < highest_length:
            data.remove(item)
    for i in range(len(data[0])):
        atts_.append([])
    for instance_index in range(len(data)):
        for att_index in range(len(data[instance_index])):
            if atts_[att_index].count(data[instance_index][att_index]) == 0:
                atts_[att_index].append(data[instance_index][att_index])
    for i in range(len(data[0]) - 1):
        root.append("\n")
    build_tree(root, 0, "root")


if __name__ == "__main__":
    main()
