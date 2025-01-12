import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.cluster import KMeans

def preprocess_data(df):
    #pick 1000 training examples out of 15,000 and drop the timestamp column
    df = df.sample(n=1000, random_state=42).reset_index(drop=True)
    df = df.drop(columns=['Timestamp'])

    #hot encoding for age and gender columns
    label_encoders = {}
    for col in ['AGE', 'GENDER']:  
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        label_encoders[col] = encoder

    #scale all values between 0-1
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)

    #core features = core_circle, bmi, steps, sleep, wlb
    X = df_scaled.iloc[:,[3,8,11,13,22]].values
    return X

if __name__ == '__main__':
    df = pd.read_csv('Wellbeing_and_lifestyle_data_Kaggle.csv')
    X = preprocess_data(df)
    kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
    kmeans.fit(X)
    with open('kmeans_model.pkl', 'wb') as file:
        pickle.dump(kmeans, file)