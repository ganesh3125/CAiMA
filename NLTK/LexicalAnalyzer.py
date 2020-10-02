import nltk
from nltk.corpus import stopwords
import numpy as np

class LexicalAnalyzer:

    def __init__(self):
        self.stop_words = set(stopwords.words('english'))

    def analyze_and_search(self,text,keyword):
        keyword_appearance_list = list()
        wordsList = nltk.word_tokenize(text)
        wordslst = nltk.pos_tag(wordsList)
        only_word_list = []
        for x in wordslst:
            only_word_list.append(x[1])
        only_word_list = ' '.join(only_word_list)
        analyzed_text = np.asarray(nltk.pos_tag(wordsList))
        if len(analyzed_text)!=0:
            analyzed_text1 = list(analyzed_text[:, 0])
            keyword_appearance_list = [n for n, x in enumerate(analyzed_text1) if x == keyword]
        return analyzed_text, keyword_appearance_list, only_word_list
