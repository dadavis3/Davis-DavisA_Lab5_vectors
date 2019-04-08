# DAVIS, DAVID A  80610756

# In this lab assignment we were asked to read 2 files, one that had vectors
# for some words and other with pairs of words in which we will compare 
# and provide the amgnitud of the words. We had to use 2 ways, one with hash
# tables and other with binary searc trees. The main goal for this lab 
# assignment is to learn and practice how to solve problems with hash tables
# and binary search trees.

import numpy as np
import time
import math

#-------------------------     PRE-METHODS     -----------------

# **** BST:
class BST(object):
    # Constructor
    def __init__(self, item=[], left=None, right=None):
        self.item = item
        self.left = left
        self.right = right
        
def Insert(T,newItem):
    if T == None:
        T =  BST(newItem)
    elif T.item > newItem:
        T.left = Insert(T.left,newItem)
    else:
        T.right = Insert(T.right,newItem)
    return T        
        
# BST: find the height of a tree
def FindHeight(T):
    if T is not None:  # base case
        return (1 + max([(FindHeight(T.left)), FindHeight(T.right)]))  # 1 + (the higher number)
    else:
        return -1
    
# BST: count the number of nodes in T
def count_nodes(T):
    if T is not None:
        return 1 + count_nodes(T.left) + count_nodes(T.right)
    return 0

# BST: search a string in the tree T, return node with the same number if it was found, None if not found
def search_word(T, k):
    temp = T  # temporary variable for T
    while temp is not None:  # iterate through necessary nodes
        if temp.item[0] == k:  # found
            temp.item[1]
            return temp.item[1]
        elif temp.item[0] > k:  # smaller
            temp = temp.left
        else:  # larger
            temp = temp.right
    return None  # not found

# *** HASHTABLE:        
        
class HashTableC(object):
    # Builds a hash table of size 'size'
    # Item is a list of (initially empty) lists
    # Constructor
    def __init__(self, size):
        self.item = []
        self.num_items = 0
        for i in range(size):
            self.item.append([])
    
        
def InsertC(H, k):
    # Inserts k in appropriate bucket (list)
    # Does nothing if k is already in the table
    if H.num_items // len(H.item) == 1:  # recize table
        H = doubleSize(H)
    b = h(k[0], len(H.item))  # get the right index
    H.item[b].append([k[0], np.array(k[1:]).astype(np.float)])
    H.num_items += 1  # keep up with elements
    return H

# HT: find k and return array if found
def FindC(H, k):
    # Returns bucket (b) and index (i)
    # If k is not in table, i == -1
    b = h(k, len(H.item))  # get index
    for i in range(len(H.item[b])):  # traverse the node
        if H.item[b][i][0] == k:  # found
            return H.item[b][i][1]  # return array
    return -1

# Returns # of empty list and standard deviation of lengths of lists
def h(s, n):
    r = 0
    for c in s:
        r = (r * n + ord(c)) % n
    return r

# This method returns # of empty list and standard deviation of lengths of lists
def infolist(H):
    c = 0
    m = H.num_items / len(H.item)
    k = 0
    for a in H.item:
        k += len(a) - m
        if a == []:
            c += 1
    return c, (1 / len(H.item)) * k

#  Doubles the size of hashtable
def doubleSize(H):
    H2 = HashTableC(2 * len(H.item) + 1)  # To double the size
    for a in H.item:  
        if a != []:  # if the table is not empty traverses it cince it's chaining
            for i in a:
                H2.item[h(i[0], len(H2.item))].append([i[0], i[1]])
                H2.num_items += 1
    return H2

#------------------------   METHODS FOR LAB     ---------------

# Builds the BST
def BSTree(f, f2):
    print("\nBuilding binary search tree.\n")
    T = None
    start1 = time.time()  # starting time
    
    for line in f:  # reads line by line 
        data = line.split(' ')  # array separated by ' '
        T = Insert(T, [data[0], np.array(data[1:]).astype(np.float)])  # insert word+embeddings
    
    print("Binary Search Tree stats:")
    print("Number of nodes: ", count_nodes(T))  # num of nodes
    print("Height: ", FindHeight(T))  # num of height
    print("Running time for binary search tree construction:", (time.time() - start1))
    print("\nReading word file to determine similarities.\n")
    start2 = time.time()  # starting time
    for line2 in f2:  # reads line by line the txt file with the pairs
        
        data2 = line2.split(',')  # words pair separated by ','
        e0 = search_word(T, data2[0])  # search the 1st word and returns array
        e1 = search_word(T, data2[1])  # search the 2nd word and returns array
        print("Similarity", data2[0:2], " = ",round(np.sum(e0 * e1) / (math.sqrt(np.sum(e0 * e0)) * math.sqrt(np.sum(e1 * e1))),4))  # compute the similarity
    print("\nRunning time for binary search tree query processing: ", (time.time() - start2))

# Builds the HashTable
def HashTable(f,f2):
    print("\nBuilding hash table.\n")
    print("Hash Table stats:")
    H = HashTableC(29)  
    print("Initial table size", len(H.item))
    start1 = time.time()  # starts the time 
    for line in f:  # read line by line the glove.txt
        
        data = line.split(' ')
        H = InsertC(H, data)  # inserts al the data into the hash table
     
    print("Total elements: ", H.num_items)
    print("Final table size: ", len(H.item))
    print("Load factor: ", H.num_items / len(H.item))
    c, d = infolist(H)
    print("Percentage of empty lists:", c / len(H.item) * 100)
    print("Standard deviation of the lengths of the lists:", d)
    print("Running time for Hash Table construction:", (time.time() - start1))
    print("\nReading word file to determine similarities.\n")
    start2 = int(time.time())
    for line2 in f2:  # reads line by line the txt file where the words are
        data2 = line2.split(',')
        e0 = FindC(H, data2[0])  # return array if string found
        e1 = FindC(H, data2[1])  
        print("Similarity", data2[0:2], " = ",
              round(np.sum(e0 * e1) / (math.sqrt(np.sum(e0 * e0)) * math.sqrt(np.sum(e1 * e1))),
                    4))  # compute similarity
    print("\nRunning time for hash table query processing: ", (time.time() - start2))

# main method
answer = '1'
answer = input("Type 1 for binary search tree or 2 for hash table with chaining\nChoice: ")
f = open('glove.6B.50d.txt', encoding='utf-8')  # file with vectors
f2 = open('WordList.txt', encoding='utf-8')  # file with pairs

if answer == '1':   # if 1 then BST, if 2 then HashTable
    BSTree(f,f2)
elif answer == '2':  
    HashTable(f, f2)

f.close()
f2.close()
