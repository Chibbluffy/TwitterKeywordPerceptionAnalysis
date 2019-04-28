from time import time
from utils import txt2words, w2v_load_model
import numpy as np
import gensim
import json
import sys

class DeepTextAnalyzer(object):
    def __init__(self, word2vec_model):
        """
        Construct a DeepTextAnalyzer using the input Word2Vec model
        :param word2vec_model: a trained Word2Vec model
        """
        self._model = word2vec_model

    def txt2vectors(self,txt):
        """
        Convert input text into an iterator that returns the corresponding vector representation of each
        word in the text, if it exists in the Word2Vec model
        :param txt: input text
        :param is_html: if True, then extract the text from the input HTML
        :return: iterator of vectors created from the words in the text using the Word2Vec model.
        """
        words = txt2words(txt)
        words = [w for w in words if w in self._model]
        if len(words) != 0:
            for w in words:
                yield self._model[w]


    def txt2avg_vector(self, txt):
        """
        Calculate the average vector representation of the input text
        :param txt: input text
        :param is_html: is the text is a HTML
        :return the average vector of the vector representations of the words in the text  
        """
        vectors = self.txt2vectors(txt)
        vectors_sum = next(vectors, None)
        if vectors_sum is None:
            return None
        count =1.0
        for v in vectors:
            count += 1
            vectors_sum = np.add(vectors_sum,v)
        
        #calculate the average vector and replace +infy and -inf with numeric values 
        avg_vector = np.nan_to_num(vectors_sum/count)
        return avg_vector

def load_tweets(f):
    tweets = []
    loaded = json.loads(f)
    for x in loaded:
        #id_str = x["id_str"]
        label = x["label"]
        text = x["text"]
        tweets.append([label, text])
    return tweets

def generate_arff_header(f, size):
    f.write('@relation Word2VecRelation\n\n')
    for i in range(size):
        f.write('@attribute feature%s numeric\n' % i)
    f.write('@attribute class { relevant, irrelevant, unknown }\n')
    f.write('\n')

def generate_arff_data(f, tweets):
    t0 = time()
    model = w2v_load_model('../GoogleNews-vectors-negative300.bin')
    print 'loading model: %s' % (time() - t0)

    dta = DeepTextAnalyzer(model)

    f.write('@data\n');
    #for _, label, text in tweets:
    for label, text in tweets:
        vector = w2v_vector(dta, text, label)
        if vector is not None:
            f.write('%s,%s\n' % (','.join(vector), label))

def w2v_vector(dta, text, label):
    """
    Given a text, generate Word2Vec vector and return it
    :param dta: DeepTextAnalyzer object
    :param text: input text
    :param label: input label
    """
    vector = dta.txt2avg_vector(text)
    if vector is None:
        print 'Could not generate Word2Vec vector for %s' % text
        return
    return [0.0 if v==None else str(v) for v in vector]

if __name__ == '__main__':
    # 1. load tweets
    tweets = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            loaded = json.loads(line)
            label = loaded["label"]
            text = loaded["text"]
            tweets.append([label, text])

    # 2. generate ARFF file
    with open(sys.argv[1][:-4]+'.arff', 'w') as f:
        # generate the header
        generate_arff_header(f, len(tweets))

        # generate the data part
        generate_arff_data(f, tweets)

