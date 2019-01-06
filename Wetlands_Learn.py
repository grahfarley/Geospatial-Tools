"""This file performs the machine learning for the wetlands"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as RF
from sklearn.linear_model import LogisticRegression as LR

os.chdir("C:\Users\graham.farley\Downloads\Data")
WetlandFILE  = "C:\Users\graham.farley\Downloads\Data\WetlandTraining.txt"
NonWetlandFILE = "C:\Users\graham.farley\Downloads\Data\NonwetlandTraining.txt"


data1 = pd.read_csv(WetlandFILE,header = 0)
data2 = pd.read_csv(NonWetlandFILE,header = 0)



A = data1.values    #Convert to numpy array
l = np.shape(A)
ones = np.ones((l[0],1)) 
A = np.hstack((A,ones)) #Add at "True" column

B = data2.values
l = np.shape(B)
z = np.zeros((l[0],1))
B = np.hstack((B,z))    #Add a "False" Column


C = np.vstack((A,B))
D = np.delete(C,1,1)
D[:,3] /= 100 #Convert curvature and TWI back to original values
D[:,4] /= 100

y = D[:,5] #Output
X = D[:,:5] #Variables






X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

RandomForest = RF(max_depth = 3)
logreg = LR()

logreg.fit(X_train[:,2:],y_train,sample_weight=X_train[:,1]) #Column 1 is the "count", or the number of raster cells that take that value. This is used as the sample weight. 
RandomForest.fit(X_train[:,2:],y_train, sample_weight=X_train[:,1])

logreg.predict(X_test[:,2:])
print(logreg.score(X_test[:,2:],y_test,sample_weight=X_test[:,1])) #Gives the results as a percentage of accuracy

ypred = RandomForest.predict(X_test[:,2:])
print(RandomForest.score(X_test[:,2:],y_test,sample_weight=X_test[:,1]))

RESULTS = np.hstack((X_test[:,1],ypred)) #Create an array with the results and the associated OID

numpy.savetxt("WetlandResults.csv", RESULTS, delimiter=",") #write RESULTS to csv to be joined to wetlands in ArcMap.








