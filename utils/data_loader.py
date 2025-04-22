import os
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="📁 Đang tải dữ liệu...")
def load_data():
    # base_path là thư mục gốc của project
    base_path = os.path.dirname(os.path.dirname(__file__))
    path_1 = os.path.join(base_path, 'data', 'Products_ThoiTrangNam_raw.csv')
    path_2 = os.path.join(base_path, 'data', 'Products_ThoiTrangNam_rating_raw.csv')

    # Đọc dữ liệu
    file_1 = pd.read_csv(path_1)
    file_2 = pd.read_csv(path_2, sep='\t')  

    # Kiểm tra cột quan trọng
    if 'product_id' not in file_1.columns or 'product_id' not in file_2.columns:
        raise KeyError("Thiếu cột 'product_id' trong file_1 hoặc file_2.")

    # Làm sạch dữ liệu
    file_2.drop_duplicates(inplace=True)
    file_1 = file_1.dropna(subset=['description'])

    # Gán ảnh mặc định nếu thiếu
    default_img = "https://via.placeholder.com/100x100.png?text=No+Image"
    file_1['image'] = file_1['image'].fillna('').apply(lambda x: x if x.strip() != '' else default_img)

    # Merge dữ liệu
    df = pd.merge(
        file_2,
        file_1[['product_id', 'product_name', 'price', 'sub_category', 'image', 'link', 'description']],
        on='product_id',
        how='inner'
    )

    return file_1, file_2, df

@st.cache_data
def load_stop_words(file_path: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Không tìm thấy file stop words tại: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        stop_words = f.read().splitlines()

    # Loại bỏ từ "ngủ" khỏi danh sách
    stop_words = [word for word in stop_words if word.strip().lower() != "ngủ"]

    return stop_words

