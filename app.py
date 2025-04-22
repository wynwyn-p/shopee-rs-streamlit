# File chính gọi các components
import streamlit as st
import pandas as pd

# Import các module
from components import sidebar, home, introduction, exploration, visualization, demo, link_code
from utils.data_loader import load_data, load_stop_words
from utils.model_loader import load_all_models

# Cấu hình giao diện trang
st.set_page_config(page_title="Shopee Recommender", page_icon="🛍️", layout="wide")

# Hiển thị thanh bên
sidebar.show()

# ========================== Load dữ liệu và mô hình ==========================
with st.spinner("📁 Đang tải dữ liệu và mô hình..."):
    # Load dữ liệu
    file_1, file_2, df = load_data()

    # Load stopword
    stop_words = load_stop_words("utils/vietnamese-stopwords.txt")

    # Load toàn bộ mô hình
    MODEL_DIR = "models"
    dictionary, tfidf_model, similarity_index, df_final, baseline_model = load_all_models(MODEL_DIR)

# ========================== Điều hướng theo menu ==========================
selected = st.session_state.get("selected_page", "Introduction")

if selected == "Home":
    home.show()
elif selected == "Introduction":
    introduction.show()
elif selected == "Data Exploration":
    exploration.render_exploration(file_1)
elif selected == "Data Visualization":
    visualization.show(df)
elif selected == "Demo App":
    # Gọi demo với đúng dữ liệu
    demo.show(
        file_2=file_2,              # Dữ liệu rating (chứa user_id)
        file_1=file_1,              # Dữ liệu sản phẩm gốc
        df=df,                      # Dữ liệu đã merge user-product
        df_final=df_final,          # Dữ liệu đã tokenize (dùng cho TF-IDF)
        dictionary=dictionary,
        tfidf_model=tfidf_model,
        similarity_index=similarity_index,
        stop_words=stop_words,
        baseline_model=baseline_model
    )
elif selected == "Link Code":
    link_code.show()
