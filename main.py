import os
import glob
import pandas as pd
from pathlib import Path
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import math

def pdToXml(name, coordinates, size, img_folder):
    xml = ['<annotation>']
    xml.append("    <folder>{}</folder>".format(img_folder))
    xml.append("    <filename>{}</filename>".format(name))
    xml.append("    <source>")
    xml.append("        <database>Unknown</database>")
    xml.append("    </source>")
    xml.append("    <size>")
    xml.append("        <width>{}</width>".format(size["width"]))
    xml.append("        <height>{}</height>".format(size["height"]))
    xml.append("        <depth>3</depth>".format())
    xml.append("    </size>")
    xml.append("    <segmented>0</segmented>")

    for field in coordinates:
        xmin, ymin = max(0,field[0]), max(0,field[1])
        xmax = min(size["width"], field[0]+field[2])
        ymax = min(size["height"], field[1]+field[3])

        xml.append("    <object>")
        xml.append("        <name>Face</name>")
        xml.append("        <pose>Unspecified</pose>")
        xml.append("        <truncated>0</truncated>")
        xml.append("        <difficult>0</difficult>")
        xml.append("        <bndbox>")
        xml.append("            <xmin>{}</xmin>".format(int(xmin)))
        xml.append("            <ymin>{}</ymin>".format(int(ymin)))
        xml.append("            <xmax>{}</xmax>".format(int(xmax)))
        xml.append("            <ymax>{}</ymax>".format(int(ymax)))
        xml.append("        </bndbox>")
        xml.append("    </object>")
    xml.append('</annotation>')
    return '\n'.join(xml)

def transformCoordinates(string):
    [Ma,ma,r,x,y,v] = (float(z) for z in string.split())
    xr = (np.sqrt(Ma**2*np.cos(r)**2+ma**2*np.sin(r)**2)).round()
    yu = (np.sqrt(Ma**2*np.sin(r)**2+ma**2*np.cos(r)**2)).round()
    w = xr*2
    h = yu*2
    xo = x - xr
    yo = y - yu

    return xo, yo, w, h, 2*Ma, 2*ma, r, x, y

def returnEllipseListFiles(path):
    return [str(f) for f in Path(path).glob("**/*-ellipseList.txt")]

def generateArray(file):
    with open(file, 'r') as f:
        arr = f.read().splitlines()
    arr_len = len(arr)
    i=0
    rg = re.compile('(\d)*_(\d)*_(\d)*_big')
    output = []
    num_matches = 0
    while i<arr_len:
        val = arr[i]
        mtch = rg.match(val)
        if mtch:
            num_matches += 1
            try:
                di = dict()
                val = '{}.jpg'.format(val)
                di['name'] = val
                # matplotlib
                img = mpimg.imread(os.path.join("dataset_clean", val))
                if len(img.shape) == 3:
                    (h, w, _) = img.shape
                elif len(img.shape) == 2:
                    (h, w) = img.shape
                """fig,ax = plt.subplots(1)
                ax.imshow(img)"""

                jumps = int(arr[i+1])
                temp = []
                for j in range(0,jumps):
                    coords = arr[i+j+2]
                    #transformCoordinates(string)
                    xf,yf,wf,hf,Ma,ma,r,x,y = transformCoordinates(coords)

                    if xf + wf > w :
                        wf = w - xf
                    elif xf < 0 :
                        xf = 0
                    if yf + hf > h :
                        hf = h - yf
                    elif yf < 0 :
                        yf = 0
                    temp.append([xf,yf,wf,hf])

                    """rect = patches.Rectangle((xf,yf-hf), wf, hf, linewidth=1, edgecolor='b', facecolor='none')
                    ellip = patches.Ellipse((x,y), ma, Ma, r, linewidth=1, edgecolor='r', facecolor='none')
                    ax.add_patch(rect)
                    ax.add_patch(ellip)
                plt.show()"""

                di['annotations'] = temp
                di['size'] = {'height': int(h), 'width': int(w)}
                output.append(di)
            except:
                print("{} not found...".format(val))
        i+=1
    print(num_matches)
    return output

folder = glob.glob('dataset_clean/*.jpg')
folder = pd.Series(folder)
files = returnEllipseListFiles("labels")
print(len(folder))

s = 0
data = []
while s < len(files):
    x = generateArray(files[s])
    if len(data) == 0:
        data = x
    else:
        data = np.hstack((data, x))
    s+=1

data = pd.DataFrame(list(data), columns=['name', 'annotations', 'size'])
#print(data)


"""file_names = data['name'].tolist()
print(file_names)

temp = []
for filename in os.listdir('dataset_clean/'):
    if filename not in file_names:
        os.remove('dataset_clean/' + filename)"""

for index, row in data.iterrows():
    file = 'dataset_clean/{}.xml'.format(row['name'][:-4])
    print(file)
    with open(file, 'w') as f:
        xml_file = pdToXml(row['name'], row['annotations'], row['size'], 'dataset/')
        f.write(xml_file)




    
