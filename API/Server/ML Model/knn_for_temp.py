# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:24:57 2022

@author: TECHIE
"""

import sys
sys.path.append(r'C:\Users\User\Desktop\Final Year Project\API\Lib\site-packages')

import pandas as pd

#importing datasets  
data_set= pd.read_csv('cluster_obtained.csv')

x= data_set.iloc[:, [7,8]].values  
y= data_set.iloc[:, 14].values  

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test= train_test_split(x, y, test_size= 0.25, random_state=0)  
  
#feature Scaling  
from sklearn.preprocessing import StandardScaler
st_x= StandardScaler()    
x_train= st_x.fit_transform(x_train)    
x_test= st_x.transform(x_test)  

from sklearn.neighbors import KNeighborsClassifier  
classifier= KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2 )  
classifier.fit(x_train, y_train)

#Predicting the test set result  
y_pred= classifier.predict(x_test)

'''#Creating the Confusion matrix  
from sklearn.metrics import confusion_matrix  
cm= confusion_matrix(y_test, y_pred)  

from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score

print(classification_report(y_test, y_pred, digits=4))
accuracy_score(y_test, y_pred,)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average='micro')

from sklearn.metrics import cohen_kappa_score
cohen_kappa_score(y_test, y_pred)

'''


# Dump the model on pkl file
# Also dump the feature scale for fitting transforming the input latitude and longitude and predict
  
import joblib
joblib.dump(classifier, 'knn_model.pkl')
joblib.dump(st_x, 'fitted_Standard_Scaler.pkl')
