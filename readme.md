# Extract and Rank Content in New York Times Corpus on Sentence Basis 



The code is part of my master research on how to find and recommend interesting content from document archives. (it is unfinished, codes here are just on the step of trying)



## Requirements

Python 3.5

Numpy

Scipy

nltk

codecs

sklearn



## Introduction

The basic idea here is that the content from past documents (e.g. 1900 or 1980 ) will be considered "interesting" if they are:

* relevant to the query 
* common in the past yet rare in present
* Other metrics

I just focus on the first two metrics for now.



## How it works

Firstly, collect data into two folders, which represent past data and present data. For example,  past data from 1987 - 1989 and present data from 2005 - 2007.

#### Extract the full text part only

Follow this: https://github.com/notnews/nytimes-corpus-extractor



#### Read your text file into one csv file filtering by query

Do it for both past data and present data.

```Shell
$ python recursive.py <data directory> <outputfile name> <original outputfile name> <the query>
```

The `outputfile` is for calculation, so it removed stop word. `original outputfile` keeps them for reading comprehensibility. 

For example,

```Shell
$ python recursive.py present/ q_present_afternoon.csv ori_present_afternoon.csv afternoon
```



#### Compute similarity between each sentence 

```Shell
$ python cosine_sim.py <past data> <present data> 
```

For example,

```Shell
$ python cosine_sim.py q_past_afternoon.csv q_present_afternoon.csv 
```

As the result, you will get three output files, which will be the input in next step.

#### Process by MRRW

Reference: https://github.com/yvchen/MRRW

Basically, this step is based on the method in the paper.

```shell
$ python random_walk.py out_past.txt out_present.txt out_layer.txt 
```

The output file is two text file with the score for each sentence we just processed.



#### Store them as readable output!

Now we will rank the results by scores and map them to the sentence they represent.

```Shell
$ python result.py Score_layer_1.txt <original outputfile name>
```

