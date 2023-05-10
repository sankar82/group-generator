#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import random
import streamlit as st
from typing import List
import base64
import os
import zipfile

def create_random_groups(input_file: str, output_prefix: str, num_groups: int) -> List[str]:
    df = pd.read_excel(input_file)
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    group_size = len(shuffled_df) // num_groups
    groups = [shuffled_df.iloc[i*group_size:(i+1)*group_size] for i in range(num_groups)]
    output_files = []
    for i, group in enumerate(groups):
        output_file = f"{output_prefix}_group_{i+1}.xlsx"
        group.to_excel(output_file, index=False)
        output_files.append(output_file)
    return output_files

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">{file_label}</a>'
    return href

def create_zip_file(output_files, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in output_files:
            zipf.write(file, os.path.basename(file))
            os.remove(file)

st.title("Random Group Generator")

num_groups = st.number_input("Number of groups", min_value=1, value=10, step=1)
uploaded_file = st.file_uploader("Upload an Excel file with the people's information", type=['xlsx', 'xls'])


if uploaded_file:
    with st.spinner("Creating random groups..."):
        temp_input_file = "temp_input.xlsx"
        with open(temp_input_file, "wb") as f:
            f.write(uploaded_file.getbuffer())

        output_files = create_random_groups(temp_input_file, "output", num_groups)

        os.remove(temp_input_file)

        zip_name = "output_groups.zip"
        create_zip_file(output_files, zip_name)

    st.success("Random groups generated successfully!")
    st.write("The groups have been generated and saved in a ZIP file. Click the link below to download it:")
    st.markdown(get_binary_file_downloader_html(zip_name, "Download ZIP file"), unsafe_allow_html=True)
    os.remove(zip_name)


# In[ ]:




