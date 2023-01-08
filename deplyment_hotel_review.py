# -*- coding: utf-8 -*-
"""Untitled4.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1eCkYU1btuPqPqetfq6nGXMgj5OFKbyDF
"""

import pandas as pd
# import numpy as np
import re 
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words=stopwords.words('english')
from nltk.stem import WordNetLemmatizer
import nltk
from afinn import Afinn
import spacy
# from imblearn.over_sampling import SMOTE
# from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.decomposition import PCA
# from sklearn.svm import SVC
# from pickle import dump
# from pickle import load
# from sklearn.linear_model import LogisticRegression
import streamlit as st
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import coo_matrix
from spacy.lang.en import English




# Page Setup *************************************************************
st.set_page_config(layout="wide")
# front end elements of the web page
html_temp = """<div style ="background-color:yellow;padding:13px"> <h1 style ="color:black;text-align:center;">Sentiment Analysis for Hotel Review</h1> </div>"""

# display the front end aspect
st.markdown(html_temp, unsafe_allow_html=True)


# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://images8.alphacoders.com/107/1079397.png");
#              background-attachment: fixed;
# 	     background-position: 25% 75%;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# add_bg_from_url()

# col1, mid, col2 = st.columns([2,8,2])
# with col1:
#     st.image("data:image/jpeg;base64,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AI6EDwntEQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQEREBERAREQETU4dqTbTXaQF7ytLCBzA3KGxn75twEREBERAREQERMQMxEQERMQMxEQEREBERAREQETEzAREQEREBERAREQOfwD/dNP+gp/6azoTn8A/wB00/6Cn/prOhAREQEREBERA1tZv7tu7O1tp2EDdhscjtJGfhI1ZVrxutr7wO1aIQ4rO4hLvXPqjBDbOXIetzBktMCBFdUmrsZ3DaqsEMK1QVjCrYjDIKn1iu7HPnjBmxUNczkM7qptA5ImUqy/NWOQxKhM5HIk4x0kimBAjFg12Qwa4sqahR6tYV2IrasldvIDDgc+qjJIPPz1Sa2yu1GFpDVutGVry5y3O/AGD7OAuMg8+fSWTEDi2WanukBFquG/DmsIWx6/4sEFSNwXqM7SM85pluIFiAXUZcsdteFIFprWvlzU4ryTk8+o54k8QOXoRqdpWxvWFi4Z1X1q8IzDCYAPN1B8MDOfHT4tTabW7sXndUqthiEwroxVOeFYqLBnrkjn0kgEGBGKNK5sQNXqVALtuZmZe7LWBKMBuXJgST4BBzPs+X0HUK9bKti5ZbHVWLBCzgsmS2F2oAOQO7n55krEGBGNPoGsrCmu5N9oyLGbdRUFG719xy7bACQeRc46ZPyatSUbvFuJ7+i38HlSStmXTk/rVqir5BvEEk5lUQOLoKnGpd9liIykHeeRfeSCvrHIKnyG0AD4dufM+oCIiAiIgIiICIiB/9k=", width=100)
# with mid:
#     st.markdown("<h1 style='text-align: center; color: white;'>Sentiment Analysis on Review data</h1>", unsafe_allow_html=True)
# with col2:
#     st.image("https://pbs.twimg.com/profile_images/1439939214162882569/6OPFxXo3_400x400.jpg", width=80)

    
    
    
    
    
#Lemmatization
wordnet=WordNetLemmatizer()

#Stop word
stop_words=stopwords.words('english')

nlp=spacy.load("en_core_web_sm")

# Varibale created for words which are not included in the stopwords
not_stopwords = ("aren", "aren't", "couldn", "couldn't", "didn", "didn't",
                 "doesn", "doesn't", "don", "don't", "hadn", "hadn't", "hasn",
                 "hasn't", "haven", "haven't", "isn", "isn't", "mustn",
                 "mustn't", "no", "not", "only", "shouldn", "shouldn't",
                 "should've", "wasn", "wasn't", "weren", "weren't", "will",
                 "wouldn", "wouldn't", "won't", "very")
stop_words_ = [words for words in stop_words if words not in not_stopwords]

# Additional words added in the stop word list
stop_words_.append("I")
stop_words_.append("the")
stop_words_.append("s")

# Stop word for keyword extraction
stop_words_keywords = stopwords.words('english')

# special additioanl stop words added for keyword extraction
stop_words_keywords.extend([
    "will", "always", "go", "one", "very", "good", "only", "mr", "lot", "two",
    "th", "etc", "don", "due", "didn", "since", "nt", "ms", "ok", "almost",
    "put", "pm", "hyatt", "grand", "till", "add", "let", "hotel", "able",
    "per", "st", "couldn", "yet", "par", "hi", "well", "would", "I", "the",
    "s", "also", "great", "get", "like", "take", "thank"
])

#Pre-processing the new dataset
def processing(corpus):
    output=[]
    
    #convert to string
    review =str(corpus)
    
    #to handle punctuations
    review = re.sub('[^a-zA-Z0-9*]', ' ', review)
    
     # Converting Text to Lower case
    review = review.lower()

    # Spliting each words - eg ['I','was','happy']
    review = review.split()

    # Applying Lemmitization for the words eg: Argument -> Argue - Using Spacy Library
    review = nlp(' '.join(review))
    review = [token.lemma_ for token in review]

    # Removal of stop words
    review = [word for word in review if word not in stop_words_]

    # Joining the words in sentences
    review = ' '.join(review)
    output.append(review)
    
    return output

def keywords(corpus):
    output2=[]
    
    #convert to string
    review =str(corpus)
    
    #to handle punctuations
    review = re.sub('[^a-zA-Z0-9*]', ' ', review)
    
     # Converting Text to Lower case
    review = review.lower()

    # Spliting each words - eg ['I','was','happy']
    review = review.split()

    # Applying Lemmitization for the words eg: Argument -> Argue - Using Spacy Library
    review = nlp(' '.join(review))
    review = [token.lemma_ for token in review]

    # Removal of stop words
    review = [word for word in review if word not in stop_words_keywords]

    # Joining the words in sentences
    review = ' '.join(review)
    output2.append(review)
    
    tfidf2 = TfidfVectorizer(norm="l2",analyzer='word', stop_words=stop_words_keywords,ngram_range=(1,3))
    tfidf2_x = tfidf2.fit_transform(output2)
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(tfidf2_x)
    
    # get feature names
    feature_names = tfidf2.get_feature_names()
    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(tfidf2.transform(output2))
    
    def sort_coo(coo_matrix):
        tuples = zip(coo_matrix.col, coo_matrix.data)
        return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

    #sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    
    #extract only the top n, n here is 10
    def extract_topn_from_vector(feature_names, sorted_items, topn=10):
        """get the feature names and tf-idf score of top n items"""
        
        #use only topn items from vector
        sorted_items = sorted_items[:topn]
        
        score_vals = []
        feature_vals = []
        
        # word index and corresponding tf-idf score
        for idx, score in sorted_items:
            #keep track of feature name and its corresponding score
            score_vals.append(round(score, 3))
            feature_vals.append(feature_names[idx])
            
        #create a tuples of feature,score
        #results = zip(feature_vals,score_vals)
        results= feature_vals

        return pd.Series(results)
        
    attributes = extract_topn_from_vector(feature_names,sorted_items,10)
    
    return attributes



# ### Prediction
# following lines create boxes in which user can enter data required to make prediction
# Textbox for text user is entering
st.subheader("Enter the text you'd like to analyze.")
text = st.text_input('Enter text')  # text is stored in this variable

# when 'Button' is clicked, make the prediction and store it  
if st.button("Predict"):
    # predict = Prediction(text)
    cleaned = processing(text)
    afn = Afinn()
    score = [afn.score(item) for item in cleaned]
    Affin_sentiment = ['Positive' if score > 0 else 'Negative' for score in score]
    predict = Affin_sentiment[0]
    st.success('The Sentiment of the review is {}'.format(predict))
    
# if st.button("IMP Attributes"):
    st.subheader("Important Attributes in Reviews")
    imp_att=keywords(text)
    for i in imp_att:
        st.success(i)
