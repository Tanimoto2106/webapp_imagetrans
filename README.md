# webapp_imagetrans
# 画像変換ウェブアプリ

このウェブアプリはStreamlitを使用して作成され、ユーザーが異なる形式間で画像ファイルを変換できるようにします。サポートされている入力形式には、HEIC、HEIF、JPEG、JPG、PNG、およびGIFが含まれます。

## コード

```python
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

st.title('画像変換')

uploaded_files = st.file_uploader("画像ファイルを選択してください", type=["heic", "heif", "jpeg", "jpg", "png", "gif"], accept_multiple_files=True)

output_format = st.selectbox("出力形式を選択", ["JPEG", "PNG", "GIF"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            file_byte_stream = uploaded_file.read()
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension in ['heic', 'heif']:
                image = heif_to_image(file_byte_stream)
            else:
                image = Image.open(BytesIO(file_byte_stream))
            
            st.image(image, caption=f'変換した {uploaded_file.name}')
            
            output_image = BytesIO()
            image.save(output_image, format=output_format)
            
            st.download_button(
                label=f"{os.path.splitext(uploaded_file.name)[0]}.{output_format.lower()} をダウンロード",
                data=output_image.getvalue(),
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}.{output_format.lower()}",
                mime=f'image/{output_format.lower()}',
            )
        except Exception as e:
            st.error(f"{uploaded_file.name} の変換エラー: {e}")
```

## 使用方法

1. コマンド `streamlit run webapp_imagetrans.py` を使用して、Streamlitアプリを実行します。
2. アプリのファイルアップローダーを使用して画像ファイルをアップロードします。
3. ドロップダウンメニューから希望の出力形式を選択します。
4. 変換された画像がダウンロードボタンと共に表示されます。

## 依存関係

- Python
- Streamlit
- Pillow
- pyheif
