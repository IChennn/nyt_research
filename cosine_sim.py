import csv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import sys

file_past = sys.argv[1]
file_now = sys.argv[2]

#read in dataset
data_past = csv.reader(open(file_past))
data_past = list(data_past)

data_now = csv.reader(open(file_now))
data_now = list(data_now)

data_all = data_past+data_now

print("data read-in finished!")

#convert list to tuple
def convert_to_tuple(data_list):
    data_tuple = ()
    for article in data_list:
        data_tuple += (" ".join(article),)
    return data_tuple

data_past_tuple = convert_to_tuple(data_past)
data_now_tuple = convert_to_tuple(data_now)
data_all_tuple = convert_to_tuple(data_all)

print("convert to tuple finished!")

#transform by tf-idf
tfidf_vectorizer = TfidfVectorizer()

tfidf_matrix_past = tfidf_vectorizer.fit_transform(data_past_tuple)
tfidf_matrix_now = tfidf_vectorizer.fit_transform(data_now_tuple)
tfidf_matrix_all = tfidf_vectorizer.fit_transform(data_all_tuple)

print("transform to matrix by tf-idf finished!")

#create two layer's input by calculating cosine similarity
matrix_past = cosine_similarity(tfidf_matrix_past, tfidf_matrix_past)
matrix_now = cosine_similarity(tfidf_matrix_now, tfidf_matrix_now)
matrix_layer = cosine_similarity(tfidf_matrix_all, tfidf_matrix_all)

print("cosine similarity calculation finished!")

#handle the dissimilarity
def compute_dissimilarity(my_matrix):
	new_matrix = []
	for i in my_matrix:
	    new_matrix.append(np.array(1-i))
	return np.matrix(new_matrix)

dis_matrix_layer = compute_dissimilarity(matrix_layer[:len(data_past),len(data_past):])

print("dissimilarity calculation finished!")

#output result as .txt

file_name = ['out_past.txt', 'out_present.txt', 'out_layer.txt']


with open(file_name[0], "wb") as f:
    for line in matrix_past:
        np.savetxt(f, [line],  fmt='%.2f')
print("t-past file outputted!")

with open(file_name[1], "wb") as f:
    for line in matrix_now:
        np.savetxt(f, [line],  fmt='%.2f')
print("t-now file outputted!")

with open(file_name[2], "wb") as f:
    for line in dis_matrix_layer:
        np.savetxt(f,line,  fmt='%.2f')
print("between layer file outputted!")

