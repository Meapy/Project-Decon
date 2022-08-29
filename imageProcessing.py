from operator import index
from posixpath import split
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pytesseract
from pytesseract import Output
import csv
import random
from csv import writer
import os

class imageProcessing():
    

    def __init__(self, file, color, decontype, wordstoremove) -> None:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        self.file = file
        print("FILEFILE: ", file)
        self.color = color
        self.decontype = decontype
        self.wordstoremove = wordstoremove  
        pass
    
    def custom_csv(self, wordstoremove, decontype):
        if os.path.exists("data/custom-words.csv"):
            os.remove("data/custom-words.csv")
        sentencewords = 'ignorrr'
        if decontype == 'custom' and len(wordstoremove) > 0:
            wordstoremove = wordstoremove.replace('.', ',').replace('/r/', ',').replace(', ', ',')
            wordstoremove = wordstoremove.split(',')
            listwords = list(wordstoremove)
            sentencewords = []
            for i in listwords:
                if ' ' in i:
                    sentencewords.append(i.lower())

            with open('data/custom-words.csv', 'w+') as f_object:
                for word in listwords:
                    word = word.lower()
                    f_object.write(word + '\n')
                f_object.close()

        return sentencewords
    

    def setup_image(self, img):
        # convert the image to gray scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = gray
        # apply a thrshold to get image with only b&w (binarization)
        ret, img = cv2.threshold(
            img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # save the thresh holded image
        cv2.imwrite("data/output/temp.png", img)
        return img

    def getWords(self, img):
        # Pytesseract
        d = pytesseract.image_to_data(img, output_type=Output.DICT)
        text = pytesseract.image_to_string(img)
        f = open("data/output/text_output.txt", "w+")
        f.write(text)
        f.close()
        words = text.split()
        for i in range(len(words)):  # make all the words into lower case for matching
            words[i] = words[i].lower()
        return words, d

    def removeFiles(self):
        # Remove words-text.csv & words-boxs.csv
        if os.path.exists("data/words-text.csv"):
            os.remove('data/words-text.csv')
        if os.path.exists("data/words-boxs.csv"):
            os.remove('data/words-boxs.csv')

    def createCSV(self, words):
        # Creating words-text.csv ( Contains all words that are found )
        k = 0
        for j in words:
            tempList = list([words[k]])
            k = k + 1
            with open('data/words-text.csv', 'a', newline='') as f_object:
                writer_object = writer(f_object)
                writer_object.writerow(tempList)
                f_object.close()

    def boundBoxesCSV(self, d):
        # Creating words-boxs.csv ( Contains all bound boxes that are found )
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            if d['text'][i] != "":
                (x, y, w, h) = (d['left'][i], d['top']
                                [i], d['width'][i], d['height'][i])
                wList = list([x, y, w, h])
                with open('data/words-boxs.csv', 'a', newline='') as f_object:
                    writer_object = writer(f_object)
                    writer_object.writerow(wList)
                    f_object.close()
                del wList[:]

    def matchWords(self, words, temp, main, sentenceindex):
        # Match the words with the words in the csv file
        indexList = []
        with open('data/words-matched.csv', 'w') as outFile:
            for line in temp:
                if line in main:
                    outFile.write(line)
                    line = line.replace("\n", "")
                    index = words.index(line)
                    words[index] = words[index].replace(
                        line, line + ' ')  # needed for duplicates
                    indexList.append(index)
        indexList.extend(sentenceindex)
        print(indexList)
        list(set(indexList))
        return indexList

    def drawBoxes(self, img, indexList):
        with open('data/words-boxs.csv', 'r') as f:
            read = list(csv.reader(f))
            for i, value in enumerate(read):
                if i in indexList:
                    (x, y, w, h) = (int(value[0]), int(
                        value[1]), int(value[2]), int(value[3]))
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
        cv2.imwrite("static/images/output.png", img)
        return "output.png"

    def drawSentenceBoxes(self, sentencewords):
        with open('data/words-text.csv', 'r') as f:
            read = list(csv.reader(f))
            indexes = []
            for s in sentencewords:
                splitsentence = s.split(' ')

                for i, value in enumerate(read):
                    if value[0] == splitsentence[0]:
                        for k in range(len(splitsentence)):
                            if read[i+k][0] == splitsentence[k]:
                                indexes.append(str(i+k))

            indexes = [int(x) for x in indexes]
            sentenceindex = []
            for i in range(len(indexes)-1):
                if indexes[i]+1 == indexes[i+1]:
                    sentenceindex.append(indexes[i])
                    sentenceindex.append(indexes[i+1])
        
        return sentenceindex


    def run(self, img, wordstoremove, decontype):
        start = cv2.getTickCount()
        self.removeFiles()
        img = cv2.imread(img)
        sentencewords = self.custom_csv(wordstoremove, decontype)
        tempImg = self.setup_image(img)
        words, d = self.getWords(tempImg)
        self.createCSV(words)
        sentenceindex = []
        if sentencewords != 'ignorr':
            sentenceindex = self.drawSentenceBoxes(sentencewords)
        self.boundBoxesCSV(d) 
        if os.path.exists("data/custom-words.csv"):
            with open('data/custom-words.csv', 'r') as csv1, open('data/words-text.csv', 'r') as csv2:
                main = csv1.readlines()  # Custom Words Dataset
                temp = csv2.readlines()  # Dataset created from inputted image
        else:
            with open('data/bad.csv', 'r') as csv1, open('data/words-text.csv', 'r') as csv2:
                main = csv1.readlines()  # Bad Words Dataset
                temp = csv2.readlines()  # Dataset created from inputted image
        matchedWords = self.matchWords(words, temp, main, sentenceindex)
        image = self.drawBoxes(img, matchedWords)
        end = cv2.getTickCount()
        time = (end - start) / cv2.getTickFrequency()
        print("Time: " + str(time))

        return image


if __name__ == "__main__":
    img = "data/letter.png"
    color = "white"
    wordstoremove = "sexual harassment, we are"
    decontype = "custom"
    imageProc = imageProcessing(img, color, wordstoremove, decontype)
    imageProc.run(img, wordstoremove, decontype)
    pass
