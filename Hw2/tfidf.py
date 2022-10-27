import math
from collections import defaultdict
from collections import Counter
import csv
import re
FILE_PATH = "tfidf_docs.txt"
STOP_WORDS_PATH = "stopwords.txt"
OUTPUT_PATH = "preproc_"
TFIDF_OUTPUT_PATH = "tfidf_"
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
    return freq

def compute_IDF(file_count,term_count):
    return math.log(file_count / (term_count)) + 1
def get_word_count_dict(freq_dict):
    f_word_dict = defaultdict(float)
    for file in freq_dict:
        for entry in freq_dict[file]:
            if entry[0] in f_word_dict:
                f_word_dict[entry[0]] = f_word_dict[entry[0]]  + 1
            else:
                f_word_dict[entry[0]] = 1
    return f_word_dict

def idf_dict(dict,files):
    idf_dict = defaultdict(float)
    for entry in dict:
        idf_dict[entry] = compute_IDF(len(files),dict[entry])
    return idf_dict
def workingFiles():
    with open(FILE_PATH, 'r') as f:
        text = f.read()
    return text.split()

def calculate_TFIDF(idf_dict,tf_dict):
    final_dict = defaultdict()
    for file in tf_dict:
        inner_dict = defaultdict(float)
        for word in tf_dict[file]:
            inner_dict[word] = round(tf_dict[file][word] * idf_dict[word],2)
        final_dict[file] = inner_dict
    return final_dict

def get_important_words(tf_dict,tfidf_dict):
    tfidf_per_file = defaultdict()
    for file in tf_dict:
        temp_dict = []
        for word in tf_dict[file]:
            temp_dict.append((word,tfidf_dict[file][word]))
        temp_dict = sort_Tuple(temp_dict)
        tfidf_per_file[file] = temp_dict[0:5]
    return tfidf_per_file
def sort_Tuple(tup):
    lst = len(tup)
    for i in range(0, lst):      
        for j in range(0, lst-i-1):
            if (tup[j][1] < tup[j + 1][1]):
                temp = tup[j]
                tup[j]= tup[j + 1]
                tup[j + 1]= temp
            if (tup[j][1]  == tup[j + 1][1]):
                if (tup[j][0]  > tup[j + 1][0]):
                    temp = tup[j]
                    tup[j]= tup[j + 1]
                    tup[j + 1]= temp
    return tup
def main():
    tf_list = defaultdict()
    clean_text = defaultdict(str)
    freq_text = defaultdict()
    for file in workingFiles():
        text = cleanText(file)
        text = removeStopWords(STOP_WORDS_PATH,text)
        text = get_root_words(text)
        clean_text[file] = text
        write_to_file((OUTPUT_PATH + file),text)
        freq_text[file] = frequencyOfWords(text)
        tf_list[file] = term_freq(freq_text[file],text)
    idf = idf_dict(get_word_count_dict(freq_text),workingFiles())
    tfidf_dict = calculate_TFIDF(idf,tf_list)
    tmp = get_important_words(tf_list,tfidf_dict)
    for file in tmp:
        write_to_file((TFIDF_OUTPUT_PATH + file),str(tmp[file]))
    return
main()