import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.model_selection import learning_curve
from sklearn.datasets import load_digits
from sklearn.metrics import confusion_matrix, plot_confusion_matrix, classification_report
import openpyxl
import joblib
import os
import pickle
from openpyxl import Workbook
from pathlib import Path
##Loading the data from the excel dataset
xlsx_file = Path( 'text.xlsx')
wb_obj = openpyxl.load_workbook(xlsx_file)
# Read the active sheet:
sheet = wb_obj.active
df = pd.read_excel('text.xlsx')
#Mixing all the rows in the excel file
df = df.sample(frac=1)
X=df.iloc[:300000,0:2].values
y=df.iloc[:300000,-1].values
#Train test split done here
legit_train,legit_test,mal_train,mal_test= train_test_split(X,y,test_size=0.3, random_state=0)
#loading and initializing the models
reg_ada1 = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10))
reg_ada2 = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10))
reg_ada3 = AdaBoostClassifier(DecisionTreeClassifier(max_depth=10))
#training of the models
reg_ada1.fit(legit_train,mal_train)
reg_ada2.fit(legit_train,mal_train)
reg_ada3.fit(legit_train,mal_train)
#training and testing them using cross-validation
scores_ada3 = cross_val_score(reg_ada3, X, y, cv=15)
scores_ada1 = cross_val_score(reg_ada1, X, y, cv=5)
scores_ada2 = cross_val_score(reg_ada2, X, y, cv=10)

print(scores_ada3.mean())
print(scores_ada1.mean())
print(scores_ada2.mean())
avg=((scores_ada3.mean()+scores_ada1.mean()+scores_ada2.mean())/3)*100
print("accuracy: ",avg)


