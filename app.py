import streamlit as st
from PIL import Image
import PIL
from PIL.ImageOps import invert
import numpy as np
import requests
import io
st.markdown('''
            # Automated lung X-ray diagnosis 

            *Welcome to the automated X-ray diagnosis. Please upload an X-ray image in .png format and it will predict for you
            if you have tuberculosis or not.* 
''')
SERVER_URL = 'https://automated-tb-diagnostics-vx3dknw5ea-lz.a.run.app' 
#SERVER_URL = 'https://xray-vx3dknw5ea-ew.a.run.app'
#LOCAL_URL = 'http://127.0.0.1:8000'
LOCAL_URL = 'http://0.0.0.0:8000'


st.set_option('deprecation.showfileUploaderEncoding', False)

left_column, right_column = st.beta_columns(2)
uploaded_file = st.file_uploader("Choose an X-ray image", type="png")

st.markdown("<h1 style='font-size: 18px ;text-align: center;'>DISCLAIMER:</h1>", unsafe_allow_html=True)
st.markdown('1. We are **not** doctors/medical professionals.')
st.markdown('2. Our model is **not** quite state-of-the-art.')
st.markdown('3. DO NOT EVER construe our predictions as medical advice.')
st.markdown('4. If you suspect you may have TB, consult official public-health agencies and follow best practices advised therin.')
st.markdown('5. Even though this project is awesome-ish, it is purely for demonstrative and exploratory purposes.')

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    print(type(uploaded_file))
    with open("out.png", "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(uploaded_file.getbuffer())

    uploaded_file = open('out.png', 'rb')
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    response = requests.post(url=f"{SERVER_URL}/predict/", files=files).json()
    print('Response 1')

    image = Image.open(uploaded_file)
    img_array =np.array(image)
    print(img_array)

    uploaded_file = open('out.png', 'rb')
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    response_seg = requests.post(url=f"{SERVER_URL}/seglung/", files=files)
    print('Response 2')

    img = io.BytesIO(response_seg.content)
    image_seg = Image.open(img)
    img_array_seg = np.array(image_seg)
    prediction = float(list(response.values())[0])
    chance = round(float(list(response.values())[0]) * 100, 2)
    if prediction >= 0.3:
        diagnosis = 'dying'
    else:
        diagnosis = 'healthy'
    with left_column:
        st.text(" \n")
        st.image(
            img_array,
            caption=f"Your uploaded X-ray",
            use_column_width=True,
        )
        st.image(
            img_array_seg,
            caption='Segmented lungs',
            use_column_width=True
        )

    with right_column:
        if diagnosis == 'dying':
            st.markdown(f"<h1 style='color: red; font-size: 25px;'>Unfortunately, according to our model, there is a probability of {chance} % that you have tuberculosis.</h1>", unsafe_allow_html=True)
            st.markdown("1. <h1 style='font-size: 15px;'> If you are located in the USA, please check out financing options in <a href=https://www.gofundme.com/>Gofundme</a></h1>", unsafe_allow_html=True) 
            st.markdown("2. <h1 style='font-size: 15px;'> If you are located in Sweden, please check out cheap flights to Poland in <a href=https://www.skyscanner.se//>Skyscanner</a></h1>", unsafe_allow_html=True) 
        else:
            st.markdown("<h1 style='color: green; font-size:25px;'>According to our model, you do NOT have tuberculosis.</h1>", unsafe_allow_html=True)



# uploaded_file_seg = st.file_uploader("Choose an X-ray image for segmentation", type="png")

# if uploaded_file_seg is not None:
#    files = {"file": (uploaded_file_seg.name, uploaded_file_seg, "multipart/form-data")}
#    response = requests.post(url=f"{LOCAL_URL}/seglung/", files=files)
#    print(type(response))
#    print(type(response.content))
#    print(response.content[:10])
#    img = io.BytesIO(response.content)
#    image = Image.open(img)
#    img_array = np.array(image)
#    st.image(
#        img_array,
#        caption="Your segmented lungs",
#        use_column_width=True,
#    )
