#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import xml.etree.ElementTree as ET
import os, fnmatch


parser = argparse.ArgumentParser(description = 'Compute metrics')
parser.add_argument('d', type=str, help = 'input path for NN result')
parser.add_argument('g', type=str, help = 'input path for ground truth')
args = parser.parse_args()

def xmlparser(xml):
    file_box = []
    tree = ET.parse(xml)
    root = tree.getroot()
    for box in root.iter('bndbox'):
        file_box.append([int(item.text) for item in box])
    return file_box       
        
def dir_parser(path):
    os.chdir(path)
    tensor = []
    for file in os.listdir('.'):
        if fnmatch.fnmatch(file, '*.xml'):
            for filebox in xmlparser(file):
                tensor.append(filebox)
    return tensor

def Intersection_over_Union(grt, pr):
    IoU = []
    for a, b in zip(grt, pr):
        xmin = max(a[0], b[0])
        ymin = max(a[1], b[1])
        xmax = min(a[2], b[2])
        ymax = min(a[3], b[3])
        aArea = (a[2] - a[0]) * (a[3] - a[1])
        bArea = (b[2] - b[0]) * (b[3] - b[1])
        IntArea = max(0, ymax - ymin) * max(0, xmax - xmin)
        IoU.append(IntArea / (aArea + bArea - IntArea))
    return IoU
            
#path1 = "/home/ss/target"
#path2 = "/home/ss/out"

ground_truth = dir_parser(args.g)
predicted = dir_parser(args.d)
for i in range(25):
    print(ground_truth[i], '|', predicted[i])
print()

EvIoU = Intersection_over_Union(ground_truth, predicted)
threshold = 0.5
TP = 0
for i in EvIoU:
    if i > threshold: TP += 1
    
print('TP = ', TP)
print('FP = ', 25-TP)
print('FN = ', 0)
print('TN = ', 0)
print('Accuracy = ', TP / 25)
print('Precision (TPR) = ', TP / 25)
print('Recall (FPR) =', TP / TP)
