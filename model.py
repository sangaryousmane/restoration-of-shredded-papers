from config import *
import glob
import numpy as np
from PIL import Image
"""
PIL => The Python Imaging Library:
This package adds image processing capability to python
This library provides extensive file format support, 
an efficient internal representation, and fairly powerful image processing capabilities.
"""

class RestorationOfShreddedPappers:

    ABSOLUTE_IMAGE_PATH = str(Q1_path / '*.bmp')
    initialized_image = {}
    find_unique_path = set()

    def image_reading(self):
        """
        Read the shredded paper pictures in the specified directory
        and store them in the dictionary for easy use
        """
        img_name_list = glob.glob(self.ABSOLUTE_IMAGE_PATH)
        for img_name in img_name_list:
            # k = img_name.replace('.bmp','')[-3:]

            """
             Use the file path as the key of the dictionary to find out the correct order
             of the pictures and then stitch and restore the pictures
            """
            key = img_name
            self.initialized_image[key] = Image.open(img_name)

    def __init__(self):
        self.image_reading()

    def finding_match_in_papers(self, paper_img, direction):
        """
        Based on the similarity of the edges of the picture,
        find out the adjacent pieces of paper for a given shredded piece of paper
        """
        self_img_array = np.array(self.initialized_image[paper_img])
        sh, sw = self_img_array.shape
        if direction == "r":
            self_edge = self_img_array[0:sh, sw - 1:sw]
        elif direction == 'l':
            self_edge = self_img_array[0:sh, 0:1]
        min_var = -1
        for k, v in self.initialized_image.items():
            if k == paper_img:
                continue
            if k in self.find_unique_path:
                continue
            other_img_array = np.array(v)
            h, w = other_img_array.shape
            if direction == "r":
                other_edge = other_img_array[0:h, 0:1]
            elif direction == 'l':
                other_edge = other_img_array[0:h, w - 1:w]
            else:
                pass
            var = np.sum(abs(self_edge - other_edge))
            if min_var == -1:
                similar_img = k
                min_var = var
            if var < min_var:
                similar_img = k
                min_var = var
        self.find_unique_path.add(paper_img)
        return similar_img

    def edge_finding_in_papers(self):
        """
        function to find the leftmost and rightmost shredded paper images in the original image
        after observing the shredded paper picture, it can be seen that when cutting vertically
        On the leftmost and rightmost shredded pieces of complete paper, there is a certain amount of white space
        """

        def isAllWhite(edge_array):
            """
            Determine whether a column of pixel values is all 255, that is, all white
            """
            WHITE_RGB = 255
            for k in edge_array:
                if k != WHITE_RGB:
                    return False
            return True

        for k, v in self.initialized_image.items():
            img_array = np.array(v)
            h, w = img_array.shape
            right_edge = img_array[0:h, w - 1:w]
            left_edge = img_array[0:h, 0:1]
            if isAllWhite(right_edge):
                right_img_name = k
            elif isAllWhite(left_edge):
                left_img_name = k
        return (left_img_name, right_img_name)

    def find_in_perfect_order(self):
        correct_order = []
        left_side_img, right_side_img = self.edge_finding_in_papers()
        correct_order.append(left_side_img)
        paper_list = list(self.initialized_image.keys())
        paper_list.remove(left_side_img)
        paper_list.remove(right_side_img)
        while paper_list:
            now_paper = correct_order[len(correct_order) - 1]
            next_paper = self.finding_match_in_papers(now_paper, direction="r")
            paper_list.remove(next_paper)
            correct_order.append(next_paper)
        correct_order.append(right_side_img)
        return correct_order;

    def final_splicing(self, order):
        """
        Restore vertically cut shredded pieces of paper
        In the correct picture order (from left to right),
        the shredded pieces of paper are stitched together into complete pieces
        """
        UNIT_W, UNIT_H = self.initialized_image[order[0]].size
        TARGET_WIDTH = len(order) * UNIT_W
        target = Image.new('RGB', (TARGET_WIDTH, UNIT_H))
        x = 0
        for img_name in order:
            img = self.initialized_image[img_name]
            target.paste(img, (x, 0))
            x += UNIT_W
        return target


if __name__ == "__main__":
    rp = RestorationOfShreddedPappers()
    perfect_order = rp.find_in_perfect_order()
    final_result = rp.final_splicing(perfect_order)
    final_result.show('whole.bmp') # method which show an image to disk, and calls an external display utility.
    idx_list = []
    for order in perfect_order:
        idx = order[-7:-3]
        idx_list.append(idx)
    print(idx_list)
