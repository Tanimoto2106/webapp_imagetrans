import os
import streamlit as st
from PIL import Image
import pyheif
from io import BytesIO

def heif_to_image(heif_file):
    heif_image = pyheif.read(heif_file)
    image = Image.frombytes(
        heif_image.mode, 
        heif_image.size, 
        heif_image.data,
        "raw",
        heif_image.mode,
        heif_image.stride,
    )
    return image

st.title('Image Converter')

uploaded_files = st.file_uploader("Choose image files", type=["heic", "heif", "jpeg", "jpg", "png", "gif"], accept_multiple_files=True)

output_format = st.selectbox("Select Output Format", ["JPEG", "PNG", "GIF"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_byte_stream = uploaded_file.read()
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension in ['heic', 'heif']:
                image = heif_to_image(file_byte_stream)
            else:
                image = Image.open(BytesIO(file_byte_stream))
            
            st.image(image, caption=f'Converted {uploaded_file.name}')
            
            output_image = BytesIO()
            image.save(output_image, format=output_format)
            
            st.download_button(
                label=f"Download {os.path.splitext(uploaded_file.name)[0]}.{output_format.lower()}",
                data=output_image.getvalue(),
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}.{output_format.lower()}",
                mime=f'image/{output_format.lower()}',
            )
        except Exception as e:
            st.error(f"Error converting {uploaded_file.name}: {e}")
