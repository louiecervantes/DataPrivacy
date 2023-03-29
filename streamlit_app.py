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

# Define the Streamlit app
def app():
    st.header("Welcome to Data Privacy Awareness Study")
    st.subheader("Louie F. Cervantes M.Eng. \n(c) 2023 WVSU College of ICT")
    
    st.title("Awareness and Utilization of Data Privacy in Social Media")
    st.write("Sequential explanatory mixed method research design was used in this study. It started with collecting and analyzing quantitative data using a validated and reliability-tested two sets of researcher-made instrument that was used to determine the school personnel’s level of awareness on data privacy and their degree of personal information shared on social media.")

    # Load the mobile phone dataset
    df = pd.read_csv('data_privacy.csv', dtype='str', header=0, 
        sep = ",", encoding='latin')
    st.dataframe(df, width=800, height=400)
    desc = df.describe().T
    st.write(desc)
    
    if st.button('Begin'):
        st.write("We select the relevant attributes for describing our samples.")
        df1 = df.loc[:, ['Age', 'Position']]
        st.write(df1.head())


# Run the app
if __name__ == "__main__":
    app()
