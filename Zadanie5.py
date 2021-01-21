import numpy as np
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu, sobel
from skimage.morphology import dilation, closing
from skimage.measure import label, regionprops
from skimage.color import rgb2hsv

def define_shape(image):
    if np.min(image) > 0:
        return "Прямоугольник"
    return "Круг"

def define_colors(reg_array):
    colors = []
    for region in reg_array:
        bbox = region.bbox
        subimage = image[bbox[0]:bbox[2], bbox[1]:bbox[3]]
        colors.append(np.max(subimage))
       
    colors.sort()
    
    diff = np.diff(colors)
    limit = np.max(diff) / 2
    
    groups = []
    
    while len(colors) > 0:
        group = []
        group += [colors.pop()]
        for c in colors[:]:
            if abs(c-group[0]) < limit:
                group.append(c)
                colors.remove(c)
        groups.append(group)
        
    return {i:len(group) for i, group in enumerate(groups)}  
   

image = plt.imread("balls_and_rects.png")
image = rgb2hsv(image)[:,:,0]
b  = image.copy()
b[b>0] = 1
labeled = label(b)

shapes = {}
for region in regionprops(labeled):
    key = define_shape(region.image)
    if key in shapes.keys():
        shapes[key] += [region]
    else:
        shapes[key] = [region]
    
print(f"Суммарное количество фигур: {np.max(labeled)}")
for key, value in shapes.items():
    print(f'Количество фигур "{key}": {len(value)}')
    print(f'По цветам:')
    
    for key, value in define_colors(value).items():
        print(f"Цвет {key}: {value}")
    