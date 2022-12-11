import os
import numpy
import glob
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from config import *

images = glob.glob(str(Q2_path / '*.bmp'))

# Gets the current directory listing
# Number of images
num = len(images)

line = Image.open(images[0]).size[1]  # Image height
lie = Image.open(images[0]).size[0]  # Image width
edgeInfo = numpy.zeros((line, 2 * num))  # The matrix is used to store edge information.

# Open the image to get the edge value.
for i in range(0, num):
    img = Image.open(images[i])
    edgeInfo[:, 2 * i + 1] = numpy.array(img)[:, 0]  # Left edge information, placed in odd series
    edgeInfo[:, 2 * i] = numpy.array(img)[:, lie - 1]  # Right edge information, placed in an even column

# The edge value is obtained
known = [[] for i in range(0, num)]  # Known stitching

impossible = [[] for i in range(0, num)]  # Negative stitching

i = 0;
m = 14  # m is the starting point
m1 = m
splicing_sequence = [m]  # Save the stitching sequence
temp = [k for k in range(0, num)]
temp.remove(m1)

for kn in known:
    for knn in kn:
        try:
            temp.remove(knn)  # Delete known cases
        except:
            pass

while i < num - 1:
    if len(known[m1]) != 0:
        m2 = 0
        for kn in known[m1]:
            splicing_sequence.append(kn)
            m2 = kn
            i = i + 1
        m1 = m2
    else:
        temp1 = temp[:]
        for imp in impossible[m1]:
            try:
                temp.remove(imp)
            except:
                pass
        compare_matrices = numpy.zeros(len(temp))  # Use to compare matrices
        for j in range(0, len(temp)):
            # Each right edge is compared to all left edges
            compare_matrices[j] = numpy.sum((edgeInfo[:, 2 * m1] - edgeInfo[:, 2 * temp[j] + 1]) ** 2)

            # The smallest difference means the highest degree of agreement
        m = numpy.argmin(compare_matrices)
        splicing_sequence.append(temp[m])
        i = i + 1
        m1 = temp[m]
        temp = temp1[:]
        temp.remove(m1)  # remove the ladder up behind you
print(splicing_sequence)  # The comparison is complete and the sequence is output

# Add a watermark
myfont = ImageFont.truetype("C:\Windows\Fonts\simsun.ttc", 40) # Watermark font and size

comb_img = Image.new("RGBA", (lie * num, line), (255, 0, 0))  # New image, used for compositing
j = 0
for i in splicing_sequence:
    img = Image.open(images[i])
    d = ImageDraw.Draw(img)  # Add watermark
    d.ink = 150  # Watermark color
    d.text((0, 0), str(i), font=myfont)  # Add a watermark
    region = img.crop((0, 0, lie, line))
    comb_img.paste(region, (lie * j, 0, lie * (j + 1), line))
    j = j + 1
comb_img.show()


# The code don't have to be redundant as long it solves the problem