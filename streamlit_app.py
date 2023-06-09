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
label_encoder = []
def encode_label(input_label, test_label):
  label_encoder.append(LabelEncoder())
  label_encoder[-1].fit(input_label)
  return label_encoder[-1].transform(test_label)

def GetSocmediaLevel(socmedia):   
    if ( socmedia > 2.50 ):
        return 'high'
    if ( socmedia > 1.50):
        return 'moderate'
    else: 
        return 'low'
      
def GetDPA_awarenessLevel(dpa_awareness):   
    if ( dpa_awareness > 4.70 ):
        return 'high'
    if ( dpa_awareness > 4.0):
        return 'moderate'
    else: 
        return 'low'
      
def GetAgeRange(Age):   
    if ( Age > 65 ):
        return 'senior'
    if ( Age > 40 ):
        return 'middle'
    else: 
        return 'young'

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
        
        df1 = pd.DataFrame(X)
        df1.columns = ['Age',	'Position',	'socmedia',	'dpa_awareness']
        fig=plt.figure(figsize=(4,2))
        st.write("Social media mean rating (raw)")
        p = sns.countplot(x="socmedia", data = df1, palette="muted")
        _ = plt.setp(p.get_xticklabels(), rotation=90)
        st.pyplot(fig)
       
        st.write("DPA Awareness mean rating (raw)")
        fig=plt.figure(figsize=(6,3))
        p = sns.countplot(x="dpa_awareness", data = df1, palette="muted")
        _ = plt.setp(p.get_xticklabels(), rotation=90) 
        st.pyplot(fig)
        
        df1['socmedialevel'] = df1.apply(lambda x : GetSocmediaLevel(x['socmedia']), axis=1)
        st.write(df1.socmedialevel.value_counts())
        fig=plt.figure(figsize=(4,2))        
        sns.countplot(x="socmedialevel", data = df1, order=['high','moderate','low'],  palette="muted")
        plt.title('Social Media Levels')
        st.pyplot(fig) 
        
        st.write("DPA Awareness Levels")
        df1['DPAawarenesslevel'] = df1.apply(lambda x : GetDPA_awarenessLevel(x['dpa_awareness']), axis=1)
        st.write(df1.DPAawarenesslevel.value_counts())
        st.write("Age groups")
        df1['AgeRange'] = df1.apply(lambda x : GetAgeRange(x['Age']), axis=1)
        st.write(df1.AgeRange.value_counts())
        
        st.write("Levels of DPA Awareness Across Age Groups")
        fig=plt.figure(figsize=(4,2))
        p = sns.countplot(x='AgeRange', data = df1, hue='socmedialevel', palette='bright')
        _ = plt.setp(p.get_xticklabels(), rotation=90)
        st.pyplot(fig)
        
        st.write("Levels of Social Media Use Across Positions")
        fig=plt.figure(figsize=(4,2))
        df1['Position'] = label_encoder[0].inverse_transform(df1['Position'].astype(int))
        p = sns.countplot(x='Position', data = df1, hue='socmedialevel', palette='bright')
        _ = plt.setp(p.get_xticklabels(), rotation=90)
        st.pyplot(fig)
        
        st.write("Levels of DPA Awareness Across Age Groups")
        fig=plt.figure(figsize=(4,2))        
        p = sns.countplot(x='AgeRange', data = df1, hue='DPAawarenesslevel', palette='bright')
        _ = plt.setp(p.get_xticklabels(), rotation=90) 
        st.pyplot(fig)
 
        st.write("Levels of DPA Awareness Across Position")
        fig=plt.figure(figsize=(4,2))    
        p = sns.countplot(x='Position', data = df1, hue='DPAawarenesslevel', palette='bright')
        _ = plt.setp(p.get_xticklabels(), rotation=90)
        st.pyplot(fig)
        
        st.write("Compute Chi-Square for Age Groups and Social Media Use")
        # Generate a contingency table
        st.write("Contigency Table")
        cont_table = pd.crosstab(df1['AgeRange'], df1['socmedialevel'])
        st.write(cont_table)
    
        # perform a chi-square test of independence
        chi2_stat, p_value, dof, expected = chi2_contingency(cont_table)

        # print the results
        st.write("Chi-square statistic: " + str(chi2_stat))
        st.write("p-value: " + str(p_value))
        st.write("Degrees of freedom: " + str(dof))
        st.write("Expected frequencies: \n" + str(expected))

# Run the app
if __name__ == "__main__":
    app()
