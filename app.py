import streamlit as st
from PIL import Image
import numpy as np
import requests
st.markdown('''
            # Automated lung X-ray diagnosis 

            Welcome to the automated X-ray diagnosis. Please upload a X-ray image in png format and it will predict for you
            if you have tuberculosis or not. Our state of the art model will give you an accurate diagnosis
            of 100% chance of tuberculosis, even if you uploaded an image of your cat. 
''')

SERVER_URL = 'https://xray-vx3dknw5ea-ew.a.run.app'
LOCAL_URL = 'http://127.0.0.1:8000'

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Choose an X-ray image", type="png")

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    response = requests.post(url=f"{LOCAL_URL}/predict/", files=files).json()
    image = Image.open(uploaded_file)
    img_array = np.array(image)
    if float(list(response.values())[0]) >= 0.5:
        diagnosis = 'dying'
    else:
        diagnosis = 'healthy'
    st.image(
        img_array,
        caption=f"Your lungs looks like they are {diagnosis}",
        use_column_width=True,
    )
