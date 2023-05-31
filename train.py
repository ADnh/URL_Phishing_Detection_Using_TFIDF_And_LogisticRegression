# EDA Packages
import pandas as pd
import numpy as np
import random
import pickle

# Machine Learning Packages
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import f1_score, recall_score, accuracy_score,confusion_matrix,classification_report

import imblearn
from imblearn.under_sampling import RandomUnderSampler

# Load Url Data 
urls_data = pd.read_csv("data/final_data_hack_2023.csv")

def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens

# Labels
y = urls_data["label"].astype(int)
# Features
url_list = urls_data["url"]

# Using Default Tokenizer
#vectorizer = TfidfVectorizer()
# Using Custom Tokenizer
vectorizer = TfidfVectorizer(tokenizer=makeTokens, token_pattern=None)

# Store vectors into X variable as Our XFeatures
X = vectorizer.fit_transform(url_list)

pickle.dump(vectorizer, open("models/tfidf.pkl", "wb"))

with open("models/tfidf.pkl",'rb') as f:
    tf = pickle.load(f)

kf = StratifiedKFold(n_splits=2,shuffle=True,random_state=3)
spl=RandomUnderSampler()
model = LogisticRegression(max_iter=7600)

# train model
model.fit(X,y)

# save model
model_file = 'models/final_model.pkl'
pickle.dump(model, open(model_file, "wb"))

# eval model
y_pred = model.predict(X)

acc_arr = accuracy_score(y, y_pred)
f1_arr= f1_score(y, y_pred)
print("%0.2f f1 score" %(f1_arr))
print("%0.2f accuracy" %(acc_arr))
print('----------------------')
