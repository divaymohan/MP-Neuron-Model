# -*- coding: utf-8 -*-
"""MP_Neuron.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cafVfBTq-19ycR3JHXsUQ6swCSWDxdt7

# Loading Data from Sklearn (Breast Cancer)
"""

import numpy as np
import sklearn.datasets
breast_cancer = sklearn.datasets.load_breast_cancer()
X = breast_cancer.data
Y = breast_cancer.target
print(X.shape,Y.shape)



import pandas as pd

data = pd.DataFrame(breast_cancer.data,columns = breast_cancer.feature_names)

data.head()

data['class'] = breast_cancer.target

data.head()

data.describe()

print(data['class'].value_counts())

print(breast_cancer.target_names)

data.groupby('class').mean()



"""# TestTrain Split

## Simple Split
"""

from sklearn.model_selection import train_test_split

X = data.drop('class',axis=1)
y = data['class']

type(X)

X_train,X_test,Y_train,Y_test = train_test_split(X,y,test_size=0.1);

print(X.shape,X_train.shape,X_test.shape)

print(y.mean(),Y_test.mean(),Y_train.mean())

"""## Data Ratio is different lets stratify data."""

X_train,X_test,Y_train,Y_test = train_test_split(X,y,test_size=0.1,stratify=y);

print(y.mean(),Y_test.mean(),Y_train.mean())

"""## Fixing the splits every time we run it"""

X_train,X_test,Y_train,Y_test = train_test_split(X,y,test_size=0.1,stratify=y,random_state=1)
print(y.mean(),Y_test.mean(),Y_train.mean())

"""# Binarisation of input"""

import matplotlib.pyplot as plt

plt.plot(X_train.T,'*')
plt.xticks(rotation='vertical')
plt.show()



import matplotlib.pyplot as plt
#binarize with mean
X_binarised_train = X_train.apply(pd.cut,bins=2,labels=[1,0])
X_binarised_test = X_test.apply(pd.cut,bins=2,labels=[1,0])
plt.plot(X_binarised_train.T,'*')
plt.xticks(rotation='vertical')
plt.show()

plt.plot(X_binarised_test.T,'*')
plt.xticks(rotation='vertical')
plt.show()

#converting them into numpy array
X_binarised_train = X_binarised_train.values
X_binarised_test = X_binarised_test.values

"""# MP Neuron Model"""

import numpy as np
for b in range(X_binarised_train.shape[1]+1):
  Y_pred_train = []
  accurate_rows = 0
  for x,y in zip(X_binarised_train,Y_train):
    y_pred = (np.sum(x)>=b)
    Y_pred_train.append(y_pred)
    accurate_rows += (y==y_pred)
  print(b,accurate_rows/X_binarised_train.shape[0])



from sklearn.metrics import accuracy_score
b = 28
y_pred_test = []
for x in X_binarised_test:
  y_pred = (np.sum(x)>=b)
  y_pred_test.append(y_pred)
print(b, accuracy_score(y_pred_test,Y_test))



"""# MP Neuron class"""

class MPNeuron:
 def __init__(self):
   self.b = None
 def model(self,x):
   return(sum(x)>=self.b)
 def predict(self,X):
   Y=[]
   for x in X:
     result = self.model(x)
     Y.append(result)
   return Y
 def fit(self,X,Y):
   accuracy = {}
   for b in range(X.shape[1]+1):
     self.b = b;
     y_pred = self.predict(X)
     accuracy[b]=accuracy_score(y_pred,Y)
   best_b = max(accuracy,key = accuracy.get)
   self.b = best_b

   print('Optimal value of b is', best_b)
   print('Highest Accuracy is',accuracy[best_b])

mp_neuron = MPNeuron()
mp_neuron.fit(X_binarised_train,Y_train)

y_test_pred = mp_neuron.predict(X_binarised_test)
accuracy_test = accuracy_score(y_test_pred,Y_test)
print(accuracy_test)

