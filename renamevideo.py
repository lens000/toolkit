#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 20:07
# @Author  : Lens
# @Version : 3.7
# @File    : renamevideo.py
# @Software: PyCharm


import os

path = "C:/Users/m1834/Desktop/数值分析"

fileNames = os.listdir(path)
fileNamesDict = {}
for file in fileNames:
    if ".flv" in file:
        ext_name = file.split(".")[0]
        fileNamesDict[int(ext_name)] = file

newFileName = []
file = open(os.path.join(path, "课程目录.txt"))
for line in file:
    line = line.strip()
    line += ".flv"
    newFileName.append(line)

for fileKey in sorted(fileNamesDict):
    oldName = os.path.join(path,fileNamesDict[fileKey])
    newName = os.path.join(path,newFileName[fileKey - 1])
    os.rename(oldName, newName)
