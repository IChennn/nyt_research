import os
import sys
import codecs
import csv
import numpy as np

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
import string


#Preprocessing 

stop = set(stopwords.words('english'))
exclude = set(string.punctuation) 
lemma = WordNetLemmatizer()

# doc-based
# def clean(input_doc):
#     stop_free = ' '.join([i for i in input_doc.lower().split() if i not in stop])
#     punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
#     #normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
#     return punc_free

def clean(input_doc):
    
    sentence_wise = sent_tokenize(input_doc)
    
    punc_free = []
    for sen in sentence_wise:
        punc_free.append(''.join(ch for ch in sen.lower() if ch not in exclude))
    
    stop_free = []
    for sen in punc_free:
        stop_free.append(" ".join(i for i in sen.split() if i not in stop)) 
        
    nor = []
    for sen in stop_free:
        nor .append(" ".join(lemma.lemmatize(word) for word in sen.split()))
    
    
    return nor

def clean_for_showing(input_doc):

    sentence_wise = sent_tokenize(input_doc)
    
    return sentence_wise

#To walk through and read in the file

# usage: python recursive.py [directory to process] [outputfile name(not path)] [query]
# example:
# walk_dir = "/Users/Hung/Documents/研究/0122/01"
# output_file = "test_out.csv"
# query = "designs"

walk_dir = sys.argv[1]
output_file = sys.argv[2]
ori_file = sys.argv[3]
query = sys.argv[4]

print('walk_dir = ' + walk_dir)


exclude_file_list = ['.DS_Store'] 
exclude_content = "LEAD: *3*** COMPANY REPORTS "

result = []
result_origin = []

for root, subdirs, files in os.walk(walk_dir):

    #subdirs: directory under current dir
    #files: file under current dir (not in the subdir)
    
    print('--\nroot = ' + root)
    # list_file_path = os.path.join(root, 'my-directory-list.csv')
    list_file_path = os.path.join('/Users/Hung/Documents/研究/0122', output_file)
    ori_file_path = os.path.join('/Users/Hung/Documents/研究/0122', ori_file)
    #print('output_file_path = ' + list_file_path)

    with open(list_file_path, 'w') as list_file:
        

        for filename in files:
            file_path = os.path.join(root, filename)

            if filename not in exclude_file_list:

                with codecs.open(file_path, "r", encoding='utf-8', errors='ignore') as f: 
                    f_content = f.read()
                    if exclude_content not in f_content and query in f_content:
                        
                        tmp = clean(f_content)
                        tmp2 = clean_for_showing(f_content)
                        
                        for i in range(len(tmp)):  
                            if query in tmp[i] and len(tmp2[i].split())>=10:                         
                                result.append(tmp[i].split())
                                result_origin.append([filename.rstrip(".fulltext.txt")] + tmp2[i].split())
                                print('\t- file %s (full path: %s)' % (filename, file_path))
                            

        for item in result:
            wr = csv.writer(list_file, quoting=csv.QUOTE_ALL)
            wr.writerow(item)

    with open(ori_file_path, 'w') as original_file:

        for item2 in result_origin:
            wr = csv.writer(original_file, quoting=csv.QUOTE_ALL)
            wr.writerow(item2)