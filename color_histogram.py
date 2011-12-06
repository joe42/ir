'''
Created on 05.12.2011

@author: joe
'''
#!/usr/bin/python

from PIL import Image
from collections import defaultdict
import sys, math, pickle

#file1 = sys.argv[1]
def get_histogram(img_path):
    im1 = Image.open(img_path)
    RED = 0
    GREEN = 1
    BLUE = 2
    histogram = defaultdict(int)
    body = im1.getdata()
    for px in body:
        index = ""
        for color in [RED,GREEN]:
            if px[color] in range(0,86):
                index += "0"
            elif px[color] in range(86,171):
                index += "1"
            elif px[color] in range(171,256):
                index += "2"
        if px[BLUE] in range(0,64):
            index += "0"
        elif px[BLUE] in range(64,128):
            index += "1"
        elif px[BLUE] in range(128,192):
            index += "2"
        elif px[BLUE] in range(192,255):
            index += "3"
        histogram[index] += 1
    return histogram

def histogram_diff(histogram1, histogram2):
    """:returns: an positive number representing the difference between the two histograms"""
    ret = 0;
    for key in histogram1.keys():
        ret += abs(histogram1[key]-histogram2[key])**2
    return math.sqrt(ret)

def get_image_list1():
    img_list1 = []
    for i in range(1, 101):
        img_list1.append("../img1/%03d.JPG" % i)
    return img_list1

def get_image_list2():
    img_list1 = []
    for i in range(1, 95):
        img_list1.append("../img2/%02d.JPG" % i)
    return img_list1
        

grey=Image.open("../img2/01.JPG").convert('L')
body = grey.getdata()
print repr(body[0])

img_list1 = get_image_list1()
img_list2 = get_image_list2()
   #thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   #thread.start_new_thread( print_time, ("Thread-2", 4, ) ) Image.open('input.bmp').convert('L')

        
def get_histograms():
    with open('data.pkl', 'r+b') as data:
        try:
            return pickle.load(data)
        except(EOFError):
            pass
        histograms = {}
        for img in get_image_list1():
            histograms[img]= get_histogram(img)
        for img in get_image_list2():
            histograms[img]= get_histogram(img)
        pickle.dump(histograms, data, -1)
    return histograms
    
histograms = get_histograms()
hitlist = defaultdict(list)

img_list1_copy = img_list1
for img1 in img_list1:
    for img2 in img_list1_copy:
        diff = histogram_diff(histograms[img1], histograms[img2])
        hitlist[img1].append((img2, diff))
        hitlist[img2].append((img1, diff))
    img_list1_copy.pop(0)
def f(x,y):
    return cmp(x[1],y[1])
for key in hitlist.keys():
    hitlist[key].sort(lambda x,y: f(x,y))
    print key +": " + repr(hitlist[key])

