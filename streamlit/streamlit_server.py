import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def user_input_features():
    SepalLengthCm = st.sidebar.slider('SepalLengthCm', 4.3, 7.9, 5.4)
    SepalWidthCm = st.sidebar.slider('SepalWidthCm', 2.0, 4.4, 3.4)
    PetalLengthCm = st.sidebar.slider('PetalLengthCm', 1.0, 6.9, 3.5)
    PetalWidthCm = st.sidebar.slider('PetalWidthCm', 0.1, 2.5, 1.2)
    data = {
        'SepalLengthCm': SepalLengthCm,
        'SepalWidthCm': SepalWidthCm,
        'PetalLengthCm': PetalLengthCm,
        'PetalWidthCm': PetalWidthCm
    }
    features = pd.DataFrame(data, index=[0])
    return features

st.write("""
# Simple Iris Flower Prediction App
""")

st.sidebar.header("User Input data features")
st.sidebar.markdown("""


""")

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    input_df = user_input_features()

iris_row = pd.read_csv("Iris.csv")
iris = iris_row.drop(columns=["Id", "Species"], axis=1)
df = pd.concat([input_df, iris], axis=0)
df = df[:1]

st.subheader("User Input Features")

if uploaded_file is not None:
    st.write(df)
else:
    st.write("Using Sample Data, upload your own CSV file to use your data")
    st.write(df)

#model
load_clf = pickle.load(open("iris_clf.pkl", "rb"))
prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

st.subheader("Prediction")
iris_species = np.array(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
st.write(iris_species[prediction])
st.subheader("Prediction Probability")
st.write(prediction_proba)

