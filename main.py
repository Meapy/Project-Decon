import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
import easygui
from pytesseract import Output
import csv
import random
from csv import writer
import os


f = easygui.fileopenbox(filetypes=["*.jpg","*.jpeg","*.png"])
print(f)
img = cv2.imread(f)

#if on windows, uncomment this line:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


# create a function to extract text from image using pytesseract and put it into a txt file
def setup_image(img):
    # convert the image to gray scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = gray
    # apply a thrshold to get image with only b&w (binarization)
    ret, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # save the thresh holded image
    cv2.imwrite("data/output/temp.png", img)
    return img


# Read in image
img1 = setup_image(img)

# Pytesseract
d = pytesseract.image_to_data(img1, output_type=Output.DICT)
text = pytesseract.image_to_string(img1)
f = open("data/output/text_output.txt", "w+")
f.write(text)
f.close()
words = text.split()
for i in range(len(words)):  # make all the words into lower case for matching
    words[i] = words[i].lower()

# Remove words-text.csv & words-boxs.csv
if os.path.exists("words-text.csv"):
    os.remove('words-text.csv')
if os.path.exists("words-boxs.csv"):
    os.remove('words-boxs.csv')

# Creating words-text.csv ( Contains all words that are found)
k = 0
for j in words:
    tempList = list([words[k]])
    temptList = tempList
    k = k + 1
    with open('words-text.csv', 'a', newline='') as f_object:
        # Pass File object to Writer object
        writer_object = writer(f_object)
        # Append the List to next csv row
        writer_object.writerow(tempList)
        # Close the csv
        f_object.close()
    del tempList[:]

# Creating words-boxs.csv file ( Contains all Bounding Boxes )
n_boxes = len(d['level'])
for i in range(n_boxes):
    if d['text'][i] != "":
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        wList = list([x, y, w, h])
        with open('words-boxs.csv', 'a', newline='') as f_object:
            # Pass File object to Writer object
            writer_object = writer(f_object)
            # Append the List to next csv row
            writer_object.writerow(wList)
            # Close the csv
            f_object.close()
        del wList[:]

# Compare words-text.csv with bad-words-removed-blanks.csv to see if any words match
with open('data/bad.csv', 'r') as csv1, open('words-text.csv', 'r') as csv2:
    # Main = Bad Words Dataset
    # Temp = Dataset created from inputted image
    main = csv1.readlines()
    temp = csv2.readlines()

indexList = []
print('The matching words are:')
# Open the words-matched.csv File and write in any matched words
with open('words-matched.csv', 'w') as outFile:
    for line in temp:
        if line in main:
            outFile.write(line)
            print(''.join(line))
            line = line.replace("\n", "")
            index = words.index(line)
            words[index] = words[index].replace(line, line + ' ')  # needed for duplicates
            print(index)
            indexList.append(index)
print(indexList)

# Draw Rectangle on the bad words
with open('words-boxs.csv', 'r') as f:
    read = list(csv.reader(f))
    for i, value in enumerate(read):
        if i in indexList:
            (x, y, w, h) = (int(value[0]), int(value[1]), int(value[2]), int(value[3]))
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
            print(i, value)

cv2.imwrite("data/output/output.png", img)
img = cv2.resize(img, (0,0), fx=0.75, fy=0.75)
cv2.imshow('censored.png', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
