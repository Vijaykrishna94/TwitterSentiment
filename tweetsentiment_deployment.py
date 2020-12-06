# -*- coding: utf-8 -*-
"""TweetSentiment_deployment.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UrmP0qwD4h0AqpP2mTZPTKM--ROdUQv3
"""

'''from google.colab import drive
drive.mount('/content/drive')
import subprocess'''

def install(name):
    subprocess.call(['pip', 'install', name])

'''install('flask-ngrok')'''
install('streamlit')

import nltk
nltk.download('punkt')
nltk.download('wordnet')


import pickle
import os
os.environ['PYTHONHASHSEED'] = '0'
import random as rn
rn.seed(0)
import pandas as pd
import numpy as np
np.random.seed(0)
import tensorflow as tf
tf.random.set_seed(0)
import streamlit as st
import nltk 
import re 
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer() 
from sklearn.model_selection import train_test_split
#from tensorflow.keras.preprocessing.text import one_hot
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras import layers
from tensorflow.keras.layers import Dropout
from tensorflow import keras
from  tensorflow.keras.models import load_model

import  numpy as np
from PIL import Image
import requests
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS 

with open("encoder_3 (1)", "rb") as f:
    encoder = pickle.load(f)


with open("/content/drive/MyDrive/ML/tweet_nouns", "rb") as f:
    tweets = pickle.load(f)


get_sentiment = load_model('Tweet_Sentiment_3 (1).h5')


def remove_columns(df,l):
      return df.drop(l,axis=1)

def convert_str(df,text):
      return  df.text.apply(lambda x: str(x))

def convert_lower(s):
      return s.apply(lambda x: x.lower())

def remove_special(u):
      return u.apply(lambda x: re.sub(r"[^a-zA-Z0-9]+",' ',x))

def lemmet(l):
       return l.apply(lambda x: " ".join([lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(x)]))
       



def preprocess(df,text,remove,l):
  if remove==True:
    df_p = remove_columns(df,l)
    df_p.text = lemmet(remove_special(convert_str(df_p,text)))
    
  else : 
    df_p.text = lemmet(remove_special(convert_str(df_p,text)))
  
  return df_p

  
def Hash(X_train):
  global vocab_size 
  vocab_size = 10000
  return [encoder(word,vocab_size,hash_function='md5') for word in X_train]

  


def padd(Train_encoded):
  global max_length
  max_length = 50
  return pad_sequences(Train_encoded,maxlen=max_length,padding='pre' )


def Model_data(df_p,text):
  return np.array(padd(Hash(df_p[text])))




def prepare_data(df_test,text,remove,l):
  X_test = Model_data(preprocess(df_test,text,remove,l),text)
  return X_test



def predict(X_test_1):
  y_pred_1 = get_sentiment.predict_classes(X_test_1)
  y_pred_1 = y_pred_1.reshape(-1)
  return pd.Series(y_pred_1).map({0:'General',1:'Disaster'})

def execute(df_test,text = 'text',remove=True,l=['keyword','id','location']):
  return pd.concat([preprocess(df_test,'text',remove=True,l=['keyword','id','location']),predict(prepare_data(df_test,'text',remove=True,l=['keyword','id','location']))],axis=1)



def welcome():

  return "Hi wana Classify"

#_____________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________


def text_str(text):
      return  str(text)

def lower_text(s):
      return s.lower()

def text_special(u):
      return re.sub(r"[^a-zA-Z0-9]+",' ',u)

def lemmet_text(l):
       return " ".join([lemmatizer.lemmatize(word.lower()) for word in nltk.word_tokenize(l)])

def preprocess_text(text):

  return lemmet_text(text_special(lower_text(text_str(text))))



def Hash_text(text):
  global vocab_size 
  vocab_size = 10000
  return [encoder(text,vocab_size,hash_function='md5')]





def padd_text(text_encoded):
  global max_length
  max_length = 50
  return pad_sequences(text_encoded,maxlen=max_length,padding='pre' )


def Model_text(text):
  return np.array(padd_text(Hash_text(text)))


def prepare_text(text):
  text_test = Model_text(preprocess_text(text))
  return text_test


def predict_text(text_test):
  y_pred_text = get_sentiment.predict_classes(text_test)
  y_pred_text = y_pred_text.reshape(-1)
  if y_pred_text[0] == 0 :
    k='General'
  else:
    k='Disaster'

  return k

def execute_text(text):
  return predict_text(prepare_text(text))






def get_wordcloud(tweets):
  pic = np.array(Image.open('/content/drive/MyDrive/PngItem_300707.png'))

  wordcloud = WordCloud(width = 800, height = 800, 
                  background_color ='white', 
                  stopwords = STOPWORDS, mask = pic, 
                  min_font_size = 5).generate(tweets)

  plt.figure(figsize = (10, 10), facecolor = 'white', edgecolor='blue') 
  plt.imshow(wordcloud) 
  plt.axis("off") 
  plt.tight_layout(pad = 0) 
    
  plt.show()












#_____________________________________________________________________________________________________________________
#_____________________________________________________________________________________________________________________




def main():
  st.title('Tweet Sentiment-Kaggle Dataset')
  
  html_temp= """ 
  <div style="background-color:tomato;padding:10px">
  <h2 style="color:white;text-align:centre;">Identifying Disaster Tweets</h2>
  </div>
  <address style="color:black;text-align:left">by VijayKrishna Burra</address>
  """
     
  
  st.markdown(html_temp,unsafe_allow_html=True)

  
  text = st.text_input('Enter text here')
  if text:
    st.success("The tweet is : {0} ".format(execute_text(text)))

  










  
  test = st.file_uploader("Choose a CSV file", accept_multiple_files=True)
  if test:
  # To read file as bytes:
    df_test = pd.read_csv(test[0])
    
    if st.button("Check"):
      st.write(df_test)
    if st.button("Predict"):
      st.write(execute(df_test,text = 'text',remove=True,l=['keyword','id','location']))

  if st.button("WordCloud"):
    st.image('/content/drive/MyDrive/ML/tweet_wordcloud.png')

  if st.button("About"):
    st.text("Built Using StreamLit-by VijayKrishna")



if __name__== '__main__':
  main()

