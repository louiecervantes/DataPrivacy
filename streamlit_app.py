#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from scipy.stats import chi2_contingency
import scipy.stats as stats

#This function is used to encode the labels into numeric data
def encode_label(input_label, test_label):
  label_encoder.append(LabelEncoder())
  label_encoder[-1].fit(input_label)
  return label_encoder[-1].transform(test_label)

# Define the Streamlit app
def app():
    st.header("Welcome to Data Privacy Awareness Study")
    st.subheader("Louie F. Cervantes M.Eng. \n(c) 2023 WVSU College of ICT")
    
    st.title("Awareness and Utilization of Data Privacy in Social Media")
    st.write("Sequential explanatory mixed method research design was used in this study. It started with collecting and analyzing quantitative data using a validated and reliability-tested two sets of researcher-made instrument that was used to determine the school personnel’s level of awareness on data privacy and their degree of personal information shared on social media.")

    st.subheader("The Dataset")
    df = pd.read_csv('data_privacy.csv', dtype='str', header=0, 
        sep = ",", encoding='latin')
    st.dataframe(df, width=800, height=400)
    st.write("Properties of the dataset")
    desc = df.describe().T
    st.write(desc)
    df1 = df.loc[:, ['Age', 'Position']]
    if st.button('Begin'):
        st.write("We select the relevant attributes for describing our samples. The first 10 rows are shown below.")
        st.write(df1.head(10))
        st.write("The unique records in the selected attributes")
        st.write(df1.nunique())
        
    if st.button('Visualize'):
        st.write("The samples as grouped by Age")
        fig = plt.figure(figsize=(5,2))
        p = sns.countplot(x="Age", data = df1, palette="bright")
        _ = plt.setp(p.get_xticklabels(), rotation=90) 
        st.pyplot(fig)
        st.write("The samples as grouped by Position")
        fig = plt.figure(figsize=(5,2))
        p = sns.countplot(x="Position", data = df1, palette="muted")
        _ = plt.setp(p.get_xticklabels(), rotation=90) 
        st.pyplot(fig)
    if st.button('Analyze'):
        socmedia = df.iloc[:,2:21].astype(int).mean(axis=1)
        df1['socmedia'] = socmedia
        st.write("The social media mean ratings")
        st.write(df1)
        dpa_awareness = df.iloc[:,22:41].astype(int).mean(axis=1)
        df1['dpa_awareness'] = dpa_awareness
        st.write("The Data Privacy Awareness mean ratings")
        st.write(df1)

        # Convert string data to numerical data
        X = np.array(df1)
        #initialize the variables
        label_encoder = []
        X_encoded = np.empty(X.shape)

        position_labels = ['Faculty', 'Unit/Subject Area Head', 'Non-teaching Staff', 'A-Team']

        X_encoded[:, 0] =  X[:, 0]
        X_encoded[:, 1] = encode_label(position_labels, X[:, 1])
        #these data already numeric so we just copy
        X_encoded[:, 2] =  X[:, 2]
        X_encoded[:, 3] =  X[:, 3]

        X = np.array(X_encoded)
        #print the data to verify encoding was successful
        st.write('Sample of the encoded data')
        st.write(X[0:5])
# Run the app
if __name__ == "__main__":
    app()
