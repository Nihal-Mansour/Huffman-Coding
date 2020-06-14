import numpy as np
import heapq


class Node:
    def __init__(self, char, probability, left_child, right_child):
        self.char = char
        self.probability = probability
        self.left_child = left_child
        self.right_child = right_child

    def __lt__(self, other):
        return self.probability < other.probability


Codes = {}


# if a tree has one node it's code will be 0
def encode(root, binaryCode):
    if (root is None):
        return
    if (root.right_child is None and root.left_child is None):
        Codes[root.char] = binaryCode
        return
    if (root.right_child is not None):
        binaryCode += '0'
        encode(root.right_child, binaryCode)
        binaryCode = binaryCode[:-1]
    if (root.left_child is not None):
        binaryCode += '1'
        encode(root.left_child, binaryCode)
        binaryCode = binaryCode[:-1]


# gets a leaf at a time
a = 0


def decode(root, code):
    global a
    if (root.right_child is None and root.left_child is None):
        return root.char

    if (code[a] == '0'):
        a += 1
        return decode(root.right_child, code)

    if (code[a] == '1'):
        a += 1
        return decode(root.left_child, code)


prob = {}  # has each char and it's probabillity
freq = {}  # has each char and it's frequancy
size = 0  # the size of the frequancy array
Nodes = []  # the list of nodes
outputfile = ""  # has the encoded chars (binary chars)
decodedfile1 = ""  # the decoded string

# open the file and reads from it
f = open("inputfile.txt", "r")
file = f.read()
f.close()

# to erase the extra endline in the end of the file
file = file[:-1]

# get the freq of each char
for i in file:
    if (i in freq):
        freq[i] += 1
    else:
        freq[i] = 1

# count the size of the frequancy array
for i in freq:
    size += freq[i]

# calculates the probabillity of each char
for i in freq:
    x = freq.get(i)
    prob[i] = x / size

# creats a heap from the nodes
for l in prob:
    node1 = Node(l, prob[l], None, None)
    heapq.heappush(Nodes, node1)

# left child is the bigger it's code is 1
# right child the smaller it's code is 0
# constructing the tree
# the Nodes list will have one node in it wich is the root of the tree
while len(Nodes) != 1:
    node2 = heapq.heappop(Nodes)
    node3 = heapq.heappop(Nodes)
    node4 = Node(node2.char + node3.char, node2.probability + node3.probability, node3, node2)
    heapq.heappush(Nodes, node4)

# makes the code for each char
encode(Nodes[0], "")

# loops on the file (input chars) and replaces each char with it's code
for n in file:
    outputfile += Codes[n]

# open the file and outpust the encoded string
f = open("encoded_file.txt", "w")
f.write(outputfile)
f.close()

# open the file and read the encoded string to decode it
f = open("encoded_file.txt", "r")
binaryfile = f.read()

# calls the function that get the char of each code
# and loops till the file ends
while a != len(binaryfile):
    decodedfile1 += decode(Nodes[0], binaryfile)

# open the file and outpust the decoded string
f = open("decoded_file.txt", "w")
f.write(decodedfile1)
f.close()


