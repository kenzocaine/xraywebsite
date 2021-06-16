import streamlit as st
from PIL import Image
import numpy as np
import requests
import io
st.markdown('''
            # Automated lung X-ray diagnosis 

            Welcome to the automated X-ray diagnosis. Please upload a X-ray image in png format and it will predict for you
            if you have tuberculosis or not. Our state of the art model will give you an accurate diagnosis
            of 100% chance of tuberculosis, even if you uploaded an image of your cat. 
''')

SERVER_URL = 'https://xray-vx3dknw5ea-ew.a.run.app'
LOCAL_URL = 'http://127.0.0.1:8000'

st.set_option('deprecation.showfileUploaderEncoding', False)

left_column, right_column = st.beta_columns(2)
uploaded_file = st.file_uploader("Choose an X-ray image", type="png")


if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    print(type(uploaded_file))
    with open("out.png", "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(uploaded_file.getbuffer())

    uploaded_file = open('out.png', 'rb')
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    response = requests.post(url=f"{LOCAL_URL}/predict/", files=files).json()
    print('Response 1')

    image = Image.open(uploaded_file)
    img_array = np.array(image)

    uploaded_file = open('out.png', 'rb')
    files = {"file": (uploaded_file.name, uploaded_file, "multipart/form-data")}
    response_seg = requests.post(url=f"{LOCAL_URL}/seglung/", files=files)
    print('Response 2')

    img = io.BytesIO(response_seg.content)
    image_seg = Image.open(img)
    img_array_seg = np.array(image_seg)

    if float(list(response.values())[0]) >= 0.5:
        diagnosis = 'dying'
    else:
        diagnosis = 'healthy'
    with left_column:
        st.image(
            img_array,
            caption=f"Your lungs looks like they are {diagnosis}",
            use_column_width=True,
        )
        st.image(
            img_array_seg,
            caption='Segmented lungs',
            use_column_width=True
        )

    with right_column:
        st.markdown('You are dying')



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
