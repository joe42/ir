'''
Created on 06.12.2011

@author: joe
'''
from PIL import Image
import shelve
from collections import defaultdict
import sys

recount = 0


class MyImage(object):
    def __init__(self, image_path, bucket_size, minimal_cluster_size):
        self.path = image_path
        self.bucket_size = bucket_size
        self.category_cnt = 0
        self.cluster_size_dict = defaultdict(int)
        self.minimal_cluster_size = minimal_cluster_size
        self.category_to_bucket_map = {}
        
    def get_ccv(self):
        db = shelve.open("ccv.shelves")
        if db.has_key(self.path+"%i %i"%(self.bucket_size, self.minimal_cluster_size)):
            ccv = db[self.path+"%i %i"%(self.bucket_size, self.minimal_cluster_size)]
        else: 
            self.grey_image = Image.open(self.path).convert('L')
            self.pixels = list(self.grey_image.getdata())
            self.width, self.height = self.grey_image.size
            
            self.__form_clusters()
            
            ccv = {}
            for bucket in set(self.category_to_bucket_map.values()):
                categories_in_bucket = self.__get_categories(bucket)
                sum_of_coherent_pixels_in_current_bucket = 0  
                nr_of_incoherent_pixels_in_current_bucket = 0  
                for category in categories_in_bucket:
                    if self.cluster_size_dict[category] >= self.minimal_cluster_size:
                        sum_of_coherent_pixels_in_current_bucket +=  self.cluster_size_dict[category]
                    else: 
                        nr_of_incoherent_pixels_in_current_bucket += self.cluster_size_dict[category] 
                ccv[bucket] = (sum_of_coherent_pixels_in_current_bucket, nr_of_incoherent_pixels_in_current_bucket)
                
            db[self.path+"%i %i"%(self.bucket_size, self.minimal_cluster_size)] = ccv
            db.close()
        return ccv
    
    def __get_categories(self, bucket):
        ret = []
        for category in self.category_to_bucket_map.keys():
            if self.category_to_bucket_map[category] == bucket:
                ret.append(category)
        return ret
    
    def __get_new_category(self):
        self.category_cnt += 1
        return self.category_cnt
    
    def __get_pixel(self, x, y):
        if x >= self.width or y >= self.height or x < 0 or y < 0:
            return None
        return self.pixels[x+y*self.width]
    
    def __set_pixel(self, x, y, value):
        self.pixels[x+y*self.width] = value
    
    def __get_not_categorized_pixels_coordinates_from_surroundings(self, x, y):
        ret = []
        surrounding_coordinates = [(x-1,y-1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y+1),(x-1,y)]
        for x,y in surrounding_coordinates:
            pixel = self.__get_pixel(x, y)
            if pixel != None:
                ret.append((x,y))
        return ret
    
    def __form_clusters(self):
        for x in range(self.width):
            for y in range(self.height):
                pixel = self.__get_pixel(x, y)
                if pixel == None: 
                    continue
                bucket = self.__get_pixel(x, y) / self.bucket_size
                category = self.__get_new_category()
                self.category_to_bucket_map[category] = bucket
                self.cluster_size_dict[category] += 1
                self.__form_cluster(x,y,category, bucket)
        
    
    def __form_cluster(self, x, y, category, bucket):
        surrounding_pixels = set(self.__get_not_categorized_pixels_coordinates_from_surroundings(x, y))
        while len(surrounding_pixels)>0:
            x,y = surrounding_pixels.pop()
            if bucket != self.__get_pixel(x, y) / self.bucket_size:
                continue # pixel belongs to an other bucket
            self.__set_pixel(x, y, None)
            self.cluster_size_dict[category] += 1
            surrounding_pixels |= set(self.__get_not_categorized_pixels_coordinates_from_surroundings(x, y))
                
    def compare_ccv(self, image_path):
        ccv1 = self.get_ccv()
        ccv2 = MyImage(image_path, self.bucket_size, self.minimal_cluster_size).get_ccv()
        res = 0
        for bucket in range(0,255,5):
            if bucket in ccv1 and bucket in ccv2:
                res += abs(ccv1[bucket][0]-ccv2[bucket][0]) + abs(ccv1[bucket][1]-ccv2[bucket][1])
            elif bucket in ccv1:
                res += ccv1[bucket][0] + ccv1[bucket][1]
            elif bucket in ccv2:
                res += ccv2[bucket][0] + ccv2[bucket][1]
        return res
        
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
        

def run(img_list):
    hitlist = defaultdict(list)
    img_list_copy = img_list[:]
    for img1 in img_list:
        img_list_copy.pop(0)
        for img2 in img_list_copy:
            diff =MyImage(img1, 10, 5).compare_ccv(img2)
            hitlist[img1].append((img2, diff))
            hitlist[img2].append((img1, diff))
    for key in hitlist.keys():
        hitlist[key].sort(lambda x,y: cmp(x[1],y[1]))
        print key +": " + repr(hitlist[key][0:10])


img_list1 = get_image_list1() 
img_list2 = get_image_list2() 
run(img_list1)
run(img_list2)



        