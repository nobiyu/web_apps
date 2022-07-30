import streamlit as st
import pandas as pd
import numpy as np

# Header and description
st.write("""
    # Mean-Variance-Standard Deviation Calculator
    \- by **Ayush Bist** \n
    This is a simple web application made using Streamlit to calculate Mean, Variance, Standard
    Deviation, Minimum value, Maximum value, and Sum accross a 3*3 matrix \n
    **Packages used:** Pandas, Numpy\n
    ***
""")

# input
st.header('Input')

input = "1 2 3 4 5 6 7 8 9"
input = st.text_area("Enter nine numbers, seperated by space as shown below:", input, height=220)
input = input.split()
st.write('---')


# custom function to calculate mean-var-std by converting list to a 3x3 matrice 
def calculate(list):
    if len(list) != 9:
        raise ValueError("List must contain nine numbers.")
    
    input_arr = np.array(list, dtype=int)
    input_3x3 = np.reshape(input_arr, (3,3))
    
    mean = [np.around(input_3x3.mean(0), decimals=2), np.around(input_3x3.mean(1), decimals=2), np.around(input_3x3.mean(), decimals=2)]
    var = [np.around(input_3x3.var(0), decimals=2), np.around(input_3x3.var(1), decimals=2), np.around(input_3x3.var(), decimals=2)]
    std = [np.around(input_3x3.std(0), decimals=2), np.around(input_3x3.std(1), decimals=2), input_3x3.std()]
    max = [np.around(input_3x3.max(0), decimals=2), np.around(input_3x3.max(1), decimals=2), np.around(input_3x3.max(), decimals=2) ]
    min=[np.around(input_3x3.min(0), decimals=2), np.around(input_3x3.min(1), decimals=2), np.around(input_3x3.min(), decimals=2)]
    sum=[np.around(input_3x3.sum(0), decimals=2), np.around(input_3x3.sum(1), decimals=2), np.around(input_3x3.sum(), decimals=2)]

    
    output = dict([
        ('Mean',mean),
        ('Variance', var),
        ('Standard deviation',std),
        ('Max',max),
        ('Min',min),
        ('Sum',sum),
        ])
    return output, input_3x3

output, matrice = calculate(input)
df = pd.DataFrame.from_dict(output,orient='index')
df = df.rename({0:'axis1', 1:'axis2', 2:'flat'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'function'})
st.write('')

if st.button('Show Matrice ->'):
    matrice

if st.button('Show Stats ->'):
    st.write(df)
