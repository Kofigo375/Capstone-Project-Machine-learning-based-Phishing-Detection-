import numpy as np
import pandas as pd
from xgboost import XGBClassifier
import feature_extraction 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE




def predict_xgb(test_url_array):
   
    ## importing dataset
    df = pd.read_csv('uci-ml-phishing-dataset.csv')
    print("shape of dataframe", df.shape)

    ## dropping web_traffic column
    df.drop(['id','web_traffic', 'Page_Rank'], axis=1, inplace=True)  # noqa: E501
    print("shape of dataframe after dropping 'web_traffic' ",df.shape)
    X = df.drop('Result', axis=1)
    print("shape of X ", X.shape)
    print("columns in X ", X.columns)
    y = df['Result']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=df['Result'])  # noqa: E501


    # Create SMOTE object
    smote = SMOTE(random_state=42)

    # Apply SMOTE to generate synthetic samples
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print('shape of X_train_resampled', X_train_resampled.shape)
    print("shape of 'y_train_resampled'", y_train_resampled.shape)

 
    y_train_xgb = np.where(y_train_resampled == -1, 0, y_train_resampled) ## converting -1 class to zero since xgboostclassifier expects o or 1
    xgb = XGBClassifier(n_estimators=100)
    xgb.fit(X_train_resampled, y_train_xgb)       ## come back and correct this
   

    return xgb.predict(test_url_array)



def predict_rf(test_url_array):
    df = pd.read_csv('uci-ml-phishing-dataset.csv')

    df.drop(['id','web_traffic','Page_Rank'], axis=1, inplace=True)  # noqa: E501
    X = df.drop('Result', axis=1)
    y = df['Result']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, stratify=df['Result'])  # noqa: E501

    # Create SMOTE object
    smote = SMOTE(random_state=42)

    # Apply SMOTE to generate synthetic samples
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train, y_train)
    print('X_train_resampled', X_train_resampled.shape)
    print('y_train', y_train_resampled.shape)

    
 
    rf = RandomForestClassifier(n_estimators=100)
    rf.fit(X_train_resampled, y_train_resampled)       ## come back and correct this
    ## how can we use part of the data to predict
   

    return rf.predict(test_url_array)














