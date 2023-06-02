"""
This script computes the novelty of a text file (e.g., generation) 
with regard to another text file (e.g., train) based on jaccard similarity.

Both text files are in the same format: one instance per line.

Example usage:
python jaccard_similarity.py train.txt generation.txt

"""

from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.tokenize import sent_tokenize
import numpy as np
import sys, string

# lemmatizer = WordNetLemmatizer()

def normalization(text):
    a = text.split()
    new_list = []
    for e in a:
        e = lemmatizer.lemmatize(e)
        new_list.append(e)
    return new_list

def jaccard_similarity(text1, text2):
    a = text1.split() #normalization(text1)
    b = text2.split() #normalization(text2)

    intersection = len(list(set(a).intersection(set(b))))
    union = len(set(a).union(set(b)))    #(len(a) + len(b)) - intersection
    if union == 0:
        print(a, b)
    return float(intersection) / float(union)

def novelty(train, generation):
    novelty_score = []
    for t in generation:
        t_score = []
        for text in train:
            t_score.append(jaccard_similarity(text, t))
        s = 1 - max(t_score)
        novelty_score.append(s)
    return np.mean(np.array(novelty_score))

def read_txt(filename):
    sentences = []
    with open(filename) as f:
        for line in f:
            # s = sent_tokenize(line[:-1])
            # s = line[:-1]
            h = " ".join(line.lower().split())
            h = h.translate(str.maketrans('', '', string.punctuation))
            h = " ".join(h.lower().split())
            sentences.append(h)
    return sentences

def formalized_train(text):
    if "'" in text:
        a = text.replace("'", " ")
        return a
    else:
        return text

if __name__ == "__main__":

    train = read_txt(sys.argv[1])
    generation = read_txt(sys.argv[2])

    score = novelty(list(set(train)), generation)
    print("novelty for {} is {:.3f}.".format(sys.argv[2], score))

