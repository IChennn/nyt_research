import os
import sys
import numpy as np
import csv


score_file = sys.argv[1]
data_file = sys.argv[2]

#read in data

score_past = np.loadtxt(score_file)
data_past = csv.reader(open(data_file))
data_past = list(data_past)

print("read in data completed!")

#ranking

def get_ranking(scores, articles):  
    tmp = []
    for i, score in enumerate(scores):
        tmp.append([i, score, articles[i][0], " ".join(articles[i][1:])])
    ranking = sorted(tmp, key=lambda x:x[1], reverse=True)
     
    return ranking

ranked_result = get_ranking(score_past, data_past)

print("ranking completed!")

#save as file
with open("extracted_news.csv", 'w') as f:	
	for news in ranked_result:
	    wr = csv.writer(f, quoting=csv.QUOTE_ALL)
	    wr.writerow(news)

print("extracted news txt saved!")
