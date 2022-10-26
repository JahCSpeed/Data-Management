import math
from collections import defaultdict
from collections import Counter
import csv
from os import remove
import re
import filecmp
FILE_PATH = "tfidf_docs.txt"
STOP_WORDS_PATH = "stopwords.txt"
OUTPUT_PATH = "preproc_"
def removeExtraWhite(text):
    split = text.split()
    return " ".join(split)
def removeLinks(text):
    start1 = text.find("http://")
    start2 = text.find("https://")
    while((start1 != -1) or (start2 != -1)):
        if(start1 != -1):
            targetString = text[start1:findEnd(text,start1)]
            text = text.replace(targetString," ")
        if(start2 != -1):
            targetString = text[start2:findEnd(text,start2)]
            text = text.replace(targetString," ")
        start1 = text.find("http://")
        start2 = text.find("https://")
    
    return text
def findEnd(text,start):
    space = text.find(" ",start)
    newLine = text.find("\n",start)
    return min(space,newLine)
def removeNonAlpha(text):
    split_text = str(text).split()
    new = []
    for words in split_text:
        new.append(re.sub(r'\W+', '', words))
    return " ".join(new)
def write_to_file(path,text):
    f = open(path, "w")
    f.write(text)
    f.close()   
    
def cleanText(filePath):
    with open(filePath, 'r') as f:
        text = f.read()
    text.strip()
    text = removeLinks(text)
    text = removeExtraWhite(text)
    text = text.lower()
    text = removeNonAlpha(text)
    return text

def removeStopWords(filePath,text):
    with open(filePath, 'r') as f:
        stop_text = f.read()
    split_stop = stop_text.split()
    split_text = str(text).split()
    new = []
    for words in split_text:
        if words in split_stop:
            continue
        new.append(words)
    return " ".join(new)
    
def get_root_words(text):
    contents = str(text).split()
    new = []
    for token in contents:
        if token.endswith("ly"):
            new.append(token[0:-2])
        elif token.endswith("ing"):
            new.append(token[0:-3])
        elif token.endswith("ment"):
            new.append(token[0:-4])
        else:
            new.append(token)
    return " ".join(new) 

def frequencyOfWords(text):
    split_text = str(text).split()
    frequencyDict = Counter(split_text).most_common()
    return(frequencyDict)

def term_freq(dict,text):
    freq = defaultdict(float)
    for entry in dict:
        freq[entry[0]] = float((float(entry[1]) / (len(str(text).split()))))
    print(freq)


def workingFiles():
    with open(FILE_PATH, 'r') as f:
        text = f.read()
    return text.split()
    
def main():
    for file in workingFiles():
        text = cleanText(file)
        text = removeStopWords(STOP_WORDS_PATH,text)
        text = get_root_words(text)
        write_to_file((OUTPUT_PATH + file),text)
        dict = frequencyOfWords(text)
        term_freq(dict,text)
    return
main()